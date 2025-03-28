# Copyright Modal Labs 2022
import io
import pickle
import typing
from dataclasses import dataclass
from typing import Any

from modal._utils.async_utils import synchronizer
from modal_proto import api_pb2

from ._object import _Object
from ._vendor import cloudpickle
from .config import logger
from .exception import DeserializationError, ExecutionError, InvalidError
from .object import Object

if typing.TYPE_CHECKING:
    import modal.client

PICKLE_PROTOCOL = 4  # Support older Python versions.


class Pickler(cloudpickle.Pickler):
    def __init__(self, buf):
        super().__init__(buf, protocol=PICKLE_PROTOCOL)

    def persistent_id(self, obj):
        from modal.partial_function import PartialFunction

        if isinstance(obj, _Object):
            flag = "_o"
        elif isinstance(obj, Object):
            flag = "o"
        elif isinstance(obj, PartialFunction):
            # Special case for PartialObject since it's a synchronicity wrapped object
            # that's set on serialized classes.
            # The resulting pickled instance can't be deserialized without this in a
            # new process, since the original referenced synchronizer will have different
            # values for `._original_attr` etc.

            impl_object = synchronizer._translate_in(obj)
            attributes = impl_object.__dict__.copy()
            # ugly - we remove the `._wrapped_attr` attribute from the implementation instance
            # to avoid referencing and therefore pickling the wrapped instance despite having
            # translated it to the implementation type

            # it would be nice if we could avoid this by not having the wrapped instances
            # be directly linked from objects and instead having a lookup table in the Synchronizer:
            if synchronizer._wrapped_attr and synchronizer._wrapped_attr in attributes:
                attributes.pop(synchronizer._wrapped_attr)

            return ("sync", (impl_object.__class__, attributes))
        else:
            return
        if not obj.is_hydrated:
            raise InvalidError(f"Can't serialize object {obj} which hasn't been hydrated.")
        return (obj.object_id, flag, obj._get_metadata())


class Unpickler(pickle.Unpickler):
    def __init__(self, client, buf):
        self.client = client
        super().__init__(buf)

    def persistent_load(self, pid):
        if len(pid) == 2:
            # more general protocol
            obj_type, obj_data = pid
            if obj_type == "sync":  # synchronicity wrapped object
                # not actually a proto object in this case but the underlying object of a synchronicity object
                impl_class, attributes = obj_data
                impl_instance = impl_class.__new__(impl_class)
                impl_instance.__dict__.update(attributes)
                return synchronizer._translate_out(impl_instance)
            else:
                raise ExecutionError("Unknown serialization format")

        # old protocol, always a 3-tuple
        (object_id, flag, handle_proto) = pid
        if flag in ("o", "p", "h"):
            return Object._new_hydrated(object_id, self.client, handle_proto)
        elif flag in ("_o", "_p", "_h"):
            return _Object._new_hydrated(object_id, self.client, handle_proto)
        else:
            raise InvalidError("bad flag")


def serialize(obj: Any) -> bytes:
    """Serializes object and replaces all references to the client class by a placeholder."""
    buf = io.BytesIO()
    Pickler(buf).dump(obj)
    return buf.getvalue()


def deserialize(s: bytes, client) -> Any:
    """Deserializes object and replaces all client placeholders by self."""
    from ._runtime.execution_context import is_local  # Avoid circular import

    env = "local" if is_local() else "remote"
    try:
        return Unpickler(client, io.BytesIO(s)).load()
    except AttributeError as exc:
        # We use a different cloudpickle version pre- and post-3.11. Unfortunately cloudpickle
        # doesn't expose some kind of serialization version number, so we have to guess based
        # on the error message.
        if "Can't get attribute '_make_function'" in str(exc):
            raise DeserializationError(
                "Deserialization failed due to a version mismatch between local and remote environments. "
                "Try changing the Python version in your Modal image to match your local Python version. "
            ) from exc
        else:
            # On Python 3.10+, AttributeError has `.name` and `.obj` attributes for better custom reporting
            raise DeserializationError(
                f"Deserialization failed with an AttributeError, {exc}. This is probably because"
                " you have different versions of a library in your local and remote environments."
            ) from exc
    except ModuleNotFoundError as exc:
        raise DeserializationError(
            f"Deserialization failed because the '{exc.name}' module is not available in the {env} environment."
        ) from exc
    except Exception as exc:
        if env == "remote":
            # We currently don't always package the full traceback from errors in the remote entrypoint logic.
            # So try to include as much information as we can in the main error message.
            more = f": {type(exc)}({str(exc)})"
        else:
            # When running locally, we can just rely on standard exception chaining.
            more = " (see above for details)"
        raise DeserializationError(
            f"Encountered an error when deserializing an object in the {env} environment{more}."
        ) from exc


def _serialize_asgi(obj: Any) -> api_pb2.Asgi:
    def flatten_headers(obj):
        return [s for k, v in obj for s in (k, v)]

    if obj is None:
        return api_pb2.Asgi()

    msg_type = obj.get("type")

    if msg_type == "http":
        return api_pb2.Asgi(
            http=api_pb2.Asgi.Http(
                http_version=obj.get("http_version", "1.1"),
                method=obj["method"],
                scheme=obj.get("scheme", "http"),
                path=obj["path"],
                query_string=obj.get("query_string"),
                headers=flatten_headers(obj.get("headers", [])),
                client_host=obj["client"][0] if obj.get("client") else None,
                client_port=obj["client"][1] if obj.get("client") else None,
            )
        )
    elif msg_type == "http.request":
        return api_pb2.Asgi(
            http_request=api_pb2.Asgi.HttpRequest(
                body=obj.get("body"),
                more_body=obj.get("more_body"),
            )
        )
    elif msg_type == "http.response.start":
        return api_pb2.Asgi(
            http_response_start=api_pb2.Asgi.HttpResponseStart(
                status=obj["status"],
                headers=flatten_headers(obj.get("headers", [])),
                trailers=obj.get("trailers"),
            )
        )
    elif msg_type == "http.response.body":
        return api_pb2.Asgi(
            http_response_body=api_pb2.Asgi.HttpResponseBody(
                body=obj.get("body"),
                more_body=obj.get("more_body"),
            )
        )
    elif msg_type == "http.response.trailers":
        return api_pb2.Asgi(
            http_response_trailers=api_pb2.Asgi.HttpResponseTrailers(
                headers=flatten_headers(obj.get("headers", [])),
                more_trailers=obj.get("more_trailers"),
            )
        )
    elif msg_type == "http.disconnect":
        return api_pb2.Asgi(http_disconnect=api_pb2.Asgi.HttpDisconnect())

    elif msg_type == "websocket":
        return api_pb2.Asgi(
            websocket=api_pb2.Asgi.Websocket(
                http_version=obj.get("http_version", "1.1"),
                scheme=obj.get("scheme", "ws"),
                path=obj["path"],
                query_string=obj.get("query_string"),
                headers=flatten_headers(obj.get("headers", [])),
                client_host=obj["client"][0] if obj.get("client") else None,
                client_port=obj["client"][1] if obj.get("client") else None,
                subprotocols=obj.get("subprotocols"),
            )
        )
    elif msg_type == "websocket.connect":
        return api_pb2.Asgi(
            websocket_connect=api_pb2.Asgi.WebsocketConnect(),
        )
    elif msg_type == "websocket.accept":
        return api_pb2.Asgi(
            websocket_accept=api_pb2.Asgi.WebsocketAccept(
                subprotocol=obj.get("subprotocol"),
                headers=flatten_headers(obj.get("headers", [])),
            )
        )
    elif msg_type == "websocket.receive":
        return api_pb2.Asgi(
            websocket_receive=api_pb2.Asgi.WebsocketReceive(
                bytes=obj.get("bytes"),
                text=obj.get("text"),
            )
        )
    elif msg_type == "websocket.send":
        return api_pb2.Asgi(
            websocket_send=api_pb2.Asgi.WebsocketSend(
                bytes=obj.get("bytes"),
                text=obj.get("text"),
            )
        )
    elif msg_type == "websocket.disconnect":
        return api_pb2.Asgi(
            websocket_disconnect=api_pb2.Asgi.WebsocketDisconnect(
                code=obj.get("code"),
            )
        )
    elif msg_type == "websocket.close":
        return api_pb2.Asgi(
            websocket_close=api_pb2.Asgi.WebsocketClose(
                code=obj.get("code"),
                reason=obj.get("reason"),
            )
        )

    else:
        logger.debug("skipping serialization of unknown ASGI message type %r", msg_type)
        return api_pb2.Asgi()


def _deserialize_asgi(asgi: api_pb2.Asgi) -> Any:
    def unflatten_headers(obj):
        return list(zip(obj[::2], obj[1::2]))

    msg_type = asgi.WhichOneof("type")

    if msg_type == "http":
        return {
            "type": "http",
            "http_version": asgi.http.http_version,
            "method": asgi.http.method,
            "scheme": asgi.http.scheme,
            "path": asgi.http.path,
            "query_string": asgi.http.query_string,
            "headers": unflatten_headers(asgi.http.headers),
            **({"client": (asgi.http.client_host, asgi.http.client_port)} if asgi.http.HasField("client_host") else {}),
            "extensions": {
                "http.response.trailers": {},
            },
        }
    elif msg_type == "http_request":
        return {
            "type": "http.request",
            "body": asgi.http_request.body,
            "more_body": asgi.http_request.more_body,
        }
    elif msg_type == "http_response_start":
        return {
            "type": "http.response.start",
            "status": asgi.http_response_start.status,
            "headers": unflatten_headers(asgi.http_response_start.headers),
            "trailers": asgi.http_response_start.trailers,
        }
    elif msg_type == "http_response_body":
        return {
            "type": "http.response.body",
            "body": asgi.http_response_body.body,
            "more_body": asgi.http_response_body.more_body,
        }
    elif msg_type == "http_response_trailers":
        return {
            "type": "http.response.trailers",
            "headers": unflatten_headers(asgi.http_response_trailers.headers),
            "more_trailers": asgi.http_response_trailers.more_trailers,
        }
    elif msg_type == "http_disconnect":
        return {"type": "http.disconnect"}

    elif msg_type == "websocket":
        return {
            "type": "websocket",
            "http_version": asgi.websocket.http_version,
            "scheme": asgi.websocket.scheme,
            "path": asgi.websocket.path,
            "query_string": asgi.websocket.query_string,
            "headers": unflatten_headers(asgi.websocket.headers),
            **(
                {"client": (asgi.websocket.client_host, asgi.websocket.client_port)}
                if asgi.websocket.HasField("client_host")
                else {}
            ),
            "subprotocols": list(asgi.websocket.subprotocols),
        }
    elif msg_type == "websocket_connect":
        return {"type": "websocket.connect"}
    elif msg_type == "websocket_accept":
        return {
            "type": "websocket.accept",
            "subprotocol": asgi.websocket_accept.subprotocol if asgi.websocket_accept.HasField("subprotocol") else None,
            "headers": unflatten_headers(asgi.websocket_accept.headers),
        }
    elif msg_type == "websocket_receive":
        return {
            "type": "websocket.receive",
            "bytes": asgi.websocket_receive.bytes if asgi.websocket_receive.HasField("bytes") else None,
            "text": asgi.websocket_receive.text if asgi.websocket_receive.HasField("text") else None,
        }
    elif msg_type == "websocket_send":
        return {
            "type": "websocket.send",
            "bytes": asgi.websocket_send.bytes if asgi.websocket_send.HasField("bytes") else None,
            "text": asgi.websocket_send.text if asgi.websocket_send.HasField("text") else None,
        }
    elif msg_type == "websocket_disconnect":
        return {
            "type": "websocket.disconnect",
            "code": asgi.websocket_disconnect.code if asgi.websocket_disconnect.HasField("code") else 1005,
        }
    elif msg_type == "websocket_close":
        return {
            "type": "websocket.close",
            "code": asgi.websocket_close.code if asgi.websocket_close.HasField("code") else 1000,
            "reason": asgi.websocket_close.reason,
        }

    else:
        assert msg_type is None
        return None


def serialize_data_format(obj: Any, data_format: int) -> bytes:
    """Similar to serialize(), but supports other data formats."""
    if data_format == api_pb2.DATA_FORMAT_PICKLE:
        return serialize(obj)
    elif data_format == api_pb2.DATA_FORMAT_ASGI:
        return _serialize_asgi(obj).SerializeToString(deterministic=True)
    elif data_format == api_pb2.DATA_FORMAT_GENERATOR_DONE:
        assert isinstance(obj, api_pb2.GeneratorDone)
        return obj.SerializeToString(deterministic=True)
    else:
        raise InvalidError(f"Unknown data format {data_format!r}")


def deserialize_data_format(s: bytes, data_format: int, client) -> Any:
    if data_format == api_pb2.DATA_FORMAT_PICKLE:
        return deserialize(s, client)
    elif data_format == api_pb2.DATA_FORMAT_ASGI:
        return _deserialize_asgi(api_pb2.Asgi.FromString(s))
    elif data_format == api_pb2.DATA_FORMAT_GENERATOR_DONE:
        return api_pb2.GeneratorDone.FromString(s)
    else:
        raise InvalidError(f"Unknown data format {data_format!r}")


class ClsConstructorPickler(pickle.Pickler):
    def __init__(self, buf):
        super().__init__(buf, protocol=PICKLE_PROTOCOL)

    def persistent_id(self, obj):
        if isinstance(obj, (_Object, Object)):
            if not obj.object_id:
                raise InvalidError(f"Can't serialize object {obj} which hasn't been created.")
            return True


def check_valid_cls_constructor_arg(key, obj):
    # Basically pickle, but with support for modal objects
    buf = io.BytesIO()
    try:
        ClsConstructorPickler(buf).dump(obj)
        return True
    except (AttributeError, ValueError):
        raise ValueError(
            f"Only pickle-able types are allowed in remote class constructors: argument {key} of type {type(obj)}."
        )


def assert_bytes(obj: Any):
    if not isinstance(obj, bytes):
        raise TypeError(f"Expected bytes, got {type(obj)}")
    return obj


@dataclass
class ParamTypeInfo:
    default_field: str
    proto_field: str
    converter: typing.Callable[[str], typing.Any]
    type: type


PYTHON_TO_PROTO_TYPE: dict[type, "api_pb2.ParameterType.ValueType"] = {
    # python type -> protobuf type enum
    str: api_pb2.PARAM_TYPE_STRING,
    int: api_pb2.PARAM_TYPE_INT,
    bytes: api_pb2.PARAM_TYPE_BYTES,
}

PROTO_TYPE_INFO = {
    # Protobuf type enum -> encode/decode helper metadata
    api_pb2.PARAM_TYPE_STRING: ParamTypeInfo(
        default_field="string_default",
        proto_field="string_value",
        converter=str,
        type=str,
    ),
    api_pb2.PARAM_TYPE_INT: ParamTypeInfo(
        default_field="int_default",
        proto_field="int_value",
        converter=int,
        type=int,
    ),
    api_pb2.PARAM_TYPE_BYTES: ParamTypeInfo(
        default_field="bytes_default",
        proto_field="bytes_value",
        converter=assert_bytes,
        type=bytes,
    ),
}


def apply_defaults(
    python_params: typing.Mapping[str, Any], schema: typing.Sequence[api_pb2.ClassParameterSpec]
) -> dict[str, Any]:
    """Apply any declared defaults from the provided schema, if values aren't provided in python_params

    Conceptually similar to inspect.BoundArguments.apply_defaults.

    Note: Apply this before serializing parameters in order to get consistent parameter
        pools regardless if a value is explicitly provided or not.
    """
    result = {**python_params}
    for schema_param in schema:
        if schema_param.has_default and schema_param.name not in python_params:
            default_field_name = schema_param.WhichOneof("default_oneof")
            if default_field_name is None:
                raise InvalidError(f"{schema_param.name} declared as having a default, but has no default value")
            result[schema_param.name] = getattr(schema_param, default_field_name)
    return result


def serialize_proto_params(python_params: dict[str, Any]) -> bytes:
    proto_params: list[api_pb2.ClassParameterValue] = []
    for param_name, python_value in python_params.items():
        python_type = type(python_value)
        protobuf_type = get_proto_parameter_type(python_type)
        type_info = PROTO_TYPE_INFO.get(protobuf_type)
        proto_param = api_pb2.ClassParameterValue(
            name=param_name,
            type=protobuf_type,
        )
        try:
            converted_value = type_info.converter(python_value)
        except ValueError as exc:
            raise ValueError(f"Invalid type for parameter {param_name}: {exc}")
        setattr(proto_param, type_info.proto_field, converted_value)
        proto_params.append(proto_param)
    proto_bytes = api_pb2.ClassParameterSet(parameters=proto_params).SerializeToString(deterministic=True)
    return proto_bytes


def deserialize_proto_params(serialized_params: bytes) -> dict[str, Any]:
    proto_struct = api_pb2.ClassParameterSet()
    proto_struct.ParseFromString(serialized_params)
    python_params = {}
    for param in proto_struct.parameters:
        python_value: Any
        if param.type == api_pb2.PARAM_TYPE_STRING:
            python_value = param.string_value
        elif param.type == api_pb2.PARAM_TYPE_INT:
            python_value = param.int_value
        elif param.type == api_pb2.PARAM_TYPE_BYTES:
            python_value = param.bytes_value
        else:
            raise NotImplementedError(f"Unimplemented parameter type: {param.type}.")

        python_params[param.name] = python_value

    return python_params


def validate_params(params: dict[str, Any], schema: typing.Sequence[api_pb2.ClassParameterSpec]):
    # first check that all declared values are provided
    for schema_param in schema:
        if schema_param.name not in params:
            # we expect all values to be present - even defaulted ones (defaults are applied on payload construction)
            raise InvalidError(f"Missing required parameter: {schema_param.name}")
        python_value = params[schema_param.name]
        python_type = type(python_value)
        param_protobuf_type = get_proto_parameter_type(python_type)
        if schema_param.type != param_protobuf_type:
            expected_python_type = PROTO_TYPE_INFO[schema_param.type].type
            raise TypeError(
                f"Parameter '{schema_param.name}' type error: expected {expected_python_type.__name__}, "
                f"got {python_type.__name__}"
            )

    schema_fields = {p.name for p in schema}
    # then check that no extra values are provided
    non_declared_fields = params.keys() - schema_fields
    if non_declared_fields:
        raise InvalidError(
            f"The following parameter names were provided but are not present in the schema: {non_declared_fields}"
        )


def deserialize_params(serialized_params: bytes, function_def: api_pb2.Function, _client: "modal.client._Client"):
    if function_def.class_parameter_info.format in (
        api_pb2.ClassParameterInfo.PARAM_SERIALIZATION_FORMAT_UNSPECIFIED,
        api_pb2.ClassParameterInfo.PARAM_SERIALIZATION_FORMAT_PICKLE,
    ):
        # legacy serialization format - pickle of `(args, kwargs)` w/ support for modal object arguments
        param_args, param_kwargs = deserialize(serialized_params, _client)
    elif function_def.class_parameter_info.format == api_pb2.ClassParameterInfo.PARAM_SERIALIZATION_FORMAT_PROTO:
        param_args = ()  # we use kwargs only for our implicit constructors
        param_kwargs = deserialize_proto_params(serialized_params)
        # TODO: We can probably remove the validation below since we do validation in the caller?
        validate_params(param_kwargs, list(function_def.class_parameter_info.schema))
    else:
        raise ExecutionError(
            f"Unknown class parameter serialization format: {function_def.class_parameter_info.format}"
        )

    return param_args, param_kwargs


def get_proto_parameter_type(parameter_type: type) -> "api_pb2.ParameterType.ValueType":
    if parameter_type not in PYTHON_TO_PROTO_TYPE:
        type_name = getattr(parameter_type, "__name__", repr(parameter_type))
        supported = ", ".join(parameter_type.__name__ for parameter_type in PYTHON_TO_PROTO_TYPE.keys())
        raise InvalidError(f"{type_name} is not a supported parameter type. Use one of: {supported}")
    return PYTHON_TO_PROTO_TYPE[parameter_type]
