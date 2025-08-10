from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app import db, crud, schemas, config
from app.db import SessionLocal, init_db
from app.services.qr_service import generate_qr_for_amount
from app.services.settlement_service import settlement_service
from app.utils import require_api_key
import uuid
import logging

app = FastAPI(title="QRIS Payment Gateway Backend")

# initialize DB
init_db()

# dependency
def get_db():
    db_sess = SessionLocal()
    try:
        yield db_sess
    finally:
        db_sess.close()

@app.post("/orders", response_model=schemas.OrderResponse, dependencies=[Depends(require_api_key)])
def create_order(payload: schemas.OrderCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # idempotency: if reference exists, return existing
    existing = crud.get_order_by_reference(db, payload.reference)
    if existing:
        return existing

    # generate qr (sync) and save order
    qr_string, img_path = generate_qr_for_amount(payload.amount)
    order = crud.create_order(db, payload.reference, payload.amount, qr_string, img_path)

    # optionally start background check later, or wait for client to poll /webhook
    # background_tasks.add_task(poll_settlement_for_order, payload.reference, payload.amount)

    return order

@app.get("/orders/{reference}", response_model=schemas.OrderResponse, dependencies=[Depends(require_api_key)])
def get_order(reference: str, db: Session = Depends(get_db)):
    order = crud.get_order_by_reference(db, reference)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.post("/orders/{reference}/check", response_model=schemas.OrderResponse, dependencies=[Depends(require_api_key)])
def check_order(reference: str, db: Session = Depends(get_db)):
    order = crud.get_order_by_reference(db, reference)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    result = settlement_service.check_payment(order.amount)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error", "Check failed"))

    # If paid, update order
    data = result.get("data", {})
    if data.get("status") == "PAID":
        crud.update_order_paid(db, reference, settlement_reference=data.get("reference"))
    order = crud.get_order_by_reference(db, reference)
    return order

@app.post("/webhook/settlement", dependencies=[Depends(require_api_key)])
def settlement_webhook(payload: dict, db: Session = Depends(get_db)):
    """
    Optional webhook endpoint to accept callbacks from settlement provider.
    payload should contain something like: {'reference': '...', 'amount': 10000, 'status': 'PAID', ...}
    """
    try:
        ref = payload.get("reference")
        status = payload.get("status")
        amount = int(payload.get("amount", 0))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid payload")

    order = crud.get_order_by_reference(db, ref)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if status == "PAID" and amount == order.amount:
        crud.update_order_paid(db, ref, settlement_reference=payload.get("settlement_id"))
        return {"success": True}
    return {"success": False, "reason": "no update performed"}

@app.get("/health")
def health():
    return {"status": "ok"}
