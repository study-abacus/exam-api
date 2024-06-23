from fastapi import APIRouter, Depends, HTTPException
from typing import List, Any , Optional, Union
from sqlalchemy.orm import Session

from app.utils.service_request import handle_result
from app.schemas.order import OrderBase, OrderCreate, OrderAmount,OrderCapture
from app.schemas.admit_card import AdmitCard
from app.services.payments.razorpay_order import RazorPayOrderService

from app.router import deps
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=OrderBase)
async def create_order(order: OrderCreate, db: Session = Depends(deps.get_session),  cache = Depends(deps.get_cache)):
    """
    Create new order.
    """
    result = await RazorPayOrderService(db, cache).create_order(order)
    return handle_result(result)

@router.post("/calculate/", response_model=OrderAmount)
async def calculate_order(order: OrderCreate, db: Session = Depends(deps.get_session)):
    """
    Calculate order.
    """
    result = await RazorPayOrderService(db).calculate_order(order)
    return handle_result(result)

@router.post("/{order_id}/capture/", response_model=AdmitCard)
async def capture_order(order_id: str, order_details :OrderCapture, db: Session = Depends(deps.get_session), cache = Depends(deps.get_cache)):
    """
    Capture order.
    """
    result = await RazorPayOrderService(db, cache).capture_order(order_id, order_details)
    return handle_result(result)