from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.schemas.order import OrderCreate, StatusUpdate
from app.services.order_service import (
    create_order_service,
    list_orders_service,
    update_status_service,
    get_dashboard_service,
    get_order_history_service
)

router = APIRouter()

@router.post("/orders", status_code=201)
def create_order(order: OrderCreate):
    return create_order_service(order)

@router.get("/orders")
def list_orders(
    status: Optional[str] = Query(None, description="Filter by status"),
    search: Optional[str] = Query(None, description="Search by name or phone")
):
    return list_orders_service(status, search)

@router.patch("/orders/{order_id}/status")
def update_status(order_id: str, update: StatusUpdate):
    result = update_status_service(order_id, update)
    if not result:
        raise HTTPException(404, f"Order {order_id} not found")
    return result

@router.get("/dashboard")
def get_dashboard():
    return get_dashboard_service()

@router.get("/orders/{order_id}/history")
def get_order_history(order_id: str):
    result = get_order_history_service(order_id)
    if not result:
        raise HTTPException(404, f"Order {order_id} not found")
    return result
