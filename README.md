Ques Attempt:
id
admit_card : FK
question : FK
answer 
INS_DT
UPS_DT

Examination:
description : TEXT

ACTION:

User comes onto portal

## /authenticate -> JWT [EXAM ID]

## /examination/id [cache]
    ### description


[COUNTDOWN OVER]

## middleware 
    /questions

    1. verify exam_id-> admit_card
    2. cache(exam_id)
    3. exam.starttime >= utc.now()


## [GET] questions?{exam_id} --> [AUTHENTICATED]
    1. cache(exam_id -> questions)
    2. get call 

    Response : 
    List[Question]


## [GET] questions?{question_id}?{exam-id} --> [AUTHENTICATE]
    1. cache(exam_id -> questions)
    2. get(questions using exam_id, ans)

    Response :  {
        question : str
        question options: str
        user_answer: str
    }

## [PUT] questions?{question_id}?{exam_id} --> [AUTHENTICATE]
    1. cache (exam_id)
    2. verify question_id in exam_id
    3. upsert the question_attempt

    Response :  {
        question : str
        question options: str
        user_answer: str
    }



    

