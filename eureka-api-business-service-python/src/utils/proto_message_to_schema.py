from src.schema import *

from src.protos.business_pb2 import *


def proto_message_to_schema(message):

    if type(message) == CreateBusinessRequest:

        schema = CreateBusiness(
            created_by=message.created_by,
            name=message.name,
            description=message.description,
            long_address=message.long_address,
            latitude=message.latitude,
            longitude=message.longitude,

        )

        return schema
    
    elif type(message) == FetchAllBusinessRequest:

        schema = FetchAllBusiness(
            page=message.page,
            page_size=message.page_size

        )

        return schema
    
    elif type(message) == FetchBusinessByIdRequest:

        schema = FetchBusinessById(
            id=message.id,

        )

        return schema
    

    elif type(message) == UpdateBusinessRequest:

        schema = UpdateBusiness(
            id=message.business.id,
            name=message.business.name,
            description=message.business.description,
            long_address=message.business.long_address,
            latitude=message.business.latitude,
            longitude=message.business.longitude,

        )

        return schema
    
    elif type(message) == DeleteBusinessRequest:

        schema = DeleteBusinessById(
            id=message.id,

        )

        return schema
    
    


