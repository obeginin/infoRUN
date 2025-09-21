from utils.config import settings
from utils import errors,general

from sqlalchemy.ext.asyncio import AsyncSession
import logging

logger = logging.getLogger(__name__) # создание логгера для текущего модуля

# TODO переведен на асинхронный postgres

async def get_variants(db: AsyncSession, subject_id: int | None = None, variant_id: int | None = None):
    logger.debug(f"Запуск функции get_variants | subject_id={subject_id}, variant_id={variant_id}")

    if variant_id is not None:
        query = '''SELECT * FROM "Variants" WHERE "VariantID" = :variant_id'''
        params = {"variant_id": variant_id}

    elif subject_id is not None:
        query = '''SELECT * FROM "Variants" WHERE "SubjectID" = :subject_id ORDER BY "VariantName"'''
        params = {"subject_id": subject_id}

    else:
        query = '''SELECT * FROM "Variants" ORDER BY "VariantName"'''
        params = {}

    return await general.run_query_select(
        db,
        query= query,
        mode="mappings_all",
        params= params,
        error_message=f"Ошибка при получения вариантов из БД"
    )