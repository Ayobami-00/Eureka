import grpc
from dependency_injector.wiring import Provide, inject

from src.protos.business_pb2_grpc import BusinessServiceServicer
from src.protos.business_pb2 import CreateBusinessRequest, CreateBusinessResponse, Business

from src.usecase import BusinessUsecase
from src.core.container import Container
from src.utils.proto_message_to_schema import proto_message_to_schema
from src.utils.gapi_response import gapi_response


class BusinessService(BusinessServiceServicer):
    @inject
    async def Create(self, request: CreateBusinessRequest, context: grpc.aio.ServicerContext, usecase: BusinessUsecase = Provide[Container.business_usecase]) -> CreateBusinessResponse:

        schema = proto_message_to_schema(request)

        return gapi_response(CreateBusinessResponse(), getattr(usecase, "add"), schema, context, "Business Created Successfully")
