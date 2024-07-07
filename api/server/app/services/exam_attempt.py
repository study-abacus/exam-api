from app.utils.app_exceptions import AppException
from app.services.main import AppService, AppCRUD

from app.utils.service_request import ServiceResult

from app.models.exam_attempt import ExamAttempt

from sqlalchemy import asc, desc, and_
from sqlalchemy.dialects.postgresql import insert
from typing import List, Any , Optional, Union

import logging
import datetime
import json

logger = logging.getLogger(__name__)

class ExamAttemptCRUD(AppCRUD):

    async def get(self, examination_id:int , admit_card_id:int, model = ExamAttempt):
        return self.db.query(model).filter(and_(model.admit_card_id==admit_card_id, model.examination_id == examination_id)).first()


    async def get_create(self, examination_id:int , admit_card_id:int, model = ExamAttempt):
        """
        Get the examination attempt using examination id and admit_card id
        """

        #check in the cache

        exam_attempt = json.loads(self.cache.hget('exam_attempts', f'{admit_card_id}-{examination_id}') or '{}')

        if exam_attempt:
            return ExamAttempt(**exam_attempt)
        
        exam_attempt = await self.get(examination_id, admit_card_id)
        
        if not exam_attempt:
            exam_attempt = ExamAttempt(
                admit_card_id = admit_card_id,
                examination_id = examination_id,
                is_submitted = False,
                INS_DT = datetime.datetime.now()
            )
            self.db.add(exam_attempt)
            self.db.commit()
            self.db.refresh(exam_attempt)
        
        self.cache.hset('exam_attempts', f'{admit_card_id}-{examination_id}', json.dumps(exam_attempt.as_dict() , default= str))

        return exam_attempt
    
    async def update(self, examination_id:int , admit_card_id:int, model = ExamAttempt):
        """
        Update the ExamAttempt
        """

        exam_attempt = await self.get(examination_id, admit_card_id)
        exam_attempt.is_submitted =  True
        exam_attempt.END_DT = datetime.datetime.now()
        self.db.commit()
        self.db.refresh(exam_attempt)

        self.cache.hdel('exam_attempts', f'{admit_card_id}-{examination_id}')

        return exam_attempt

