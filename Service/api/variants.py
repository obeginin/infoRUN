
from utils.config import settings

from utils import errors,general
from Service.Database import get_db
from Service.Models import Student
from Service.Crud.auth import get_current_student, permission_required
from Service.Crud import variants as variants_crud
from Service.Schemas import variants as variants_schema
from Service.producer import send_log

from fastapi import APIRouter, Depends, Request, Form, UploadFile, File, Query, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
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

# TODO переведен на асинхронный postgres

variant_router = APIRouter(prefix="/api/variants", tags=["variants"])


# /api/tasks/variants  (GET) @
''' Получить список вариантов'''
@variant_router.get("",
                    operation_id = 'Variants',
                    summary="Получить список вариантов",
                    description="""Если передан параметр **subject_id**, то возвращаются варианты только для указанного предмета.  
                            Если параметр не передан, возвращаются варианты по всем предметам.  
                            **subjectID** передается как Query-параметр   
                                    "`/api/variants` — все варианты"  
                                    "`/api/variants?subjectID=10` — варианты для предмета с subject ID 10"  
                                    так же необходимо передавать в заголовке **токен** пользователя
                            """
                    )
async def read_variants(
        subject_id: int | None = Query(None, description="ID предмета для фильтрации"),
        db: AsyncSession = Depends(get_db),
        current_student=Depends(permission_required("view_variants"))):
    logger.info(f"Пользователь {current_student.Login} запросил список всех вариантов")
    variants = await variants_crud.get_variants(db, subject_id=subject_id)
    return {"count": len(variants), "variants": variants}

@variant_router.get("/{variant_id}",operation_id = 'VariantsVariantID', summary="Получить вариант по его variant_id")
async def read_variant_by_id(
    variant_id: int,
    db: AsyncSession = Depends(get_db),
    current_student=Depends(permission_required("view_variants"))
):
    logger.info(f"Пользователь {current_student.Login} запросил вариант с variant_id={variant_id}")
    variant = await variants_crud.get_variants(db, variant_id=variant_id)
    if not variant:
        logger.warning(f"Вариант с variant_id={variant_id} не найден")
        raise errors.not_found(message=f"Вариант с variant_id={variant_id} не найден")
    return variant[0]


# TODO передалать но новое
# /api/variants/exec/{VariantID}
'''вызов хранимки с вариантом'''
@variant_router.get("/exec/{VariantID}/{StudentID}",operation_id = 'VariantsExecVariantIDStudentID', summary="роут с вызовом хранимой процедуры")
async def read_tasks_of_variant (VariantID: int, StudentID: int, db: AsyncSession = Depends(get_db)):
    query = text("EXEC dbo.GetStudentsTasks @VariantID =:VariantID, @StudentID =:StudentID")
    result = db.execute(query, {"VariantID": VariantID, "StudentID": StudentID}).fetchall()
    print(result)
    if not result:
            raise HTTPException(status_code=404, detail=f"нет задач с варианте с ID {VariantID}")
    subtasks = [dict(row._mapping) for row in result]
    return jsonable_encoder(subtasks)

# TODO передалать но новое
# /api/variants/check_answers
#@variant_router.post("/check_answers", summary="роут который проверяет ответы пользователя для целого вараинта",
#                      description="передаем словарь с ответами на все задангия пользователя в виде строк")
async def check_answers(user_answers: Dict[int, Optional[str]], db: AsyncSession = Depends(get_db)):
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
