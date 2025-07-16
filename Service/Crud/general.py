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
    error_message: str = "Ошибка запроса к БД"
):
    try:
        result = db.execute(text(query), params)

        # Выбор метода извлечения
        match mode:
            case "scalar":
                return result.scalar()              # Первое поле первой строки
            case "scalars_all":
                return result.scalars().all()       # Список значений одной колонки
            case "mappings_first":
                return result.mappings().first()    # Один словарь (строка)
            case "mappings_all":
                return result.mappings().all()      # Список словарей
            case "one_or_none":
                return result.one_or_none()         # Один объект или None, выбрасывает ошибку если >1
            case "first":
                return result.first()               # Первый результат (обычно ORM объект)
            case _:
                raise ValueError(f"Неизвестный режим выборки: {mode}")

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

'''INSERT'''