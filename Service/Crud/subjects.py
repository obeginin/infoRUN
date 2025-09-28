from utils.config import settings
from utils import errors,general

from sqlalchemy.ext.asyncio import AsyncSession
import logging
from typing import List


logger = logging.getLogger(__name__) # создание логгера для текущего модуля
# TODO переведен на асинхронный postgres



''' функция-SQL запрос к БД для вывода всех предметов'''
async def get_all_subjects(db: AsyncSession):
    logging.debug(f"Запуск функции get_all_subjects")
    return await general.run_query_select(
        db,
        query= '''SELECT * FROM "Subjects"''',
        mode="mappings_all",
        params= None,
        error_message=f"Ошибка при получения предметов из БД"
    )

''' функция-SQL запрос к БД для вывода определенного предмета'''
async def get_subject_by_id(db: AsyncSession, subjectID: int):
    logging.debug(f"Запуск функции get_subject_by_id с subjectID={subjectID}")
    return await general.run_query_select(
        db,
        query= '''SELECT * FROM "Subjects" WHERE "ID" = :subjectID''',
        mode="mappings_first",
        params= {"subjectID": subjectID},
        error_message=f"Ошибка при получения предмета из БД"
    )