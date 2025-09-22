from Service.Models import Student
from Service.Schemas.students import StudentTaskRead
from Service.Schemas import auth
from utils import errors,general

from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
import logging

# Crud\Students.py
''' 
CRUD - основная логика работы запроса
Основные функции для студентов
'''



logger = logging.getLogger(__name__) # создание логгера для текущего модуля

''' Получение всех студентов'''
''' функция-SQL запрос к БД для вывода всех студентов'''
def get_all_students(db: Session):
    return general.run_query_select(
        db,
        query= """SELECT s.*, r.Name as RoleName FROM Students s LEFT JOIN Roles r ON s.RoleID = r.RoleID""",
        mode="mappings_all",
        params= None,
        error_message=f"Ошибка при получения студентов из БД"
    )

''' функция-SQL запрос к БД для вывода определенного студента'''
def get_student_id(db: Session, Student_id: int):
    return general.run_query_select(
        db,
        query= """SELECT s.*, r.Name as RoleName FROM Students s
                LEFT JOIN Roles r ON s.RoleID = r.RoleID
                WHERE s.ID = :Student_id""",
        mode="mappings_first",
        params= {"Student_id": Student_id},
        required=True,
        error_message=f"Ошибка при получения студента из БД"
    )


''' функция добавления нового студента'''
def add_student(db: Session, student: auth.StudentCreate, hashed_password:str):
    data = student.dict()
    # подставляем значение по умолчанию, если не пришло

    if data["IsActive"] is None:
        data["IsActive"] = True

    data["Password"] = hashed_password  # Добавляем хэш пароля

    return general.run_query_insert(
        db,
        query= """INSERT INTO STUDENTS (Login, Last_Name, First_Name, Middle_Name, Email, Sex, BirthDate, Comment, Password, RoleID, IsActive, Phone) 
        VALUES (:Login, :Last_Name, :First_Name, :Middle_Name, :Email, :Sex, :BirthDate, :Comment, :Password, :RoleID, :IsActive, :Phone)""",
        params= data,
        error_message=f"Ошибка при добавлении нового студента"
    )




def edit_student_id(db: Session, student_ID: int, data: auth.StudentCreate):
    # превращаем в словарь, убирая пустые значения
    update_data = {k: v for k, v in data.dict().items() if v is not None}

    if not update_data:
        logger.warning(f"Нет данных для обновления")
        raise errors.bad_request(message="Нет данных для обновления")

    # формируем данные для вставки в SQL запрос
    set_clause = ", ".join([f"{key} = :{key}" for key in update_data])
    update_data["id"] = student_ID  # добавляем ID для условия WHERE

    return general.run_query_update(
        db,
        query=f"""
                update Students 
                set {set_clause}
                where ID = :id
                """,
        params=update_data,
        error_message=f"Ошибка обновления данных студента с id:{student_ID}"
    )

def activate_student_id(db: Session, student_ID: int, flag: bool):
    return general.run_query_update(
        db,
        query="""
                update Students 
                set isActive = :flag
                where ID = :id
                """,
        params={"flag": flag, "id": student_ID},
        error_message=f"Ошибка при обновлении активности студента с ID:{student_ID}"
    )

'''функция удаление студента по id'''
def del_student_id(db: Session, id: int):
    try:
        logger.info(f"Удаляем задачи студента с id: {id}")
        general.run_query_delete(
            db,
            query="""
                DELETE FROM StudentTasks 
                WHERE StudentID = :id
                """,
            params={"id": id},
            commit=False
        )

        logger.info(f"Удаляем студента с id:{id}")
        general.run_query_delete(
            db,
            query="""
                DELETE FROM Students 
                WHERE ID = :id
                """,
            params={"id": id},
            commit=False
        )

        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        logger.exception(f"Ошибка при удалении студента с id:{id} и связанных данных")
        raise errors.internal_server(message=f"Ошибка удаления студента с id:{id} и связанных данных")


'''функция которая работает по хранимке'''
def get_students_all_tasks(
    db,
    student_task_id=None,
    student_id=None,
    sub_task_id=None,
    task_id=None,
    subject_id=None,
    variant_id=None,
    completion_status=None,
    search=None,
    sort_column1=None,
    sort_column2=None,
    sort_direction1=None,
    sort_direction2=None,
    limit=None,
    offset=None
):
    logging.debug(
        f"""[DB CALL] Вызов хранимки GetStudentsTasks с параметрами:
        student_task_id: {student_task_id}, student_id: {student_id}, sub_task_id: {sub_task_id}, task_id: {task_id}, subject_id: {subject_id}, variant_id: {variant_id},
        completion_status: {completion_status}, search: {search}, sort_column1: {sort_column1}, sort_direction1: {sort_direction1}, sort_column2: {sort_column2},
        sort_direction2: {sort_direction2}, offset: {offset}, limit: {limit}
        """
    )

    query = """
    EXEC GetStudentsTasks 
        @StudentTaskID = :student_task_id,
        @StudentID = :student_id,
        @SubTaskID = :sub_task_id,
        @TaskID = :task_id,
        @SubjectID = :subject_id,
        @VariantID = :variant_id,
        @CompletionStatus = :completion_status,
        @Search = :search,
        @SortColumn1 = :sort_column1,
        @SortColumn2 = :sort_column2,
        @SortDirection1 = :sort_direction1,
        @SortDirection2 = :sort_direction2,
        @Limit = :limit,
        @Offset = :offset
    """

    params = {
        "student_task_id": student_task_id,
        "student_id": student_id,
        "sub_task_id": sub_task_id,
        "task_id": task_id,
        "subject_id": subject_id,
        "variant_id": variant_id,
        "completion_status": completion_status,
        "search": search,
        "sort_column1": sort_column1,
        "sort_column2": sort_column2,
        "sort_direction1": sort_direction1,
        "sort_direction2": sort_direction2,
        "limit": limit,
        "offset": offset,
    }
    return general.run_query_select(
        db=db,
        query=query,
        params=params,
        mode="mappings_all",  # Возвращаем список словарей
        required=False,
        error_message="[EXEC] Не удалось получить список задач студента"
    )


''' Получения студента по заданному полю(id, логин)'''
'''def get_student_by_field(db: Session, value: str, by: str = "id"):
    if by == "id":
        try:
            student_id = int(value)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID должен быть числом")
        student = db.query(Student).filter(Student.ID == student_id).all()
    elif by == "login":
        student = db.query(Student).filter(Student.Login == value).all()
    else:
        raise HTTPException(status_code=400, detail="Недопустимое поле поиска")

    if not student:
        raise HTTPException(status_code=404, detail="Студент не найден")

    return student'''

''' Получения всех задач всех студентов '''
def get_all_students_tasks(db: Session):
    query = text("SELECT * FROM StudentTasks JOIN Tasks on Tasks.TaskID = StudentTasks.SubTaskID")
    result = db.execute(query).fetchall()
    student_tasks = [
        {"StudentTaskID": row.StudentTaskID,
        "StudentID": row.StudentID,
         "SubTaskID": row.SubTaskID,
         "CompletionStatus": row.CompletionStatus,
         "Score": row.Score,
         #"CompletionDate": row.CompletionDate,
         "StudentAnswer": row.StudentAnswer,
         "TaskNumber": row.TaskNumber,
         "TaskTitle": row.TaskTitle
         }
        for row in result]
    return student_tasks

''' Получения всех задач студента по ID'''

# МЕНЯЮ НА ХРАНИМКУ!!!!
# С нее работает список задач студентов в админке
'''def get_student_all_tasks(db: Session, student_id: int):
    query = text(f"""SELECT StudentTaskID,StudentID, Login, SubTaskID,CompletionStatus,Score,CompletionDate,StudentAnswer, TaskNumber, TaskTitle  
                 FROM StudentTasks 
                 JOIN Students ON Students.ID = StudentTasks.StudentID 
				 JOIN Tasks on Tasks.TaskID = StudentTasks.SubTaskID
                 WHERE StudentTasks.StudentID = :student_id""")
    result = db.execute(query, {"student_id": student_id}).fetchall()
    logging.warning(f"Получаем задачи для студента с ID = {student_id}")
    logging.warning(f"Результатов найдено: {len(result)}")
    student_tasks = [
        {"StudentTaskID": row.StudentTaskID,
        "StudentID": row.StudentID,
         "Login": row.Login,
         "SubTaskID": row.SubTaskID,
         "CompletionStatus": row.CompletionStatus,
         "Score": row.Score,
         #"CompletionDate": row.CompletionDate,
         "StudentAnswer": row.StudentAnswer,
         "TaskNumber": row.TaskNumber,
         "TaskTitle": row.TaskTitle}
        for row in result]
    if not result:
        raise HTTPException (status_code=404, detail=f"Студент с ID {student_id} не найден")
    return student_tasks
'''





''' Получения задачи студента по SubTaskID'''
def get_task_student(db: Session, student_id: int, SubTaskID: int) -> list[StudentTaskRead]:
# Проверка существования студента (запрос с параметром лучше чем f-строка
    query = text("SELECT 1 FROM Students WHERE ID = :student_id")
    params = {"student_id": student_id}
    student_check = db.execute(query, params).fetchone()
    #student_check = db.execute(text("SELECT 1 FROM Students WHERE ID = :student_id"),{"student_id": student_id}).fetchone()
    if not student_check:
        raise HTTPException(status_code=404, detail=f"Студент с ID {student_id} не найден")

# Проверка существования подзадачи
    subtask_check = db.execute(text("SELECT 1 FROM SubTasks WHERE SubTaskID = :subtask_id"),{"subtask_id": SubTaskID}).fetchone()
    if not subtask_check:
        raise HTTPException(status_code=404, detail=f"Подзадача с ID {SubTaskID} не найдена")

# Основной запрос
    query = text(f"select * from StudentTasks join Students on ID=StudentID where StudentID={student_id} and SubTaskID={SubTaskID}")
    result = db.execute(query).fetchall()
    if not result:
            raise HTTPException(status_code=404, detail=f"У студента с ID {student_id} нет подзадачи с ID {SubTaskID}")

    task_student = [
        {"StudentTaskID": row.StudentTaskID,
        "StudentID": row.StudentID,
         "Login": row.Login,
         "SubTaskID": row.SubTaskID,
         "CompletionStatus": row.CompletionStatus,
         "Score": row.Score,
         #"CompletionDate": row.CompletionDate,
         "StudentAnswer": row.StudentAnswer}
        for row in result]
    return task_student

# Функция для получения студента по логину
'''def get_student_by_login(db: Session, login: str):
    return db.query(Student).filter(Student.Login == login).first()'''


'''все данные задачи выбранного студента по StudentTaskID'''
def Get_Student_TaskDetails_By_ID(db: Session, StudentTaskID: int):
    query = text("EXEC dbo.GetStudentsTasks @StudentTaskID = :student_task_id")
    result =  db.execute(query, {"student_task_id": StudentTaskID})
    if not result:
            raise HTTPException(status_code=404, detail=f"нет подзадачи с StudentTaskID {StudentTaskID}")

    row = result.fetchone()
    return dict(row._mapping)