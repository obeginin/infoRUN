from Service.Models import Student
from Service.Schemas.students import StudentTaskRead
from Service.Schemas import auth
from utils import errors,general
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import text
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
import logging
logger = logging.getLogger(__name__) # создание логгера для текущего модуля
# Crud\Students.py
''' 
CRUD - основная логика работы запроса
Основные функции для студентов
'''

# TODO переведен на асинхронный postgres



''' Получение всех студентов'''
''' функция-SQL запрос к БД для вывода всех студентов'''
async def get_all_students(db: AsyncSession):

    return await general.run_query_select(
        db,
        query= '''SELECT s.*, r."Name" as "RoleName" FROM "Students" s LEFT JOIN "Roles" r ON s."RoleID" = r."RoleID"''',
        mode="mappings_all",
        params= None,
        error_message=f"Ошибка при получения студентов из БД"
    )

''' функция-SQL запрос к БД для вывода определенного студента'''
async def get_student_id(db: AsyncSession, Student_id: int):
    return await general.run_query_select(
        db,
        query= """SELECT s.*, r."Name" as "RoleName" FROM "Students" s
                LEFT JOIN "Roles" r ON s."RoleID" = r."RoleID"
                WHERE s."ID" = :Student_id;""",
        mode="mappings_first",
        params= {"Student_id": Student_id},
        required=True,
        error_message=f"Ошибка при получения студента из БД"
    )


''' функция добавления нового студента'''
async def add_student(db: AsyncSession, student: auth.StudentCreate, hashed_password:str):
    logger.debug(f"Функция добавления нового студента add_student")
    data = student.dict()
    # подставляем значение по умолчанию, если не пришло

    if data["IsActive"] is None:
        data["IsActive"] = True

    data["Password"] = hashed_password  # Добавляем хэш пароля

    return await general.run_query_insert(
        db,
        query= """INSERT INTO "Students" ("Login", "Last_Name", "First_Name", "Middle_Name", "Email", "Sex", "BirthDate", "Comment", "Password", "RoleID", "IsActive", "Phone") 
        VALUES (:Login, :Last_Name, :First_Name, :Middle_Name, :Email, :Sex, :BirthDate, :Comment, :Password, :RoleID, :IsActive, :Phone)
        RETURNING "ID";""",
        params= data,
        return_id = True,
        error_message=f"Ошибка при добавлении нового студента"
    )




async def edit_student_id(db: AsyncSession, student_ID: int, data: auth.StudentCreate):
    logger.debug(f"Функция изменение студента с student_ID={student_ID}")
    # превращаем в словарь, убирая пустые значения
    update_data = {k: v for k, v in data.dict().items() if v is not None}

    if not update_data:
        logger.warning(f"Нет данных для обновления")
        raise errors.bad_request(message="Нет данных для обновления")

    # формируем данные для вставки в SQL запрос

    set_clause = ", ".join([f'"{key}" = :{key}' for key in update_data])
    update_data["ID"] = student_ID  # добавляем ID для условия WHERE
    logger.warning(f"set_clause={set_clause}")
    return await general.run_query_update(
        db,
        query=f"""
                update "Students" 
                set {set_clause}
                where "ID" = :ID;
                """,
        params=update_data,
        error_message=f"Ошибка обновления данных студента с id:{student_ID}"
    )

async def activate_student_id(db: AsyncSession, student_ID: int, flag: bool):
    logger.debug(f"Функция активации/деактивации студента с student_ID={student_ID} | flag={flag}")
    return await general.run_query_update(
        db,
        query="""
                update "Students" 
                set "IsActive" = :flag
                where "ID" = :id;
                """,
        params={"flag": flag, "id": student_ID},
        error_message=f"Ошибка при обновлении активности студента с ID:{student_ID}"
    )

'''функция удаление студента по id'''
async def del_student_id(db: AsyncSession, id: int):
    try:
        logger.info(f"Удаляем задачи студента с id: {id}")
        await general.run_query_delete(
            db,
            query="""
                DELETE FROM "StudentTasks" 
                WHERE "StudentID" = :id;
                """,
            params={"id": id},
            commit=False
        )

        logger.info(f"Удаляем студента с id:{id}")
        await general.run_query_delete(
            db,
            query="""
                DELETE FROM "Students" 
                WHERE "ID" = :id;
                """,
            params={"id": id},
            commit=False
        )

        await db.commit()
    except SQLAlchemyError as e:
        await db.rollback()
        logger.exception(f"Ошибка при удалении студента с id:{id} и связанных данных")
        raise errors.internal_server(message=f"Ошибка удаления студента с id:{id} и связанных данных")




async def get_students_all_tasks(db, **params):
    '''функция которая работает по хранимке'''
    # params = {'student_id': 2, 'task_id': 5, ...}
    args_sql = []

    for k, v in params.items():
        if v is not None:
            args_sql.append(f'"{k}" := :{k}')

    query = f"""
            SELECT * FROM get_students_tasks(
                {', '.join(args_sql)}
            )
        """
    return await general.run_query_select(
        db=db,
        query=query,
        params=params,
        mode="mappings_all",  # Возвращаем список словарей
        required=False,
        error_message="[F_GET] Не удалось получить список задач студента"
    )

async def __get_students_all_tasks(
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
    logger.debug(
        f"""[EXEC] Вызов хранимки get_students_tasks с параметрами:
        student_task_id: {student_task_id}, student_id: {student_id}, sub_task_id: {sub_task_id}, task_id: {task_id}, subject_id: {subject_id}, variant_id: {variant_id},
        completion_status: {completion_status}, search: {search}, sort_column1: {sort_column1}, sort_direction1: {sort_direction1}, sort_column2: {sort_column2},
        sort_direction2: {sort_direction2}, offset: {offset}, limit: {limit}
        """
    )

    query = """
        SELECT * FROM get_students_tasks(
        p_StudentTaskID := :student_task_id::int,
        p_StudentID := :student_id::int,
        p_SubTaskID := :sub_task_id::int,
        p_TaskID := :task_id::int,
        p_SubjectID := :subject_id::int,
        p_VariantID := :variant_id::int,
        p_CompletionStatus := :completion_status::varchar,
        p_Search := :search::varchar,
        p_SortColumn1 := :sort_column1::varchar,
        p_SortColumn2 := :sort_column2::varchar,
        p_SortDirection1 := :sort_direction1::varchar,
        p_SortDirection2 := :sort_direction2::varchar,
        p_Offset := :offset::int,
        p_Limit := :limit::int
    )
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
        "sort_column1": sort_column1.value if sort_column1 else None,
        "sort_column2": sort_column2.value if sort_column2 else None,
        "sort_direction1": sort_direction1.value if sort_direction1 else None,
        "sort_direction2": sort_direction2.value if sort_direction2 else None,
        "offset": offset,
        "limit": limit,
    }
    return await general.run_query_select(
        db=db,
        query=query,
        params=params,
        mode="mappings_all",  # Возвращаем список словарей
        required=False,
        error_message="[F_GET] Не удалось получить список задач студента"
    )


''' Получения студента по заданному полю(id, логин)'''
'''async def get_student_by_field(db: Session, value: str, by: str = "id"):
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



# TODO возможно надо убрать вместе с роутом

'''все данные задачи выбранного студента по StudentTaskID'''
async def Get_Student_TaskDetails_By_ID(db: AsyncSession, StudentTaskID: int):
    query = "EXEC dbo.GetStudentsTasks @StudentTaskID = :student_task_id"
    param = {"student_task_id": StudentTaskID}
    result = await general.run_query_select(db, query=query,params=param)
    if not result:
        raise errors.not_found(message= f"нет подзадачи с StudentTaskID {StudentTaskID}")
    row = result.fetchone()
    return dict(row._mapping)