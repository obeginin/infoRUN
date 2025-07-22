from Service.config import UPLOAD_IMAGE_DIR, UPLOAD_SOLUTION_DIR, UPLOAD_FILES_DIR, UPLOAD_STUDENTS_IMAGE_DIR, TEMPLATES_DIR
from Service.Schemas.students import StudentTaskRead,StudentTaskDetails, AnswerInput, SolutionInput, StudentTasksQueryParams
from Service.Crud import students
from Service.Routers.tasks import get_files_for_subtask
from Service.dependencies import get_db  # Зависимость для подключения к базе данных
from Service.Crud.auth import get_current_student, verify_password
from Service.Schemas.auth import StudentAuth, StudentOut
from fastapi import APIRouter, Depends, Request, Query, Form,  UploadFile, File
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Literal
from fastapi.responses import RedirectResponse
from starlette.responses import JSONResponse
import shutil
from typing import Optional
from sqlalchemy import text
from fastapi.encoders import jsonable_encoder
import logging
logger = logging.getLogger(__name__) # создание логгера для текущего модуля

# Routers\Students.py
''' Маршруты и Эндпоинты'''



students_router = APIRouter(prefix="/api/students", tags=["students"])
students_subtasks_router = APIRouter(prefix="/api/students_subtasks", tags=["students_subtasks"])
templates = Jinja2Templates(directory=TEMPLATES_DIR)


"""API"""
# /api/students
''' Эндпоинт: Получить список студентов'''
@students_router.get(
    "",
    response_model=list[StudentOut],
    summary="Получить список студентов в формате JSON",
)
def read_all_students(db: Session = Depends(get_db)):
    return students.get_all_students(db)

# /students/api{student_id}
''' Эндпоинт: Получить студента по id (/students/{student_id})'''
@students_router.get("/api/{student_id}", response_model=StudentAuth, summary="Получить студента по его ID")
def read_student_id(student_id: int, db: Session = Depends(get_db)):
    return students.get_student_id(db, student_id)

# /students/{value}
# !!! Полезный роут, но пока не используем!
''' Эндпоинт: Получить пользователей по параметру 
@students_router.get("/{value}", response_model=list[StudentAuth], summary="Получить студента по выбранному полю")
def read_student_by_field(
        value: str,
        #by: str = 'id', # значение по умолчанию
        by: Literal["id", "login"] = Query("id", description="Поле для поиска: 'id' или 'login'"),
        db: Session = Depends(get_db)):
    return students.get_student_by_field(db, value, by)

'''

# /api/students_subtasks
'''Эндпоинт для получения всех подзадач всех студентов'''
@students_subtasks_router.get("", response_model=list[StudentTaskRead], summary="роут с получением всех задач всех студентов")
def read_all_students_subtasks(db: Session = Depends(get_db)):
    return students.get_all_students_tasks(db)

# /api/students_subtasks/{student_id}
'''Эндпоинт для получения всех подзадач студента по его student_id
@students_subtasks_router.get("/{student_id}", response_model=list[StudentTaskRead], summary="роут с получением всех задач (список) студента по его id")
def read_student_all_subtasks(student_id: int, db: Session = Depends(get_db)):
    return students.get_student_all_tasks(db, student_id)
'''
# /api/students_subtasks/{StudentID}/{SubTasksID}
'''Эндпоинт для получения задачи студента по его student_id и номеру SubTasksID'''
@students_subtasks_router.get("/{student_id}/{SubTasksID}", response_model=StudentTaskDetails, summary="роут с получением данных о задаче студента по StudentTaskID")
def read_task_student( StudentTaskID: int, db: Session = Depends(get_db)):
    #return students.get_task_student(db, student_id, SubTasksID)
    return students.Get_Student_TaskDetails_By_ID(db, StudentTaskID)


# /api/students_subtasks/{StudentID}
@students_subtasks_router.get("/{StudentID}", response_model=list[StudentTaskDetails],
                              summary="роут с получением списка задач студента по StudentID",
                              description="""В качестве фильтров передаются параметры  
                                          CompletionStatus - Статус выполнения  
                                          SubjectID - 
                                          TaskID - ID категории 
                                          VariantID - ID варианта
                                          SortColumn - Колонка для сортировки
                                          SortDirection - возрастанию/убыванию
                                          """)
def read_tasks_student( StudentID: int,
                        filters: StudentTasksQueryParams = Depends(),
                       db: Session = Depends(get_db)):
    return students.get_students_all_tasks(
        db,
        StudentID=StudentID,
        CompletionStatus=filters.CompletionStatus,
        #SubjectID=filters.SubjectID,
        TaskID=filters.TaskID,
        VariantID=filters.VariantID,
        SortColumn=filters.SortColumn,
        SortDirection=filters.SortDirection,
        limit=filters.limit,
        offset=filters.offset
    )


'''Проверка ответа пользователя'''
# /api/students_subtasks/check-answer/
@students_subtasks_router.post("/check-answer/")
def check_answer (request: AnswerInput, db: Session = Depends(get_db)):
    logger.info("Запуск проверки ответа")

    # Получаем правильный ответ
    result = text("SELECT Answer FROM SubTasks where SubTaskID = :SubTaskID")
    correct = db.execute(result, {"SubTaskID": request.subtaskId}).fetchone()

    if not correct:
        return {"status": "Error", "detail": "Подзадача не найдена"}
    correct_answer = correct[0]
    logger.info(f"Получаем правильный ответ {correct_answer}")
    # Получаем задание студента
    result = text("SELECT * FROM StudentTasks where SubTaskID = :SubTaskID and StudentID = :StudentID ")
    student_task = db.execute(result, {"SubTaskID": request.subtaskId,"StudentID": request.studentId}).fetchone()

    student_answer = request.student_answer
    if not student_task:
        return {"status": "Error", "detail": "Задание студента не найдено"}
    logger.info(f"Получаем задание студента {student_task}")

    # Проверка ответа
    if correct_answer.strip().lower() == student_answer.strip().lower():
        new_status  = "Выполнено"
        # Обновляем статус
        db.execute(
            text(
                """
                UPDATE StudentTasks
                SET
                    CompletionStatus = :status,
                    StudentAnswer = :student_answer,
                    Attempts = Attempts + 1,
                    CompletionDate = GETDATE(),
                    ModifiedDate = GETDATE(),
                    StartDate = CASE WHEN StartDate IS NULL THEN GETDATE() ELSE StartDate END
                WHERE
                    StudentID = :StudentID AND SubTaskID = :SubTaskID
                """
            ),
            {
                "student_answer": student_answer,
                "status": new_status,
                "StudentID": request.studentId,
                "SubTaskID": request.subtaskId,
            }
        )
    else:
        new_status  = "В процессе"
        logger.info(f"Проверка ответа {new_status}")
        # Обновляем статус
        db.execute(
            text("""UPDATE StudentTasks 
                    SET 
                        CompletionStatus = :status, 
                        StudentAnswer = :student_answer,
                        Attempts = Attempts + 1,
                        ModifiedDate = GETDATE(),
                        StartDate = CASE WHEN StartDate IS NULL THEN GETDATE() ELSE StartDate END
                    WHERE 
                    StudentID = :StudentID AND SubTaskID = :SubTaskID"""),
            {
                "student_answer": student_answer,
                "status": new_status,
                "StudentID": request.studentId,
                "SubTaskID": request.subtaskId
            }
        )

    db.commit()
    return {"status": new_status}



'''Отправка Решения  пользователя'''
# /api/students_subtasks/submit-solution/
@students_subtasks_router.post("/submit-solution/")
async def submit_solution(
    StudentID: int = Form(...),
    SubTaskID: int = Form(...),
    StudentTaskID: int = Form(...),
    StudentSolutionFile: UploadFile | None = File(None),

    db: Session = Depends(get_db),
):
    print(
        f"submit_solution received: ID={StudentID}, SubTaskID={SubTaskID}, StudentTaskID={StudentTaskID}, StudentSolutionFile={StudentSolutionFile}")
    if StudentSolutionFile:
        print(f"File received: filename={StudentSolutionFile.filename}, content_type={StudentSolutionFile.content_type}")
    else:
        print("No file uploaded")
    # ... далее остальной код
    # Логирование
    logger.info(f"Пришло решение от студента {StudentID} по подзадаче {SubTaskID}")

    # Проверим есть ли запись студента и подзадачи
    student_task = db.execute(
        text("SELECT * FROM StudentTasks WHERE StudentID = :StudentID AND SubTaskID = :SubTaskID"),
        {"StudentID": StudentID, "SubTaskID": SubTaskID}
    ).fetchone()
    # Проверим есть ли запись студента и подзадачи
    if not student_task:
        return JSONResponse(status_code=404, content={"status": "Error", "detail": "Задание студента не найдено"})

   # берем TaskID и SubTaskNumber
    result = db.execute(
        text("SELECT TaskID, SubTaskNumber FROM SubTasks WHERE SubTaskID = :SubTaskID"),
        {"SubTaskID": SubTaskID}
    ).mappings().fetchone()

    if result:
        task_id = result["TaskID"]
        subtask_number = result["SubTaskNumber"]

    # Обновим запись решения Студента
    student_solution_path = None
    if StudentSolutionFile and StudentSolutionFile.filename:
        ext = StudentSolutionFile.filename.split('.')[-1]
        # Сохраняем файл решения на диск (папку можно настроить)
        filename = f"taskID_{SubTaskID}_task_{task_id}_sub_{subtask_number}_student_{StudentID}.{ext}"
        filepath = UPLOAD_STUDENTS_IMAGE_DIR / filename
        with filepath.open("wb") as buffer:
            shutil.copyfileobj(StudentSolutionFile.file, buffer)
        student_solution_path = f"Uploads/StudentSolutions/{filename}"
        logger.info(f"Файл решения сохранён по пути: {student_solution_path}")

    # Обновим таблицу StudentTasks
    if student_task:
        # Обновляем
        update_query = """
            UPDATE StudentTasks
            SET SolutionStudentPath = :student_solution_path, ModifiedDate = GETDATE()
            WHERE StudentID = :StudentID AND SubTaskID = :SubTaskID
        """
        db.execute(text(update_query), {
            "student_solution_path": student_solution_path,
            "StudentID": StudentID,
            "SubTaskID": SubTaskID,
        })
    else:
        # Вставляем новую строку
        insert_query = """
            INSERT INTO StudentTasks (StudentID, SubTaskID, SolutionStudentPath, ModifiedDate)
            VALUES (:StudentID, :SubTaskID, :student_solution_path, GETDATE())
        """
        db.execute(text(insert_query), {
            "StudentID": StudentID,
            "SubTaskID": SubTaskID,
            "student_solution_path": student_solution_path,
        })

    db.commit()
    return RedirectResponse(f"/students_subtasks/T/{StudentTaskID}", status_code=303)







"""Старое"""



# /students_subtasks/StudentTask/{StudentID}
'''Возвращем страницу со всеми задачами пользователя
@students_subtasks_router.get("/StudentTask/{StudentID}",  response_class=HTMLResponse)
def read_student_all_subtasks(
        request: Request,
        StudentID: int,
        current_student=Depends(get_current_student_or_redirect),
        db: Session = Depends(get_db)):
    logger.info(f"Вызван роут read_student_all_subtasks с StudentID={StudentID}")
    student_tasks = students.get_student_all_tasks(db, StudentID)
    print(student_tasks)
    return templates.TemplateResponse("Students/StudentTasks.html", {"request": request, "StudentID": StudentID, "tasks": student_tasks, "student": current_student})
'''

# /students_subtasks/StudentTasksByLogin
'''возвращаем страницу со всеми задачами пользователя в личном кабинете по логину из авторизации
@students_subtasks_router.get("/StudentTasksByLogin/", response_class=HTMLResponse)
def read_student_all_subtasks_by_login(
    request: Request,
    current_student=Depends(get_current_student_or_redirect),
    db: Session = Depends(get_db),
    StudentID: Optional[str] = Query(default=None),
    status: str = Query(default=None),
    TaskID: str | None = Query(None),
    variant: int | None = Query(None),
    SortColumn: str = Query(default="StudentTaskID"),
    SortDirection: str = Query(default="ASC")
):
    logger.info(f"Вызван роут с получением задач всех студентов /students_subtasks/StudentTasksByLogin")
# Проверям что пользователь авторизован и отправляем на страницу с логином

    if isinstance(current_student, RedirectResponse):
        return current_student

    # Если пришла пустая строка или None — оставляем None
    try:
        student_id_int = int(StudentID) if StudentID not in (None, "") else None
    except ValueError:
        student_id_int = None

    try:
        task_id_int = int(TaskID) if TaskID not in (None, "") else None
    except ValueError:
        task_id_int = None

    # Если админ выбрал студента — используем его, иначе id текущего
    StudentID = student_id_int if student_id_int is not None else current_student.ID
# Проверяет что студент есть в базей
    if not current_student:
        return templates.TemplateResponse("Students/StudentTasks.html", {
            "request": request,
            "error": "Студент не найден"
        })

    # ищем список категорий
    list_of_tasks = db.execute(text("SELECT TaskID, TaskTitle FROM Tasks")).fetchall()
    # ищем всех студентов
    students_id = db.execute(text("select ID, Login from Students")).fetchall()
    # ищем все варианты
    variants = db.execute(text("select distinct VariantID, VariantName from Variants")).fetchall()

# по его id ищем все его задачи


    print(f" Вызов Хранимки с параметрами StudentID:{StudentID}, CompletionStatus:{(status)} TaskID:{(task_id_int)} SortColumn:{(SortColumn)} SortDirection: {(SortDirection)} VariantID: {(variant)}")
    print(f" Вызов Хранимки с параметрами StudentID:{StudentID}, CompletionStatus:{type(status)} TaskID:{type(task_id_int)} SortColumn:{type(SortColumn)} SortDirection: {type(SortDirection)} VariantID: {type(variant)}")
    tasks1 = students.get_students_all_tasks(
        db=db,
        StudentID=StudentID,
        CompletionStatus=status or None,
        TaskID=task_id_int,
        VariantID=variant,
        SortColumn=SortColumn if SortColumn else None,
        SortDirection=SortDirection if SortDirection else None
    )
    #print(f"TASK TYPE: {type(tasks1[0])}")
    #print(f"TASK VALUE: {tasks1[0]}")
    #print(tasks1)




    # Иначе преобразуем в JSON-словарики
    """Для устранения проблемы преобразования даты в формат JSON"""
    tasks = [StudentTaskRead(**task).model_dump(mode="json") for task in tasks1]
    tasks = tasks or []
    logging.warning(f"ПАРАМЕТРЫ: StudentID={StudentID}") # логирование

    return templates.TemplateResponse("Students/StudentTasks.html", {
        "request": request,
        "StudentID": StudentID,
        "students_id": students_id,
        "tasks": tasks,
        "variants": variants,
        "TasksID": list_of_tasks,
        "student": current_student,
    })

'''
# /students_subtasks/StudentTasks/{StudentID}/{SubTasksID}
'''Возращаем страницу с задачей пользователя по его id и номеру задачи
@students_subtasks_router.get("/T/{StudentTaskID}/",  response_class=HTMLResponse)
def read_student_all_subtasks(
        request: Request,
        StudentTaskID: int,

        current_student=Depends(get_current_student_or_redirect),
        db: Session = Depends(get_db)):
    logging.warning(f"Вызываем роут read_student_all_subtasks с параметрами: StudentTaskID={StudentTaskID}")  # логирование
    Task = students.Get_Student_TaskDetails_By_ID(db, StudentTaskID)
    print(Task)
    files = get_files_for_subtask(int(Task['SubTaskID']), db)
    Task['files'] = files

    user_answer = None
    if Task:
        user_answer = Task['StudentAnswer']  # или как у тебя поле называется
    print(Task)
    print("Task:", Task)


    return templates.TemplateResponse("Students/Task.html", {"request": request, "StudentTaskID": StudentTaskID, "subtask": Task, "student": current_student, "user_answer": user_answer})
'''


