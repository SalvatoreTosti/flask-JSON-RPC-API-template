from app import app
from functools import wraps
from enum import Enum
from flask import request, jsonify  # request, url_for, g
from app.models.task import Task

# Add support for Notifications (requests without ids)
@app.route("/rpc", methods=["POST"])
def rpc():
    dispatcher = JSONRPCDispatcher([TestModel(), Task()])
    return jsonify(dispatcher.evaluate(request.json))


class TestModel:
    def dispatches(self):
        return {"test.test": self._test}

    def _test(self, params):
        return {"success": "true"}


class JSONRPC:
    def validate_request(request_payload):
        if request_payload.get("jsonrpc") != "2.0":
            raise JSONRPC.InvalidRequestException()

        if "id" not in request_payload:
            raise JSONRPC.InvalidRequestException()

    class ParseErrorException(Exception):
        ...

    class InvalidRequestException(Exception):
        ...

    class MethodNotFoundException(Exception):
        ...

    class InvalidParamsException(Exception):
        ...

    class InternalErrorException(Exception):
        ...

    class RPC_ERROR(Enum):
        PARSE_ERROR = 1
        INVALID_REQUEST = 2
        METHOD_NOT_FOUND = 3
        INVALID_PARAMS = 4
        INTERNAL_ERROR = 5

    def error(RPC_Error):
        errors = {
            JSONRPC.RPC_ERROR.PARSE_ERROR: {"code": -32700, "message": "Parse error"},
            JSONRPC.RPC_ERROR.INVALID_REQUEST: {
                "code": -32600,
                "message": "Invalid Request",
            },
            JSONRPC.RPC_ERROR.METHOD_NOT_FOUND: {
                "code": -32601,
                "message": "Method not found",
            },
            JSONRPC.RPC_ERROR.INVALID_PARAMS: {
                "code": -32602,
                "message": "Invalid params",
            },
            JSONRPC.RPC_ERROR.INTERNAL_ERROR: {
                "code": -32603,
                "message": "Internal error",
            },
        }
        _error = errors.get(RPC_Error)
        if not _error:
            return errors[INTERNAL_ERROR]
        return _error

    def JSONRPCExceptionToError(fn):
        @wraps(fn)
        def decorated_function(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except JSONRPC.ParseErrorException:
                return JSONRPC.error(JSONRPC.RPC_ERROR.PARSE_ERROR)
            except JSONRPC.InvalidRequestException:
                return JSONRPC.error(JSONRPC.RPC_ERROR.INVALID_REQUEST)
            except JSONRPC.MethodNotFoundException:
                return JSONRPC.error(JSONRPC.RPC_ERROR.METHOD_NOT_FOUND)
            except JSONRPC.InvalidParamsException:
                return JSONRPC.error(JSONRPC.RPC_ERROR.INVALID_PARAMS)
            except JSONRPC.InternalErrorException:
                return JSONRPC.error(JSONRPC.RPC_ERROR.INTERNAL_ERROR)

        return decorated_function


class JSONRPCDispatcher:
    def __init__(self, JSONRPCModels):
        self._dispatch_dict = {}
        for model in JSONRPCModels:
            self._dispatch_dict.update(model.dispatches())

    def dispatch(self, method, params):
        fn = self._dispatch_dict.get(method)
        if not fn:
            raise JSONRPC.MethodNotFoundException()
        return fn(params)

    @JSONRPC.JSONRPCExceptionToError
    def evaluate(self, request_payload):
        JSONRPC.validate_request(request_payload)
        method = request_payload.get("method")
        params = request_payload.get("params")
        result = self.dispatch(method, params)
        return {"jsonrpc": "2.0", "id": request_payload["id"], "result": result}
