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
