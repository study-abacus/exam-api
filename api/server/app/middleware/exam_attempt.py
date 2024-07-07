import pytz
from fastapi import FastAPI, Request, HTTPException
from datetime import datetime
from app.utils.jwt import decode_jwt_token
from app.services.examination import ExaminationCRUD 
from app.router.deps import get_cache,get_session
from app.services.examination import ExaminationCRUD
from starlette.middleware.base import BaseHTTPMiddleware

class VerifyQuestionAttemptJWTMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        
        if "/questions" in request.url.path:
            token = request.headers.get("Authorization")
            if not token:
                raise HTTPException(status_code=401, detail="JWT token missing")
            
            _, jwt_token  = token.split()

            try:
                payload = decode_jwt_token(jwt_token)
            except Exception as e:
                raise HTTPException(status_code=401, detail=f"JWT token invalid: {e}")
            
            # print(f'payload {payload}')
            

            exam_ids = payload["examination_ids"]
            if not exam_ids:
                raise HTTPException(status_code=401, detail="Invalid JWT payload: exam_id missing")

            query_exam_id = request.query_params.get("examination_id")
            if not query_exam_id:
                raise HTTPException(status_code=400, detail="Query parameter exam_id missing")

            if query_exam_id in exam_ids:
                raise HTTPException(status_code=403, detail="Exam ID mismatch")

            cache = next(get_cache())

            exam_detail = cache.get(query_exam_id)
            if not exam_detail:
                raise HTTPException(status_code=404, detail="Exam not found")
            
            if datetime.now(pytz.utc) < exam_detail.start_time:
                raise HTTPException(status_code=403, detail="Examination has not started yet")

        response = await call_next(request)
        return response