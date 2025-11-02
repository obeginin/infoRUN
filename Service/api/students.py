import logging
from fastapi import APIRouter, Depends, Request, Query, Form,  UploadFile, File, Body
from sqlalchemy.ext.asyncio import AsyncSession
from utils.config import settings
from Service.Schemas import students as students_schemas
from Service.Schemas.auth import StudentAuth, StudentOut, StudentCreate, SearchStudentQuery, StudentField, StudentEdit

from Service.Crud.auth import get_student_by_field, get_current_student, permission_required, get_role_id, hash_password, can_edit_admin
from Service.Crud.students import edit_student_id, del_student_id, activate_student_id
from Service.Crud import students
from utils import errors,general
from Service.Database import get_db  # Зависимость для подключения к базе данных
from Service.producer import send_log

logger = logging.getLogger(__name__) # создание логгера для текущего модуля
# api\Students.py


# TODO переведен на асинхронный postgres
students_router = APIRouter(prefix="/api/students", tags=["students"])



"""API"""
# /api/students
''' Эндпоинт: Получить список студентов'''
@students_router.get("",response_model=list[StudentOut],operation_id = 'Students', summary="Получить список студентов в формате JSON")
async def read_all_students(db: AsyncSession = Depends(get_db), current_student=Depends(permission_required("view_students"))):
    logger.info(f"Пользователь {current_student.Login} запросил список всех студентов")
    return await students.get_all_students(db)

# /api/students/{student_id}
''' Эндпоинт: Получить студента по id (/students/{student_id})'''
@students_router.get("/api/{student_id}",operation_id = 'StudentsStudentID', response_model=StudentAuth, summary="Получить студента по его ID)")
async def read_student_id(student_id: int, db: AsyncSession = Depends(get_db), current_student=Depends(permission_required("view_students"))):
    logger.info(f"Пользователь {current_student.Login} запросил студента с id={student_id}")
    return await students.get_student_id(db, student_id)


# /api/students/search (тест ✅)
''' Поиск студента по выбранному полю(ID, Login, Email, Phone '''
@students_router.get("/search",operation_id = 'StudentsSearch', summary="Поиск студента по выбранному полю(ID, Login, Email, Phone")
async def confirm_email(field_name: StudentField = Query(...),
                  value: str = Query(...),
                  db: AsyncSession = Depends(get_db), current_student=Depends(permission_required("admin_panel"))):
    logger.info(f"Пользователь {current_student.Login} запросил информацию студента с field_name={field_name} | value={value}")
    field_name = field_name.value
    value = value

    # ищем студента по выбранному полю
    student = await get_student_by_field(db, field_name, value)
    if student is None:
        logger.warning(f"Студент с {field_name} = {value} не найден")
        raise errors.not_found(message=f"Студент с {field_name} = {value} не найден")

    logger.info(f"Пользователь {current_student.Login} запросил студента с {student.Login} (ID: {student.ID})")
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
    operation_id = 'NewStudent',
    #response_model=list[auth.StudentBase],
    summary="Добавить нового студента",
    description="""
    `Login`, `email` обязательный поля  (должны быть уникальными)
    `Sex` может быть: М, Ж, пустой  
    `RoleID` именно id роли, а не её имя
    `Phone` строка, но должна состоять из цифр
    """
)
async def new_student(student_data: StudentCreate,
                db: AsyncSession = Depends(get_db),
                current_student=Depends(permission_required("create_students"))):
    logger.info(f"Пользователь {current_student.Login} отправил запрос на создание нового студента student_data={student_data}")

    # TODO: оптимизировать одним запросом
    studentWithLogin = await get_student_by_field(db, field_name="Login", value=student_data.Login)
    logger.debug(studentWithLogin)
    if studentWithLogin:
        logger.warning(f"Пользователь с логином: {student_data.Login} уже есть в базе!")
        raise errors.bad_request(message=f"Пользователь с логином '{student_data.Login}' уже есть в базе")
    studentWithEmail = await get_student_by_field(db, field_name="Email", value=student_data.Email)
    if studentWithEmail:
        logger.warning(f"Пользователь с Email: {student_data.Email} уже есть в базе!")
        raise errors.bad_request(message=f"Пользователь с Email '{student_data.Email}' уже есть в базе!")
    studentWithPhone = await get_student_by_field(db, field_name="Phone", value=student_data.Phone)
    if studentWithPhone:
        logger.warning(f"Пользователь с телефоном: {student_data.Phone} уже есть в базе!")
        raise errors.bad_request(message=f"Пользователь с телефоном '{student_data.Phone}' уже есть в базе!")

    # ищем роль по id
    role = await get_role_id(db, student_data.RoleID)
    if not role:
        logger.warning(f"[STUDENTS] Не удалось найти роль с id {student_data.RoleID}")
        return errors.not_found(message=f"Не удалось найти роль с id {student_data.RoleID}")
    hashed_password = hash_password(student_data.Password)

    new_student_id = await students.add_student(db, student_data, hashed_password)
    '''if await students.add_student(db, student_data, hashed_password) != 1:
        logger.warning(f"[STUDENTS] Не удалось добавить студента — возможно, данные невалидны или уже существуют")
        raise errors.bad_request(message="Не удалось добавить студента — возможно, данные невалидны или уже существуют")
'''

    logger.info(f"[STUDENTS] Пользователь '{current_student.Login}' добавил нового студента c id={new_student_id}")
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
    return  {"message": "Студент успешно добавлен", "student_id" : f"{new_student_id}"}

# /api/students/edit_student (тест ✅)
@students_router.patch("/edit_student",operation_id = 'EditStudent', summary="Изменение данных студента по id")
async def edit_student(id: int,
                 data: StudentEdit,
                 db: AsyncSession = Depends(get_db),
                 current_student=Depends(permission_required("edit_students"))):
    logger.info( f"Пользователь {current_student.Login} отправил запрос на изменение студента id={id}")
    logger.debug(f"data={data}")
    # проверка изменения роли (на суперадмина и админов)
    if data.RoleID:
        await can_edit_admin(data.RoleID, db=db, current_student=current_student)

    logger.info(f"[STUDENTS] Данные изменения студента: {data}")
    student_by_id = await get_student_by_field(db, field_name="ID", value=id)
    logger.info(f"[STUDENTS] Студент {student_by_id}")
    if student_by_id == None:
        logger.warning(f"[STUDENTS] Студент с id: {id} не найден")
        raise errors.bad_request(message=f"Студент с id: {id} не найден")
    logger.info(f"Проверяем уникальность логина: {data.Login}")
    # TODO: оптимизировать одним запросом
    if data.Login:
        studentWithLogin = await get_student_by_field(db, field_name="Login", value=data.Login)
        if studentWithLogin and studentWithLogin["ID"] != id:
            logger.warning(f"[STUDENTS] Логин '{data.Login}' уже занят")
            raise errors.bad_request(message=f"Логин '{data.Login}' уже занят")
    logger.info(f"Проверяем уникальность email: {data.Email}")
    if data.Email:
        studentWithEmail = await get_student_by_field(db, field_name="Email", value=data.Email)
        if studentWithEmail and studentWithEmail["ID"] != id:
            logger.warning(f"[STUDENTS] Email '{data.Email}' уже занят")
            raise errors.bad_request(message=f"Email '{data.Email}' уже занят")
    if data.Phone:
        studentWithPhone = await get_student_by_field(db, field_name="Phone", value=data.Phone)
        if studentWithPhone and studentWithPhone["ID"] != id:
            logger.warning(f"[STUDENTS] Телефон '{data.Phone}' уже заня")
            raise errors.bad_request(message=f"Телефон '{data.Phone}' уже занят")
    data.Password = hash_password(data.Password)

    logger.info(f"запуск обновления данных студента с id={id}")
    updated = await edit_student_id(db, student_ID=id, data=data)

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
@students_router.post("/active",operation_id = 'students', summary="Активация/деакцтивация студента")
async def activate_student(id: int, flag: bool, db: AsyncSession = Depends(get_db), current_student=Depends(permission_required("edit_students"))):
    logger.info(f"Пользователь {current_student.Login} отправил запрос на активацию/деактивацию студента студента id={id} | flag={flag}")

    student = await get_student_by_field(db, field_name="ID", value=id)
    logger.info(f"[STUDENTS] Студент {student}")
    if student == None:
        logger.warning(f"[STUDENTS] Студент с id: {id} не найден")
        raise errors.bad_request(message=f"Студент с id: {id} не найден")

    updated = await activate_student_id(db, id, flag)

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




# /api/students/delete_student
@students_router.post("/delete_student",operation_id = 'DeleteStudent', summary="Удаление студента выбранному полю ")
async def delete_student_v2(request: SearchStudentQuery = Depends(), db: AsyncSession = Depends(get_db), current_student=Depends(permission_required("delete_students"))):
    logger.info(f"Пользователь {current_student.Login} отправил запрос на удаление студента студента request={request}")

    field_name = request.field_name.value
    value = request.value

    # ищем студента по выбранному полю
    student = await get_student_by_field(db, field_name, value)
    if student is None:
        logger.warning(f"Студент с {field_name} = {value} не найден")
        raise errors.not_found(message=f"Студент с {field_name} = {value} не найден")

    # Удаляем студента
    await del_student_id(db, student.ID)

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

# /api/students/delete_student (тест ✅)
#@students_router.post("/delete_student", summary="Удаление студента по id и сопутствующих задач")
async def delete_student_v1(id: int, db: AsyncSession = Depends(get_db), current_student=Depends(permission_required("delete_students"))):
    logger.info(f"Пользователь {current_student.Login} отправил запрос на удаление студента студента id={id}")

    student = await get_student_by_field(db, field_name="ID", value=id)
    logger.info(f"[STUDENTS] Студент {student}")
    if student == None:
        logger.warning(f"[STUDENTS] Студент с id: {id} не найден")
        raise errors.bad_request(message=f"Студент с id: {id} не найден")
    await del_student_id(db, id)

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






















