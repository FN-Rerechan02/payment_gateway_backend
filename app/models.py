from sqlalchemy import Column, Integer, String, DateTime, Numeric, Text
from sqlalchemy.sql import func
from app.db import Base

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    reference = Column(String(128), unique=True, index=True, nullable=False)  # reference / order id
    amount = Column(Integer, nullable=False)
    status = Column(String(20), default="UNPAID")  # UNPAID / PAID / FAILED
    qr_string = Column(Text, nullable=True)
    qr_image_path = Column(String(256), nullable=True)  # optional: saved image path
    settlement_reference = Column(String(128), nullable=True)  # backend provider reference
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    note = Column(Text, nullable=True)
