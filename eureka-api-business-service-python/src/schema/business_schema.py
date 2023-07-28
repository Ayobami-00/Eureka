

from typing import Optional
from pydantic import BaseModel


class CreateBusiness(BaseModel):
    created_by: str
    name: str
    description: Optional[str] = None
    long_address: str
    latitude: float
    longitude: float
