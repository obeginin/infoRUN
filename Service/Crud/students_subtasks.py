from Service.Schemas import auth
from utils import errors,general
from sqlalchemy.ext.asyncio import AsyncSession

import logging
logger = logging.getLogger(__name__) # создание логгера для текущего модуля
# Crud\students_subtasks.py


# TODO переведен на асинхронный postgres



async def get_students_all_tasks(db, **params):
    '''функция которая работает по хранимке'''
    logger.debug(f"Запуск функции get_students_all_tasks {params}")
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



async def assign_task_students(db: AsyncSession, student_id: int, subtask_id: int):
    '''Функция назначания задачи для студента'''
    logger.debug(f"Запуск функции assign_task_students с student_id={student_id} | subtask_id={subtask_id}")
    # проверка что задача не назнача
    check = await general.run_query_select(db,
        query="""SELECT 1 FROM "StudentTasks" WHERE "StudentID"=:student_id AND "SubTaskID"=:subtask_id""",
        params={"student_id": student_id, "subtask_id": subtask_id},
        mode='scalar'
    )
    if check: # дубликат
        logger.warning(f"Задача с subtask_id={subtask_id} уже назначена студенту с student_id={student_id}")
        raise errors.conflict(message="Эта задача уже назначена этому студенту")

    # вставка
    query = """insert into "StudentTasks" ("StudentID", "SubTaskID", "CompletionStatus") Values (:StudentID,  :SubTaskID, :CompletionStatus)"""
    return await general.run_query_insert(
        db=db,
        query=query,
        params={"StudentID": student_id, "SubTaskID":subtask_id, "CompletionStatus": "Не приступал"},
        error_message="Ошибка назначения задачи студенту"
    )