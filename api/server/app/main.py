from pathlib import Path
import os
import logging
import time
import random
import string
from logging.config import fileConfig


from fastapi import FastAPI, APIRouter, Request, Depends,Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


from app.utils.request_exceptions import (
    http_exception_handler,
    request_validation_exception_handler,
)
from app.utils.app_exceptions import app_exception_handler
from app.utils.app_exceptions import AppExceptionCase
from app.utils.jwt import decode_jwt_token
from app.middleware.exam_attempt import VerifyQuestionAttemptJWTMiddleware
from app.router.v1.api import api_router
from app.router.v2.api import api_router as api_v2_router
from app.router.admin.api import api_router as admin_router


from app.core.config import settings


root_router = APIRouter()
app = FastAPI(title="StudyAbacus APIs", openapi_url=f"{settings.API_V1_STR}/openapi.json", docs_url="/docs", redoc_url="/redoc")


# setup logger
fileConfig('./app/logging.conf', disable_existing_loggers=False)


# get root logger
logger = logging.getLogger(__name__)  


origins = [
    "http://0.0.0.0:3000",
    "http://localhost:3000",
    'https://examination.studyabacus.com',
    "*"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.add_middleware(VerifyQuestionAttemptJWTMiddleware)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()
   
    response = await call_next(request)
   
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")
   
    return response



#set up Exception handler
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, e):
    return await http_exception_handler(request, e)




@app.exception_handler(RequestValidationError)
async def custom_validation_exception_handler(request, e):
    return await request_validation_exception_handler(request, e)




@app.exception_handler(AppExceptionCase)
async def custom_app_exception_handler(request, e):
    return await app_exception_handler(request, e)


@root_router.get("/", status_code=200)
def root():
    logger.info("ISCA:: API Layer is up and running.")
    return "ISCA:: API Layer is up and running."


@root_router.get("/health", status_code=200)
def health():
    logger.info("StudyAbacus:: API Layer is healthy.")
    return "StudyAbacus:: API Layer is healthy."


@root_router.get("/favicon.ico", status_code=200)
def favicon():
    return Response(content="", media_type="image/png")


app.include_router(root_router)
app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(api_v2_router, prefix=settings.API_V2_STR)
# app.include_router(admin_router, prefix=settings.ADMIN_STR)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, log_level="info", reload = False)



