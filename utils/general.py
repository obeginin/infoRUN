# from sqlalchemy.orm import Session # Синхронная
from sqlalchemy.ext.asyncio import AsyncSession # Асинхронная
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from utils import errors,general
import logging

# Crud\general.py
logger = logging.getLogger(__name__) # создание логгера для текущего модуля

# TODO переведен на асинхронный postgres (но надо сделать вызовы функций через await)

'''Универсальные шаблон для SQL-запросов'''
'''SELECT'''
async def run_query_select(
    db: AsyncSession,
    query: str,
    params: dict = None,
    mode: str = "mappings_first",
    required: bool = False, # флаг что не пустой результат
    error_message: str = "Ошибка запроса к БД"
):
    try:
        logger.debug(f"SQL: {query} | params={params} | mode={mode}")
        result = await db.execute(text(query), params)

        # Выбор метода извлечения
        match mode:
            case "scalar":
                data = result.scalar()              # Первое поле первой строки
            case "scalars_all":
                data = result.scalars().all()       # Список значений одной колонки
            case "mappings_first":
                data = result.mappings().first()    # Один словарь (строка)
            case "mappings_all":
                data = result.mappings().all()      # Список словарей
            case "one_or_none":
                data = result.one_or_none()         # Один объект или None, выбрасывает ошибку если >1
            case "first":
                data = result.first()               # Первый результат (обычно ORM объект)
            case _:
                raise ValueError(f"Неизвестный режим выборки: {mode}")

        if required and not data:
            logger.info(f"Пустой результат (required=True): {query} params={params}")
            raise errors.not_found(message=error_message)

        return data

    except SQLAlchemyError as e :
        logger.exception(f"[DB ERROR] {error_message}  | Query: {query} | Params: {params}")
        raise errors.internal_server(message=error_message) from e
    except Exception as e:
        logger.exception(f"[DB EXCEPTION] {error_message} | Query: {query} | Params: {params}")
        raise errors.internal_server(message=error_message) from e

'''UPDATE'''
async def run_query_update(
        db: AsyncSession,
        query: str,
        params: dict | None = None,
        commit: bool = True,
        error_message: str = "Ошибка записи в БД"):
    try:
        logger.debug(f"SQL: {query} | params={params} | commit={commit}")
        result = await db.execute(text(query), params or {})
        if commit:
            await db.commit()
            logger.debug("Коммит выполнен успешно")
        return result.rowcount
    except SQLAlchemyError as e:
        logger.exception(f"[DB ERROR] {error_message} | Query: {query} | Params: {params}")
        raise errors.internal_server(message=error_message) from e

    except Exception as e:
        logger.exception(f"[DB EXCEPTION] {error_message} | Query: {query} | Params: {params}")
        raise errors.internal_server(message=error_message) from e

'''DELETE'''
async def run_query_delete(
    db: AsyncSession,
    query: str,
    params: dict = None,
    commit: bool = True,
    error_message: str = "Ошибка удаления из БД"
):
    try:
        logger.debug(f"SQL: {query} | params={params} | commit={commit}")
        result = await db.execute(text(query), params or {})
        if commit:
            await db.commit()
            logger.debug("Коммит выполнен успешно")
        return result.rowcount
    except SQLAlchemyError as e:
        logger.exception(f"[DB ERROR] {error_message} | Query: {query} | Params: {params}")
        raise errors.internal_server(message=error_message) from e

    except Exception as e:
        logger.exception(f"[DB EXCEPTION] {error_message} | Query: {query} | Params: {params}")
        raise errors.internal_server(message=error_message) from e

'''INSERT'''
async def run_query_insert(
    db: AsyncSession,
    query: str,
    params: dict = None,
    commit: bool = True,
    error_message: str = "Ошибка вставки в БД",
    return_id: bool = False
):
    try:
        logger.debug(f"SQL: {query} | params={params} | commit={commit} | return_id={return_id}")
        result = await db.execute(text(query), params or {})
        if commit:
            await db.commit()
            logger.debug("Коммит выполнен успешно")

        if return_id:
            # для PostgreSQL с RETURNING
            inserted_id = result.scalar()  # вернёт первый столбец первой строки
            return inserted_id

            # если return_id=False — возвращаем количество строк
        return result.rowcount
        #inserted_id = result.scalar()  # Получаем ID из OUTPUT
        #return inserted_id
        # Если нужно получить id вставленной записи (PostgreSQL и др.):
        # inserted_id = result.scalar()
        # return inserted_id


    except IntegrityError as e:
        err_msg = str(e.orig).lower()
        await db.rollback()
    # прописываем разные ошибки
        if "unique constraint" in err_msg or "unique index" in err_msg:
            logger.exception(f"[DB ERROR] Нарушение уникального ограничения: {e.orig}")
            raise errors.conflict(message="Введённые данные должны быть уникальны.")
        elif "foreign key constraint" in err_msg or "foreign key violation" in err_msg:
            logger.exception(f"[DB ERROR] Нарушение внешнего ключа: {e.orig}")
            raise errors.bad_request(message="Связанные данные не найдены (ошибка внешнего ключа).")
        else:
            logger.exception(f"[DB ERROR] Нарушение ограничения целостности: {e.orig}")
            raise errors.bad_request(message="Ошибка целостности данных.")
    except SQLAlchemyError as e:
        logger.exception(f"[DB ERROR] {error_message} | Query: {query} | Params: {params}")
        raise errors.internal_server(message=error_message) from e

    except Exception as e:
        logger.exception(f"[DB EXCEPTION] {error_message} | Query: {query} | Params: {params}")
        raise errors.internal_server(message=error_message) from e


