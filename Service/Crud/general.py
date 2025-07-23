from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from Service.Crud import errors
import logging

# Crud\general.py

logger = logging.getLogger(__name__) # создание логгера для текущего модуля



'''Универсальный шаблон для SQL-запросов'''
'''SELECT'''
def run_query_select(
    db: Session,
    query: str,
    params: dict,
    mode: str = "mappings_first",
    required: bool = False, # флаг что не пустой результат
    error_message: str = "Ошибка запроса к БД"
):
    try:
        result = db.execute(text(query), params)

        # Выбор метода извлечения
        match mode:
            case "scalar":
                data =  result.scalar()              # Первое поле первой строки
            case "scalars_all":
                data =  result.scalars().all()       # Список значений одной колонки
            case "mappings_first":
                data =  result.mappings().first()    # Один словарь (строка)
            case "mappings_all":
                data =  result.mappings().all()      # Список словарей
            case "one_or_none":
                data =  result.one_or_none()         # Один объект или None, выбрасывает ошибку если >1
            case "first":
                data =  result.first()               # Первый результат (обычно ORM объект)
            case _:
                raise ValueError(f"Неизвестный режим выборки: {mode}")

        if required and not data:
            raise errors.not_found(message=error_message)

        return data

    except SQLAlchemyError:
        logger.exception(f"[DB ERROR] {error_message}")
        raise errors.internal_server(message=error_message)


'''UPDATE'''
def run_query_update(db: Session, query: str, params: dict = None, error_message: str = "Ошибка записи в БД"):
    try:
        result = db.execute(text(query), params or {})
        db.commit()
        return result.rowcount
    except SQLAlchemyError:
        logger.exception(f"[DB ERROR] {error_message}")
        raise errors.internal_server(message=error_message)

'''DELETE'''
def run_query_delete(
    db: Session,
    query: str,
    params: dict = None,
    error_message: str = "Ошибка удаления из БД"
):
    try:
        result = db.execute(text(query), params or {})
        db.commit()
        return result.rowcount
    except SQLAlchemyError:
        logger.exception(f"[DB ERROR] {error_message}")
        raise errors.internal_server(message=error_message)

'''INSERT'''
def run_query_insert(
    db: Session,
    query: str,
    params: dict = None,
    error_message: str = "Ошибка вставки в БД"
):
    try:
        result = db.execute(text(query), params or {})
        db.commit()
        inserted_id = result.scalar()  # Получаем ID из OUTPUT
        return inserted_id
        # Если нужно получить id вставленной записи (PostgreSQL и др.):
        # inserted_id = result.scalar()
        # return inserted_id

        return result.rowcount  # обычно 1 при успешной вставке
    except SQLAlchemyError:
        logger.exception(f"[DB ERROR] {error_message}")
        raise errors.internal_server(message=error_message)