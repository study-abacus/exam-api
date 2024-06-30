from fastapi import FastAPI, Request, HTTPException
from datetime import datetime
from app.utils.jwt import decode_jwt_token
from app.services.examination import ExaminationCRUD 
from app.router.deps import get_cache

class VerifyQuestionAttemptJWTMiddleware:
    def __init__(self, app: FastAPI):
        self.app = app

    async def __call__(self, request: Request, call_next):
        if request.url.path == "/questions":
            token = request.headers.get("Authorization")
            if not token:
                raise HTTPException(status_code=403, detail="JWT token missing")

            try:
                payload = decode_jwt_token(token)
            except Exception as e:
                raise HTTPException(status_code=403, detail=f"JWT token invalid: {e}")
            

            exam_ids = payload["examination_ids"]
            if not exam_ids:
                raise HTTPException(status_code=400, detail="Invalid JWT payload: exam_id missing")

            query_exam_id = request.query_params.get("exam_id")
            if not query_exam_id:
                raise HTTPException(status_code=400, detail="Query parameter exam_id missing")

            if query_exam_id in exam_ids:
                raise HTTPException(status_code=403, detail="Exam ID mismatch")

            cache = get_cache()
            exam_detail = cache.get(query_exam_id)
            if not exam_detail:
                raise HTTPException(status_code=404, detail="Exam not found")

            if datetime.now() < exam_detail.start_time:
                raise HTTPException(status_code=403, detail="Examination has not started yet")

        response = await call_next(request)
        return response