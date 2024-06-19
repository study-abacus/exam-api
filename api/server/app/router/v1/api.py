from fastapi import APIRouter


from app.router.v1.controllers import (
    championship,
    examination,
    profile,
    admit_card,
    order
)


api_router = APIRouter()    


api_router.include_router(championship.router, prefix="/championships", tags=["Championship"])
api_router.include_router(examination.router, prefix="/examination", tags=["Examination"])
api_router.include_router(profile.router, prefix="/profile", tags=["Profile"])
api_router.include_router(admit_card.router, prefix="/admit_card", tags=["AdmitCard"])
api_router.include_router(order.router, prefix="/order", tags=["Order"])


