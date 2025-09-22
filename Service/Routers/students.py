from utils.config import settings
from Service.Schemas.students import StudentTaskRead, StudentTasksQueryParams, AnswerInput
from Service.Schemas.auth import StudentAuth, StudentOut, StudentCreate, SearchStudentQuery, StudentField, StudentEdit

from Service.Crud.auth import verify_password, get_student_by_field
from Service.Crud.auth import get_current_student, permission_required, get_role_id, hash_password
from Service.Crud.students import edit_student_id, del_student_id, activate_student_id
from Service.Crud import students
from utils import errors,general

from Service.Routers.subtasks import get_files_for_subtask
from Service.dependencies import get_db  # Зависимость для подключения к базе данных

from Service.producer import send_log


from fastapi import APIRouter, Depends, Request, Query, Form,  UploadFile, File, Body
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
templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)


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

# /api/students/{student_id}
''' Эндпоинт: Получить студента по id (/students/{student_id})'''
@students_router.get("/api/{student_id}", response_model=StudentAuth, summary="Получить студента по его ID)")
def read_student_id(student_id: int, db: Session = Depends(get_db)):
    return students.get_student_id(db, student_id)


# /api/students/search (тест ✅)
''' Поиск студента по выбранному полю(ID, Login, Email, Phone '''
@students_router.get("/search", summary="Поиск студента по выбранному полю(ID, Login, Email, Phone")
def confirm_email(field_name: StudentField = Query(...),
                  value: str = Query(...),
                  db: Session = Depends(get_db), current_student=Depends(permission_required("admin_panel"))):
    field_name = field_name.value
    value = value

    # ищем студента по выбранному полю
    student = get_student_by_field(db, field_name, value)
    if student is None:
        logger.warning(f"Студент с {field_name} = {value} не найден")
        raise errors.not_found(message=f"Студент с {field_name} = {value} не найден")

    logger.info(f"[STUDENTS] Пользователь {current_student.Login} запросил студента с {student.Login} (ID: {student.ID})")
    send_log(
        StudentID=student["ID"],
        StudentLogin=student["Login"],
        action="StudentSearch",
        details={
            "DescriptionEvent": f"Пользователь {current_student.Login} запросил студента с {student.Login} (ID: {student.ID})"
        }
    )
    return student


# /api/students/new_student (тест ✅)
@students_router.post(
    "/new_student",
    #response_model=list[auth.StudentBase],
    summary="Добавить нового студента",
    description="""
    `Login`, `email` обязательный поля  (должны быть уникальными)
    `Sex` может быть: М, Ж, пустой  
    `RoleID` именно id роли, а не её имя
    `Phone` строка, но должна состоять из цифр
    """
)
def new_student(student_data: StudentCreate,
                db: Session = Depends(get_db),
                current_student=Depends(permission_required("admin_panel"))):
    logger.debug(student_data)

    # TODO: оптимизировать одним запросом
    studentWithLogin = get_student_by_field(db, field_name="Login", value=student_data.Login)
    logger.debug(studentWithLogin)
    if studentWithLogin:
        logger.warning(f"Пользователь с логином: {student_data.Login} уже есть в базе!")
        raise errors.bad_request(message=f"Пользователь с логином '{student_data.Login}' уже есть в базе")
    studentWithEmail = get_student_by_field(db, field_name="Email", value=student_data.Email)
    if studentWithEmail:
        logger.warning(f"Пользователь с Email: {student_data.Email} уже есть в базе!")
        raise errors.bad_request(message=f"Пользователь с Email '{student_data.Email}' уже есть в базе!")
    studentWithPhone = get_student_by_field(db, field_name="Phone", value=student_data.Phone)
    if studentWithPhone:
        logger.warning(f"Пользователь с телефоном: {student_data.Phone} уже есть в базе!")
        raise errors.bad_request(message=f"Пользователь с телефоном '{student_data.Phone}' уже есть в базе!")

    # ищем роль по id
    role = get_role_id(db, student_data.RoleID)
    if not role:
        logger.warning(
            f"[STUDENTS] Не удалось найти роль с id {student_data.RoleID}")
        return errors.not_found(message=f"Не удалось найти роль с id {student_data.RoleID}")
    hashed_password = hash_password(student_data.Password)

    if students.add_student(db, student_data, hashed_password) != 1:
        logger.warning(f"[STUDENTS] Не удалось добавить студента — возможно, данные невалидны или уже существуют")
        raise errors.bad_request(message="Не удалось добавить студента — возможно, данные невалидны или уже существуют")


    logger.info(f"[STUDENTS] Пользователь '{current_student.Login}' добавил нового студента")
    send_log(
        StudentID=current_student.ID,
        StudentLogin=current_student.Login,
        action="AddStudent",
        details={
            "DescriptionEvent": "Администратор добавил нового студента",
            "NewStudentLogin": student_data.Login,
            "NewStudentEmail": student_data.Email
        }
    )
    return  {"message": "Студент успешно добавлен"}

# /api/students/edit_student (тест ✅)
@students_router.patch("/edit_student", summary="Изменение данных студента по id")
def edit_student(id: int, data: StudentEdit, db: Session = Depends(get_db), current_student=Depends(permission_required("admin_panel"))):
    logger.info(f"[STUDENTS] Данные изменения студента: {data}")
    student_by_id = get_student_by_field(db, field_name="ID", value=id)
    logger.info(f"[STUDENTS] Студент {student_by_id}")
    if student_by_id == None:
        logger.warning(f"[STUDENTS] Студент с id: {id} не найден")
        raise errors.bad_request(message=f"Студент с id: {id} не найден")
    logger.info(f"Проверяем уникальность логина: {data.Login}")
    # TODO: оптимизировать одним запросом
    if data.Login:
        studentWithLogin = get_student_by_field(db, field_name="Login", value=data.Login)
        if studentWithLogin and studentWithLogin["ID"] != id:
            logger.warning(f"[STUDENTS] Логин '{data.Login}' уже занят")
            raise errors.bad_request(message=f"Логин '{data.Login}' уже занят")
    logger.info(f"Проверяем уникальность email: {data.Email}")
    if data.Email:
        studentWithEmail = get_student_by_field(db, field_name="Email", value=data.Email)
        if studentWithEmail and studentWithEmail["ID"] != id:
            logger.warning(f"[STUDENTS] Email '{data.Email}' уже занят")
            raise errors.bad_request(message=f"Email '{data.Email}' уже занят")
    if data.Phone:
        studentWithPhone = get_student_by_field(db, field_name="Phone", value=data.Phone)
        if studentWithPhone and studentWithPhone["ID"] != id:
            logger.warning(f"[STUDENTS] Телефон '{data.Phone}' уже заня")
            raise errors.bad_request(message=f"Телефон '{data.Phone}' уже занят")
    data.Password = hash_password(data.Password)

    logger.info(f"запуск обновления данных студента с id={id}")
    updated = edit_student_id(db, student_ID=id, data=data)

    if updated != 1:
        logger.warning(f"[STUDENTS] Ошибка при обновлении данных студента с логином: {student_by_id.Login}")
        raise errors.internal_server(message="Ошибка при обновлении данных студента с логином: {student}")

    logger.info(f"[STUDENTS] Пользователь:{current_student.Login} изменил студента с логином: {student_by_id.Login} и id: {id}.")
    send_log(
        StudentID=student_by_id.ID,
        StudentLogin=student_by_id.Login,
        action="StudentUpdated",
        details={
            "DescriptionEvent": f"Пользователь:{current_student.Login} изменил студента с логином: {student_by_id.Login} и id: {id}",
        }
    )
    return {"message": f"Студент с логином: {student_by_id.Login} успешно изменен"}

# /api/students/active (тест ✅)
@students_router.post("/active", summary="Активация/деакцтивация студента")
def activate_student(id: int, flag: bool, db: Session = Depends(get_db), current_student=Depends(permission_required("admin_panel"))):

    student = get_student_by_field(db, field_name="ID", value=id)
    logger.info(f"[STUDENTS] Студент {student}")
    if student == None:
        logger.warning(f"[STUDENTS] Студент с id: {id} не найден")
        raise errors.bad_request(message=f"Студент с id: {id} не найден")

    updated = activate_student_id(db, id, flag)

    if updated != 1:
        logger.warning(f"[STUDENTS] Не удалось обновить статус активности студента: {student}")
        raise errors.internal_server(message=f"Не удалось обновить статус активности студента: {student}")

    logger.info(f"[STUDENTS] Пользователь {current_student.Login} {'активировал' if flag else 'деактивировал'} студента {student['Login']} (ID: {id})")
    # Лог в Kafka (если у тебя используется send_log)
    send_log(
        StudentID=current_student.ID,
        StudentLogin=current_student.Login,
        action="StudentActivated" if flag else "StudentDeactivated",
        details={
            "DescriptionEvent": f"Пользователь {current_student.Login} {'активировал' if flag else 'деактивировал'} студента {student['Login']} (ID: {id})"
        }
    )
    return {"message": f"Студент {student['Login']} {'активирован' if flag else 'деактивирован'} успешно"}


# /api/students/delete_student (тест ✅)
@students_router.post("/delete_student", summary="Удаление студента по id и сопутствующих задач")
def confirm_email(id: int, db: Session = Depends(get_db), current_student=Depends(permission_required("admin_panel"))):
    # try:
    student = get_student_by_field(db, field_name="ID", value=id)
    logger.info(f"[STUDENTS] Студент {student}")
    if student == None:
        logger.warning(f"[STUDENTS] Студент с id: {id} не найден")
        raise errors.bad_request(message=f"Студент с id: {id} не найден")
    del_student_id(db, id)

    logger.info(f"[STUDENTS] Администратор:{current_student.Login} удалил студента с логином: {student.Login} и id: {id}")
    send_log(
        StudentID=student["ID"],
        StudentLogin=student["Login"],
        action="StudentDeleted",
        details={
            "DescriptionEvent": f"Администратор:{current_student.Login} удалил студента с логином: {student.Login}",
        }
    )
    return {"message": f"Студент с логином: {student.Login} успешно удалён"}



# /api/students/delete_student/v2
@students_router.post("/delete_student/v2", summary="Удаление студента выбранному полю ")
def confirm_email(request: SearchStudentQuery = Depends(), db: Session = Depends(get_db), current_student=Depends(permission_required("admin_panel"))):
    field_name = request.field_name.value
    value = request.value

    # ищем студента по выбранному полю
    student = get_student_by_field(db, field_name, value)
    if student is None:
        logger.warning(f"Студент с {field_name} = {value} не найден")
        raise errors.not_found(message=f"Студент с {field_name} = {value} не найден")

    # Удаляем студента
    del_student_id(db, student.ID)

    logger.info(f"[STUDENTS] Пользователь {current_student.Login} удалил студента {student.Login} (ID: {student.ID})")
    send_log(
        StudentID=student["ID"],
        StudentLogin=student["Login"],
        action="StudentDeleted",
        details={
            "DescriptionEvent": f"Администратор {current_student.Login} удалил студента: {student.Login} (ID: {student.ID})"
        }
    )
    return {"message": f"Студент с {field_name} = {value} успешно удалён"}

'''Студенты

@admin_router.post("/new_student", summary="Добавление нового студента")
def confirm_email(email: EmailStr,
                  db: Session = Depends(get_db), current_student=Depends(permission_required("admin_panel"))):
    # try:
    student = get_student_by_email(db, email)
    logger.info(f"Студент cccccc {student}")
    if student == None:
        logger.warning(f"Студент с email {email} не найден")
        raise errors.bad_request(message=f"Студент с email {email} не найден")
    del_student_id(db, email)

    logger.info(f"[ADMIN] Администратор:{current_student.Login} удалил студента с email: {email}")
    send_log(
        StudentID=student["ID"],
        StudentLogin=student["Login"],
        action="StudentDeleted",
        details={
            "DescriptionEvent": f"Администратор:{current_student.Login} удалил студента с email: {email}",
        }
    )
    return {"message": f"Студент с email {email} успешно удалён"}

'''

# /api/students_subtasks
'''Эндпоинт для получения всех подзадач всех студентов'''
@students_subtasks_router.get("", response_model=list[StudentTaskRead],
                              summary="ГЛАВНЫЙ РОУТ с получением списка задач всех студентов (без фильтров)",
                              description="Возвращает список всех задач студентов без применения фильтров.")
def read_all_students_subtasks(db: Session = Depends(get_db), current_student=Depends(permission_required("view_tasks"))):
    logger.info(f"[TASKS] Пользователь '{current_student.Login}' запросил задачи всех студентов. ")

    send_log(
        StudentID=current_student.ID,
        StudentLogin=current_student.Login,
        action="ViewStudentsTasks",
        details={"DescriptionEvent": "Запрос задач всех студентов"}
    )
    return students.get_students_all_tasks(db)



# /api/students_subtasks/{StudentID}
@students_subtasks_router.get("/{StudentID}", response_model=list[StudentTaskRead],
                              summary="ГЛАВНЫЙ РОУТ с получением списка задач студента по фильтрам",
                              description="""В качестве фильтров передаются параметры    
                                            `StudentTaskID` - по Номеру задачи Студента  
                                            `StudentID` - по id студента (по PATH)  
                                            `SubTaskID` - по id задачи  
                                            `TaskID` - по id категории  
                                            `SubjectID` - по id предмета  
                                            `VariantID` - по id варианта  
                                            `CompletionStatus` - по статусу выполнения   
                                            `Search` - Поиск по ключевому слову (логин, описание и т.п.)  
                                            `SortColumn1` - Выбор колонки для сортировки 1 уровень  
                                            `SortColumn2` - Выбор колонки для сортировки 2 уровень  
                                            `SortDirection1` - Сортировка (по возрастанию ASC ) DESC -по убыванию  
                                            `SortDirection2`	NVARCHAR(4)		= 'ASC'    
                                            `Offset` - с какой строки начинать выводить  
                                            `Limit` - количество выведенных строк (По умолчанию: 500)
                                          """)
def read_tasks_student(StudentID: int,
                       filters: StudentTasksQueryParams = Depends(),
                       db: Session = Depends(get_db),
                       current_student=Depends(permission_required("view_tasks"))):
    logger.info(
        f"[TASKS] Пользователь '{current_student.Login}' запросил задачи студента с ID {StudentID}. "
        f"Фильтры: {filters.dict()}"
    )

    send_log(
        StudentID=current_student.ID,
        StudentLogin=current_student.Login,
        action="ViewStudentTasks",
        details={
            "DescriptionEvent": "Запрос задач студента",
            "TargetStudentID": StudentID,
            "Filters": filters.dict()
        }
    )
    return students.get_students_all_tasks(
        db,
        student_task_id=filters.student_task_id,
        student_id=StudentID,
        sub_task_id=filters.sub_task_id,
        task_id=filters.task_id,
        subject_id=filters.subject_id,
        variant_id=filters.variant_id,
        completion_status=filters.completion_status,
        search=filters.search,
        sort_column1=filters.sort_column1,
        sort_column2=filters.sort_column2,
        sort_direction1=filters.sort_direction1,
        sort_direction2=filters.sort_direction2,
        limit=filters.limit,
        offset=filters.offset
    )


# /api/students_subtasks/{StudentID}/StudentTask/{StudentTaskID}
'''Эндпоинт для получения задачи студента по его student_id и номеру SubTasksID'''
@students_subtasks_router.get("/{student_id}/StudentTask/{student_task_id}", response_model=list[StudentTaskRead], summary="роут с получением данных о задаче студента по StudentTaskID")
def read_task_student(student_task_id: int, db: Session = Depends(get_db), current_student=Depends(permission_required("view_tasks"))):
    logger.info(f"[TASKS] Пользователь '{current_student.Login}' запросил данные задачи с ID={student_task_id}. ")

    send_log(
        StudentID=current_student.ID,
        StudentLogin=current_student.Login,
        action="ViewStudentTask",
        details={
            "DescriptionEvent": "Запрос задачи студента",
            "TargetStudentTaskID": student_task_id
        }
    )
    return students.get_students_all_tasks(db, student_task_id=student_task_id)

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
        filepath = settings.UPLOAD_STUDENTS_IMAGE_DIR / filename
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
    tasks = [students.tudentTaskRead(**task).model_dump(mode="json") for task in tasks1]
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


