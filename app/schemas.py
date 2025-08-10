from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OrderCreate(BaseModel):
    reference: str
    amount: int

class OrderResponse(BaseModel):
    reference: str
    amount: int
    status: str
    qr_string: Optional[str] = None
    qr_image_path: Optional[str] = None
    settlement_reference: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True
