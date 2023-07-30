import grpc
from src.model.business import business_to_dict
from src.protos.business_pb2 import *


def gapi_response(message, function_call, schema, context, success_message, extra_fields=None):

    if type(message) == FetchAllBusinessResponse:

        try:

            result = function_call(schema, context)

            result["founds"] = [business_to_dict(
                business) for business in result["founds"]]

            response = FetchAllBusinessResponse(
                code=grpc.StatusCode.OK.value[0],
                message=success_message,
                data=result
            )

            return response

        except grpc.RpcError as e:

            response = FetchAllBusinessResponse(
                code=e.code().value[0],
                message=e.details(),
            )

            return response

    elif type(message) == CreateBusinessResponse:

        try:

            result = function_call(schema, context)

            response = CreateBusinessResponse(
                code=grpc.StatusCode.OK.value[0],
                message=success_message,
            )

            return response

        except grpc.RpcError as e:

            response = CreateBusinessResponse(
                code=e.code().value[0],
                message=e.details(),
            )

            return response

    elif type(message) == FetchBusinessByIdResponse:

        try:

            result = function_call(extra_fields.get("id"), context)

            response = FetchBusinessByIdResponse(
                code=grpc.StatusCode.OK.value[0],
                message=success_message,
                business=business_to_dict(result)
            )

            return response

        except grpc.RpcError as e:

            response = FetchBusinessByIdResponse(
                code=e.code().value[0],
                message=e.details(),
            )

            return response

    elif type(message) == UpdateBusinessResponse:

        try:

            result = function_call(extra_fields.get("id"), schema, context)

            response = UpdateBusinessResponse(
                code=grpc.StatusCode.OK.value[0],
                message=success_message,
                business=business_to_dict(result)
            )

            return response

        except grpc.RpcError as e:

            response = UpdateBusinessResponse(
                code=e.code().value[0],
                message=e.details(),
            )

            return response
        
    
    elif type(message) == DeleteBusinessResponse:

        try:

            result = function_call(extra_fields.get("id"), context)

            response = DeleteBusinessResponse(
                code=grpc.StatusCode.OK.value[0],
                message=success_message
            )

            return response

        except grpc.RpcError as e:

            response = DeleteBusinessResponse(
                code=e.code().value[0],
                message=e.details(),
            )

            return response
