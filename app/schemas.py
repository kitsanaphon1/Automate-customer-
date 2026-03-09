from pydantic import BaseModel
from typing import List, Optional

class CustomerBase(BaseModel):
    customer_code: str
    name: str
    email: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    id: int
    class Config:
        from_attributes = True