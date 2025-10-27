from fastapi import APIRouter, Depends, Request, Query, Form,  UploadFile, File, Body
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from utils.config import settings
from utils import errors,general
from Service.Database import get_db  # Зависимость для подключения к базе данных
from Service.producer import send_log
from Service.Schemas import students_subtasks as students_subtasks_schemas
from Service.Crud import students_subtasks as students_subtasks_crud
from Service.Schemas import auth as auth_schemas
from Service.Crud.auth import get_current_student, permission_required


logger = logging.getLogger(__name__) # создание логгера для текущего модуля

# api\students_subtasks.py


# TODO переведен на асинхронный postgres

students_subtasks_router = APIRouter(prefix="/api/students_subtasks", tags=["students_subtasks"])


# /api/students_subtasks/
@students_subtasks_router.get("", response_model=list[students_subtasks_schemas.StudentTaskRead],
                              summary="ГЛАВНЫЙ РОУТ с получением списка задач студента по фильтрам",
                              description="""В качестве фильтров передаются параметры    
                                            `StudentTaskID` - по Номеру задачи Студента  
                                            `StudentID` - по id студента
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
async def read_tasks_student(
                       filters: students_subtasks_schemas.StudentTasksQueryParams = Depends(),
                       db: AsyncSession = Depends(get_db),
                       current_student=Depends(permission_required("view_tasks"))):
    logger.info(f"Пользователь '{current_student.Login}' запросил задачи студента")
    logger.info(f"Фильтры: {filters}")

    send_log(
        StudentID=current_student.ID,
        StudentLogin=current_student.Login,
        action="ViewStudentTasks",
        details={
            "DescriptionEvent": "Запрос задач студента",
            "Filters": filters.dict()
        }
    )
    return await students_subtasks_crud.get_students_all_tasks(
        db,
        student_task_id=filters.student_task_id,
        student_id=filters.student_id,
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
        p_limit=filters.p_limit,
        p_offset=filters.p_offset
    )


# TODO надо убирать
# /api/students_subtasks
'''Эндпоинт для получения всех подзадач всех студентов'''
#@students_subtasks_router.get("", response_model=list[students_subtasks_schemas.StudentTaskRead],
#                              summary="ГЛАВНЫЙ РОУТ с получением списка задач всех студентов (без фильтров)",
#                              description="Возвращает список всех задач студентов без применения фильтров.")
async def read_all_students_subtasks(db: AsyncSession = Depends(get_db), current_student=Depends(permission_required("view_tasks"))):
    logger.info(f"Пользователь '{current_student.Login}' запросил задачи всех студентов. ")

    send_log(
        StudentID=current_student.ID,
        StudentLogin=current_student.Login,
        action="ViewStudentsTasks",
        details={"DescriptionEvent": "Запрос задач всех студентов"}
    )
    return await students_subtasks_crud.get_students_all_tasks(db)

# /api/students_subtasks_router/assign_subtasks
@students_subtasks_router.get("/assign_subtasks",
                              summary="назначение задач студенту",
                              description="Для выбранного студента с (student_id)  назначиться задача сsubtask_id со статусом 'не начата'")
async def assign_task_for_student(
        student_id: int,
        subtask_id: int,
        db: AsyncSession = Depends(get_db),
        current_student=Depends(permission_required("assign_tasks"))):
    logger.debug(f"Пользователь '{current_student.Login}' назначает задачу subtask_id={subtask_id} студенту student_id={student_id}. ")

    await students_subtasks_crud.assign_task_students(db,student_id=student_id, subtask_id=subtask_id)
    send_log(
        StudentID=current_student.ID,
        StudentLogin=current_student.Login,
        action="AssignTask",
        details={"DescriptionEvent": f"Студенту с student_id{student_id} назначена задача с student_id={student_id}"}
    )
    logger.info(f"Пользователь '{current_student.Login}' назначил задачу subtask_id={subtask_id} студенту student_id={student_id}. ")
    return {"message": f"Задача успешно назначена студенту", "student_id":student_id, "subtask_id":subtask_id}

# TODO надо убирать

# /api/students_subtasks/{StudentID}/StudentTask/{StudentTaskID}
'''Эндпоинт для получения задачи студента по его student_id и номеру SubTasksID'''
#@students_subtasks_router.get("/{student_id}/StudentTask/{student_task_id}", response_model=list[students_subtasks_schemas.StudentTaskRead], summary="роут с получением данных о задаче студента по StudentTaskID")
async def read_task_student(student_task_id: int, db: AsyncSession = Depends(get_db), current_student=Depends(permission_required("view_tasks"))):
    logger.info(f"Пользователь '{current_student.Login}' запросил данные задачи с ID={student_task_id}. ")

    send_log(
        StudentID=current_student.ID,
        StudentLogin=current_student.Login,
        action="ViewStudentTask",
        details={
            "DescriptionEvent": "Запрос задачи студента",
            "TargetStudentTaskID": student_task_id
        }
    )
    return await students_subtasks_crud.get_students_all_tasks(db, student_task_id=student_task_id)



# TODO надо заменять на новый

'''Проверка ответа пользователя'''
# /api/students_subtasks/check-answer/
'''@students_subtasks_router.post("/check-answer/")
async def check_answer (request: AnswerInput, db: AsyncSession = Depends(get_db)):
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
    return {"status": new_status}'''


# TODO надо менять на новое
'''Отправка Решения  пользователя'''
'''# /api/students_subtasks/submit-solution/
@students_subtasks_router.post("/submit-solution/")
async def submit_solution(
    StudentID: int = Form(...),
    SubTaskID: int = Form(...),
    StudentTaskID: int = Form(...),
    StudentSolutionFile: UploadFile | None = File(None),

    db: AsyncSession = Depends(get_db),
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
    return RedirectResponse(f"/students_subtasks/T/{StudentTaskID}", status_code=303)'''

