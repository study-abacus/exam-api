from fastapi import APIRouter


from router.v1.controllers import (
    championship
)


api_router = APIRouter()    


api_router.include_router(championship.router, prefix="/championship", tags=["Championship"])


