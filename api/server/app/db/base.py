from app.db.base_class import Base

from app.models.championship import Championship
from app.models.examination import Examination

from app.models.question import Question
from app.models.queschoice import QuesChoice
from app.models.answer import Answer

from app.models.profile import Profile
from app.models.admit_card import AdmitCard

from app.models.question_attempt import QuestionAttempt
from app.models.exam_attempt import ExamAttempt

from sqlalchemy.orm import relationship
def add_relationships(base_class, relationships):
    for rel_name in relationships:
        setattr(
            base_class,
            rel_name,
            relationship(rel_name.split('_')[0], back_populates=rel_name)
        )

# Define the relationship names
relationship_names = [
    'championship_examination',
    'examination_championship',
    'championship_admitcard',
    'admitcard_championship',
    'examination_question',
    'questions_examination',
    'question_queschoice',
    'queschoice_question',
    'question_answer',
    'answer_question',
    'profile_admitcard',
    'admitcard_profile',
    'questionattempt_admitcard',
    'questionattempt_question',
    'examattempt_admitcard',
    'examattempt_examination'
]

# Add relationships to the Base class
add_relationships(Base, relationship_names)