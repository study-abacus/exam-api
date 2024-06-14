from fastapi import APIRouter


from router.v1.controllers import (
    championship,
    examination,
    question,
    queschoice,
    answer,
    profile,
    admit_card
)


api_router = APIRouter()    


api_router.include_router(championship.router, prefix="/championships", tags=["Championship"])
# api_router.include_router(examination.router, prefix="/examination", tags=["Examination"])
# api_router.include_router(question.router, prefix="/question", tags=["Question"])
# api_router.include_router(queschoice.router, prefix="/queschoice", tags=["QuesChoice"])
# api_router.include_router(answer.router, prefix="/answer", tags=["Answer"])
# api_router.include_router(profile.router, prefix="/profile", tags=["Profile"])
# api_router.include_router(admit_card.router, prefix="/admit_card", tags=["AdmitCard"])


