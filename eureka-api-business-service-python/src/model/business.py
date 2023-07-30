from sqlmodel import Field

from src.model.base_model import BaseModel

from google.protobuf.timestamp_pb2 import Timestamp


class Business(BaseModel, table=True):
    
    created_by: str = Field()
    name: str = Field()
    description: str = Field(default="")
    long_address: str = Field()
    latitude: float = Field()
    longitude: float = Field()


def business_to_dict(business):

    updated_at = int(business.updated_at.timestamp())
    created_at = int(business.created_at.timestamp())

    # Create a dictionary representation of the Business object
    business_dict = {
        'name': business.name,
        'updated_at': updated_at,
        'id': business.id,
        'long_address': business.long_address,
        'longitude': business.longitude,
        'created_by': business.created_by,
        'created_at': created_at,
        'description': business.description,
        'latitude': business.latitude,
    }

    return business_dict