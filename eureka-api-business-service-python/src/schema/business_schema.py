

from typing import Optional
from pydantic import BaseModel


class CreateBusiness(BaseModel):
    created_by: str
    name: str
    description: Optional[str] = None
    long_address: str
    latitude: float
    longitude: float



class FetchAllBusiness(BaseModel):
    page: int
    page_size: int

class FetchBusinessById(BaseModel):
    id: str


class UpdateBusiness(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    long_address: str
    latitude: float
    longitude: float


class DeleteBusinessById(BaseModel):
    id: str