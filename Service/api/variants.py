
from utils.config import settings

from utils import errors,general
from Service.dependencies import get_db
from Service.Models import Student
from Service.Crud.auth import get_current_student, permission_required
from Service.producer import send_log
from Service.Schemas import variants as variants_schemas
from Service.Crud import variants as variants_crud

from fastapi import APIRouter, Depends, Request, Form, UploadFile, File, Query, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse
from typing import List
from pathlib import Path
from typing import Dict, Optional
import shutil
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import logging

# api\variants.py
''' Маршруты и Эндпоинты'''

load_dotenv()
logger = logging.getLogger(__name__)



variant_router = APIRouter(prefix="/api/variants", tags=["variants"])


# /api/variants  (GET) @
''' Получить список вариантов'''
@variant_router.get(
    "",                    # добавляем префикс к адресу
    response_model=variants_schemas.VariantsListResponse,   # указываем какой схеме должны соответствовать данные
    summary="Получить список вариантов",
    description="""
        Если параметры не переданы, возвращаются все варианты по всем предметам.  
        **subjectID** и **variantID** передается как Query-параметр   
                "`/api/variants` — все варианты"  
                "`/api/variants?variantID=10` — конкретный вариант с variants ID =10 (subjectID в этом случае не нужен"  
                "`/api/variants?subjectID=10` — все варианты для указанного предмета с subject ID 10"  
                так же необходимо передавать в заголовке **токен** пользователя
        """
)
def read_varinatns_subject(
        db: Session = Depends(get_db),
        variantID: int | None = Query(default=None),
        subjectID: int | None = Query(default=None),         # передаем id предмета (не обязательно, тогда выйдут категории всех предметов)
        current_student = Depends(get_current_student)):     # получаем текущего студента по токену

    if subjectID is None and variantID is None:
        variants = variants_crud.get_all_variants(db)  # функция без фильтрации
    elif not (variantID is None):
        variants = variants_crud.get_all_variants(db, variantID=variantID)
    else:
        variants = variants_crud.get_all_variants(db, subjectID=subjectID)
    logger.warning(f"variants:{variants}")

    if not variants:
        logger.warning(f"Не найдено вариантов для предмета id= {subjectID} и варианта id={variantID}, Возвращаем пустой список")
        return {
            "message": f"Не найдено вариантов для предмета id= {subjectID} и варианта id={variantID}, Возвращаем пустой список",
            "variants": []
        }

    count = len(variants)
    send_log(
        StudentID=None,  # Или 0
        StudentLogin=current_student.Login,
        action="GetVariants",
        details={
            "DescriptionEvent": f"Получение вариантов с предметом id:{subjectID}",
            "VariantID": variantID,
            "SubjectID": subjectID,
            "variants": count
        }
    )
    logger.info(f"Пользователь {current_student.Login} запросил список вариантов для предмета с id:{subjectID} и варианта id={variantID}")
    return {
        "message": f"Найдено вариантов: {count}",
        "count": count,
        "variants": variants
    }

# /api/tasks/exec/{VariantID}
'''вызов хранимки с вариантом'''
@variant_router.get("/exec/{VariantID}/{StudentID}", summary="вызовом хранимой процедуры", description="данный роут возвращает цельный вариант задач определенного студента")
def read_tasks_of_variant (VariantID: int, StudentID: int, db: Session = Depends(get_db), current_student = Depends(get_current_student)):
    query = text("EXEC dbo.GetStudentsTasks @VariantID =:VariantID, @StudentID =:StudentID")
    result = db.execute(query, {"VariantID": VariantID, "StudentID": StudentID}).fetchall()
    print(result)
    if not result:
            raise HTTPException(status_code=404, detail=f"нет задач с варианте с ID {VariantID}")
    subtasks = [dict(row._mapping) for row in result]
    return jsonable_encoder(subtasks)

# /api/variants/check_answers
@variant_router.post("/check_answers", summary="роут который проверяет ответы пользователя для целого вараинта",
                      description="передаем словарь с ответами на все задангия пользователя в виде строк")
def check_answers(user_answers: Dict[int, Optional[str]], db: Session = Depends(get_db)):
    results = []
    print(user_answers)
    for i, (subtask_id, user_answer) in enumerate(user_answers.items()):
        if user_answer is None:
            results.append({
                "SubTaskID": subtask_id,
                "IsCorrect": False,
                "CorrectAnswer": "...",  # можно не указывать
                "UserAnswer": None
            })
            continue
        correct = db.execute(
            text("SELECT Answer FROM SubTasks WHERE SubTaskID = :id"),
            {"id": subtask_id}
        ).scalar()

        is_correct = str(user_answer).strip().lower() == str(correct).strip().lower()
        #print(i, subtask_id, correct, is_correct)
        results.append({
            "SubTaskID": subtask_id,
            "UserAnswer": user_answer,
            "CorrectAnswer": correct,
            "IsCorrect": is_correct
        })
    print(results)
    return {
        "results": results,
        "correct_count": sum(r["IsCorrect"] for r in results),
        "total": len(results),
        "message": f"Верно: {sum(r['IsCorrect'] for r in results)} из {len(results)}"
    }
