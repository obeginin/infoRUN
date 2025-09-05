
from utils.config import settings

from utils import errors,general
from Service.Database import get_db
from Service.Models import Student
from Service.Crud.auth import get_current_student, permission_required
from Service.producer import send_log

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


# /api/tasks/variants  (GET) @
''' Получить список вариантов'''
@variant_router.get("")
def read_tasks_id(db: Session = Depends(get_db)):
    result = db.execute(text(f"select VariantID, VariantName from Variants order by VariantName")).fetchall()
    variants = [dict(row._mapping) for row in result]
    return variants


# /api/tasks/exec/{VariantID}
'''вызов хранимки с вариантом'''
@variant_router.get("/exec/{VariantID}/{StudentID}", summary="роут с вызовом хранимой процедуры")
def read_tasks_of_variant (VariantID: int, StudentID: int, db: Session = Depends(get_db)):
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
