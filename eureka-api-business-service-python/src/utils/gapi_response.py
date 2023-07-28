import grpc
from src.protos.business_pb2 import *


def gapi_response(message, function_call, schema, context, success_message):

    if type(message) == CreateBusinessResponse:

        try:

            result = function_call(schema, context)

            response = CreateBusinessResponse(
                code=grpc.StatusCode.OK,
                message=success_message,
            )

            return response

        except grpc.RpcError as e:

            if e.code() == grpc.StatusCode.ALREADY_EXISTS:

                response = CreateBusinessResponse(
                    code=e.code(),
                    message=e.details(),
                )

            return response
