from sqlalchemy.orm import Session
from app import models

def get_order_by_reference(db: Session, reference: str):
    return db.query(models.Order).filter(models.Order.reference == reference).first()

def create_order(db: Session, reference: str, amount: int, qr_string: str = None, qr_image_path: str = None):
    order = models.Order(reference=reference, amount=amount, qr_string=qr_string, qr_image_path=qr_image_path)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

def update_order_paid(db: Session, reference: str, settlement_reference: str = None):
    order = get_order_by_reference(db, reference)
    if not order:
        return None
    order.status = "PAID"
    if settlement_reference:
        order.settlement_reference = settlement_reference
    db.commit()
    db.refresh(order)
    return order
