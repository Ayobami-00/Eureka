from sqlmodel import Field

from src.model.base_model import BaseModel


class Business(BaseModel):
    
    created_by: str = Field()
    name: str = Field()
    description: str = Field(default="")
    long_address: str = Field()
    latitude: float = Field()
    longitude: float = Field()
