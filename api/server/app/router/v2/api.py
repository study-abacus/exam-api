from fastapi import APIRouter


from app.router.v2.controllers import (
    order
)


api_router = APIRouter()    


api_router.include_router(order.router, prefix="/order", tags=["Order"])