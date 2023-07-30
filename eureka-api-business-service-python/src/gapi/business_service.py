import grpc
from dependency_injector.wiring import Provide, inject

from src.protos.business_pb2_grpc import BusinessServiceServicer
from src.protos.business_pb2 import CreateBusinessRequest, CreateBusinessResponse, Business, FetchBusinessByIdRequest, FetchBusinessByIdResponse, FetchAllBusinessRequest, FetchAllBusinessResponse, UpdateBusinessRequest, UpdateBusinessResponse, DeleteBusinessRequest, DeleteBusinessResponse

from src.usecase import BusinessUsecase
from src.core.container import Container
from src.utils.proto_message_to_schema import proto_message_to_schema
from src.utils.gapi_response import gapi_response


class BusinessService(BusinessServiceServicer):
    @inject
    async def FetchAll(self, request: FetchAllBusinessRequest, context: grpc.aio.ServicerContext, usecase: BusinessUsecase = Provide[Container.business_usecase]) -> FetchAllBusinessResponse:

        schema = proto_message_to_schema(request)

        return gapi_response(FetchAllBusinessResponse(), usecase.get_list, schema, context, "Business Fetched Successfully")

    @inject
    async def Create(self, request: CreateBusinessRequest, context: grpc.aio.ServicerContext, usecase: BusinessUsecase = Provide[Container.business_usecase]) -> CreateBusinessResponse:

        schema = proto_message_to_schema(request)

        return gapi_response(CreateBusinessResponse(), usecase.add, schema, context, "Business Created Successfully")

    @inject
    async def FetchById(self, request: FetchBusinessByIdRequest, context: grpc.aio.ServicerContext, usecase: BusinessUsecase = Provide[Container.business_usecase]) -> FetchBusinessByIdResponse:

        schema = proto_message_to_schema(request)

        return gapi_response(FetchBusinessByIdResponse(), usecase.get_by_id, schema, context, "Business Fetched Successfully", extra_fields={"id": schema.id})
    
    
    @inject
    async def Update(self, request: UpdateBusinessRequest, context: grpc.aio.ServicerContext, usecase: BusinessUsecase = Provide[Container.business_usecase]) -> UpdateBusinessResponse:

        schema = proto_message_to_schema(request)

        return gapi_response(UpdateBusinessResponse(), usecase.patch, schema, context, "Business Updated Successfully", extra_fields={"id": schema.id})
    
    @inject
    async def DeleteById(self, request: DeleteBusinessRequest, context: grpc.aio.ServicerContext, usecase: BusinessUsecase = Provide[Container.business_usecase]) -> UpdateBusinessResponse:

        schema = proto_message_to_schema(request)

        return gapi_response(DeleteBusinessResponse(), usecase.remove_by_id, schema, context, "Business Deleted Successfully", extra_fields={"id": schema.id})
    
    
