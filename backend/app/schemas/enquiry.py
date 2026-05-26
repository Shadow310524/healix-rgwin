from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr

class EnquiryBase(BaseModel):
    name: str
    email: EmailStr
    message: str

class EnquiryCreate(EnquiryBase):
    pass

class Enquiry(EnquiryBase):
    id: int
    created_at: datetime

    model_config = {'from_attributes': True}
