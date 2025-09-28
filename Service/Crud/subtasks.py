from utils.config import settings
from utils import errors,general

from sqlalchemy.ext.asyncio import AsyncSession
from Service.Schemas import subtasks as subtasks_schema
from sqlalchemy import text
from fastapi import HTTPException, UploadFile, File
from typing import Optional
import shutil
import json
import os
from pathlib import Path
import logging
from typing import List
from uuid import uuid4
import base64


# Crud\subtasks.py

logger = logging.getLogger(__name__)
# TODO переведен на асинхронный postgres (кроме функции save_files - надо подумать)


async def view_all_subtasks(db: AsyncSession, params: dict, mode = 'mappings_all'):
    """Вызывает функцию Posgtres get_subtasks, передавая только непустые параметры. Все остальные берутся по умолчанию из функции в PostgreSQL."""
    logger.debug("=== Запуск функции view_all_subtasks ===")
    logger.debug(f"Фильтры: {params}")

    # Оставляем только те параметры, которые реально пришли
    filtered_params = {k: v for k, v in params.items() if v is not None}

    # Формируем список аргументов для SQL
    args_sql = [f'"{k}" := :{k}' for k in filtered_params.keys()]

    query = f"""SELECT * FROM get_subtasks({', '.join(args_sql)})"""
    # Выполняем запрос, передаём только непустые параметры
    return await general.run_query_select(
        db=db,
        query=query,
        params=filtered_params,
        mode=mode,  # вернёт список словарей
        required=False,
        error_message="Не удалось получить список всех задач"
    )


async def view_files(db: AsyncSession, subtask_id):
    '''Получение всех файлов задачи по её id'''
    logger.debug(f"=== Запуск функции view_files с subtask_id: {subtask_id}===")
    return await general.run_query_select(
        db=db,
        query="""select * from "SubTaskFiles" where "SubTaskID" = :subtask_id""",
        params={"subtask_id": subtask_id},
        mode="mappings_all",
        required=False,
        error_message=f"Не удалось получить файлы для задачи с id:{subtask_id}"
    )

'''Скорей всего уберем (перевели на celery)'''
async def view_solutions_files(db: AsyncSession, subtask_id):
    logger.debug("=== Запуск функции view_solutions_files ===")
    logger.debug(f"Полученные файлов с решением задачи с subtask_id: {subtask_id}")
    query = """SELECT "ID", "FileName", "FilePath", "UploadDate" FROM "SubTaskSolutions"
        WHERE "SubTaskID" = :subtask_id"""
    params = {"subtask_id": subtask_id}
    return await general.run_query_select(
        db=db,
        query=query,
        params=params,
        mode="mappings_all",  # Возвращаем список словарей
        required=False,
        error_message=f"Не удалось получить файлы для задачи с id:{subtask_id}"
    )

async def create_subtask(db: AsyncSession, subtask_obj, files_blocks: list):
        #blocks_json = json.dumps([b.dict() for b in subtask_obj.Blocks])
    logger.debug(f"=== Запуск функции create_subtask ===")
    logger.info(f"Полученные данные подзадачи: {subtask_obj}")
    logger.info(f"Количество загруженных файлов с изображением задачи: {len(files_blocks)}")
    #logger.info(f"Количество загруженных файлов с решением задачи: {len(files_solution)}")
    #logger.info(f"Количество загруженных дополнительных файлов к задаче: {len(files)}")
    for f in files_blocks:
        logger.info(f"Файл: {f.filename}")
    try:
        # 1 Вставка основной подзадачи
        insert_subtask_query = """
            INSERT INTO "SubTasks" ("TaskID", "SubTaskNumber", "VariantID", "Creator")
            VALUES (:TaskID, :SubTaskNumber, :VariantID, :Creator)
            RETURNING "SubTaskID";
            """
        params_subtask = {
            "TaskID": subtask_obj.TaskID,
            "SubTaskNumber": subtask_obj.SubTaskNumber,
            "VariantID": subtask_obj.VariantID,
            "Creator": subtask_obj.Creator
        }
        logger.info(f"[SUBTASKS_CRUD] Добавляем строку в таблицу SubTasks с параметрами: {params_subtask}")
        subtask_id = await general.run_query_insert(
            db,
            insert_subtask_query,
            params_subtask,
            commit=False,
            return_id=True
        )
        # ставка ответа на задачу
        await general.run_query_insert(
            db,
            query=""" insert into "SubTaskAnswers" ("SubTaskID", "AnswerText", "AnswerType") 
                    Values (:SubTaskID, :AnswerText, :AnswerType) """,
            params={"SubTaskID": subtask_id, "AnswerText":subtask_obj.Answer, "AnswerType": 'text'}, # TODO: AnswerType прописан гвознядми
            commit=False,
        )

        logger.info(f"[SUBTASKS_CRUD] Подзадача вставлена с ID {subtask_id}")

        # Сохраняем файлы и создаем записи в таблицах
        # TODO: оставляем пока синхронной
        file_url_map = save_files(db, files_blocks, subtask_id, settings.UPLOAD_IMAGE_DIR, "subtask", "SubTasksImages")
        #file_url_map_2 = save_files(files_solution, UPLOAD_SOLUTION_DIR, "sol_subtask", "SubTaskSolutions")
        #ile_url_map_3 = save_files(files, UPLOAD_FILES_DIR, "f_subtask", "SubTaskFiles")


        logger.debug(f"[SUBTASKS_CRUD] Обновление блоков. Исходные блоки: {subtask_obj.Blocks}")
        # 3 Обновляем блоки (заменяем пути к картинкам)
        updated_blocks = []
        image_idx = 0
        for block in subtask_obj.Blocks:
            block_dict = block.dict()
            if block_dict["type"] == "image":
                if image_idx < len(files_blocks):
                    block_dict["content"] = file_url_map[image_idx]
                    image_idx += 1
                else:
                    logger.warning(f"[SUBTASKS_CRUD] Файл для блока не найден: {block_dict}")
            updated_blocks.append(block_dict)

        update_subtask_query = """
                UPDATE "SubTasks"
                SET "Blocks" = :Blocks
                WHERE "SubTaskID" = :SubTaskID
                """
        params_2 = {
            "Blocks": json.dumps(updated_blocks, ensure_ascii=False),
            "SubTaskID": subtask_id
        }
        logger.debug(f"Обновление задачи c subtask_id={subtask_id} с блоками: {params_2}")
        await general.run_query_update(db, update_subtask_query, params_2, commit=False)
        await db.commit()

        #return subtask_id
        return {
            "SubTaskID": subtask_id,
            "Blocks": updated_blocks,
        }

    except Exception as e:
        await db.rollback()
        logger.exception(f"Ошибка при создании подзадачи, откат изменений")
        raise errors.internal_server(message=f"Ошибка при создании подзадачи, откат изменений")



async def update_subtask(db: AsyncSession, subtask_obj, files_blocks: list, files_solution: list, files_extra: list, subtask_id: int):
    """
    Полное обновление подзадачи.
    subtask_obj — объект с новыми данными (TaskID, SubTaskNumber, VariantID, Answer, Blocks)
    files_blocks — список новых файлов для блоков (заменяем старые)
    subtask_id — ID подзадачи для обновления
    """
    logger.debug(f"=== Запуск функции update_subtask с subtask_id={subtask_id}===")

    try:
        # 1. Удаляем старые файлы и записи
        await delete_subtask_files(db, subtask_id)


        logger.info(f"[SUBTASKS_CRUD] 0")
        # 2. Сохраняем новые файлы для блоков
        file_url_map = []
        if files_blocks:
            file_url_map = save_files(db, files_blocks, subtask_id, settings.UPLOAD_IMAGE_DIR, "subtask", "SubTasksImages")
        logger.info(f"[SUBTASKS_CRUD] 1")
        # 3. Обновляем блоки с новыми путями
        updated_blocks = []
        image_idx = 0
        for block in subtask_obj.Blocks:
            block_dict = block.dict() if hasattr(block, "dict") else dict(block)
            if block_dict.get("type") == "image" and files_blocks:
                if image_idx < len(file_url_map):
                    block_dict["content"] = file_url_map[image_idx]
                    image_idx += 1
                else:
                    logger.warning(f"[SUBTASKS_CRUD] Нет соответствующего файла для блока: {block_dict}")
                    block_dict["content"] = ""
            updated_blocks.append(block_dict)
        logger.info(f"[SUBTASKS_CRUD] 2")
        # 4. Проверяем, что все блоки сериализуемы
        serializable_blocks = []
        for b in updated_blocks:
            if isinstance(b, dict):
                serializable_blocks.append(b)
            else:
                logger.warning(f"[SUBTASKS_CRUD] Блок не сериализуем, заменяем на пустой dict: {b}")
                serializable_blocks.append({})
        logger.info(f"[SUBTASKS_CRUD] 3")
        # 4. Обновляем всю подзадачу целиком
        subtask_query = """
            UPDATE "SubTasks"
            SET "TaskID" = :TaskID,
                "SubTaskNumber" = :SubTaskNumber,
                "VariantID" = :VariantID,
                "Blocks" = :Blocks
            WHERE "SubTaskID" = :SubTaskID
        """
        subtask_params = {
            "TaskID": subtask_obj.TaskID,
            "SubTaskNumber": subtask_obj.SubTaskNumber,
            "VariantID": subtask_obj.VariantID,
            "Blocks": json.dumps(serializable_blocks, ensure_ascii=False),
            "SubTaskID": subtask_id
        }
        await general.run_query_update(db, subtask_query, subtask_params,commit=False)

        await general.run_query_insert(
            db,
            query=""" insert into "SubTaskAnswers" ("SubTaskID", "AnswerText", "AnswerType") 
                            Values (:SubTaskID, :AnswerText, :AnswerType) """,
            params={"SubTaskID": subtask_id, "AnswerText": subtask_obj.Answer, "AnswerType": 'text'},
            # TODO: AnswerType прописан гвознядми
            commit=False,
        )

        await db.commit()

        logger.debug(f"Обновление задачи c subtask_id={subtask_id} ")
        return {
            "SubTaskID": subtask_id,
            "Blocks": updated_blocks,
        }

    except Exception as e:
        logger.exception(f"Ошибка при обновлении задачи с subtask_id={subtask_id} {str(e)}")
        raise errors.internal_server(message=f"Ошибка при обновлении задачи с subtask_id={subtask_id} ")




async def delete_subtask_files(db: AsyncSession, subtask_id: int):
    """
    Удаляет все файлы подзадачи из всех таблиц и с диска.
    Пути в базе хранятся относительно корня проекта.
    """
    logger.debug(f"=== Запуск функции delete_subtask_files с subtask_id={subtask_id}===")

    tables_folders = [
        ("SubTasksImages", settings.UPLOAD_IMAGE_DIR),
        ("SubTaskSolutions", settings.UPLOAD_SOLUTION_DIR),
        ("SubTaskFiles", settings.UPLOAD_FILES_DIR),
    ]
    logger.info(f"{settings.UPLOAD_IMAGE_DIR}, {settings.UPLOAD_SOLUTION_DIR}, {settings.UPLOAD_FILES_DIR}")

    for table, folder_path in tables_folders:
        logger.info(f"table {table} folder_path:{folder_path}")
        files_in_db = await general.run_query_select(
            db,
            f"""SELECT "FilePath" FROM "{table}" WHERE "SubTaskID" = :SubTaskID""",
            {"SubTaskID": subtask_id},
            mode="mappings_all"
        ) or []
        logger.info(f"{files_in_db}")

        # Удаляем записи из базы
        await general.run_query_delete(
            db,
            f"""DELETE FROM "{table}" WHERE "SubTaskID" = :SubTaskID""",
            {"SubTaskID": subtask_id},
            commit=False
        )
        logger.debug(f"[SUBTASKS_CRUD] Удалены записи из таблицы {table} для SubTaskID={subtask_id}")

        await general.run_query_delete(
            db,
            f"""DELETE FROM "SubTaskAnswers" WHERE "SubTaskID" = :SubTaskID""",
            {"SubTaskID": subtask_id},
            commit=False
        )
        await db.commit()
        if not files_in_db:
            logger.info(f"[SUBTASKS_CRUD] В таблице {table} для SubTaskID={subtask_id} файлов нет")
            continue

        for f in files_in_db:
            logger.info(f"[SUBTASKS_CRUD] Проверка записи из БД: {f} (тип {type(f)})")
            try:
                relative_path = f['FilePath']
                filename = os.path.basename(relative_path)

                if table == "SubTasksImages":
                    folder_path = settings.UPLOAD_IMAGE_DIR
                elif table == "SubTaskSolutions":
                    folder_path = settings.UPLOAD_SOLUTION_DIR
                else:
                    folder_path = settings.UPLOAD_FILES_DIR

                full_path = os.path.join(folder_path, filename)
                if os.path.exists(full_path):
                    os.remove(full_path)
                    logger.info(f"[SUBTASKS_CRUD] Удален файл с диска: {full_path}")
                else:
                    logger.warning(f"[SUBTASKS_CRUD] Файл не найден на диске: {full_path}")
            except Exception as e:
                logger.warning(f"[SUBTASKS_CRUD] Не удалось удалить файл {f}: {e}")

    logger.info(f"[SUBTASKS_CRUD] Удаление файлов для подзадачи ID={subtask_id} завершено ✅")


async def delete_subtask_record(db: AsyncSession, subtask_id: int):
    """
    Удаляет запись подзадачи из таблицы SubTasks.
    """
    logger.debug(f"=== Запуск функции delete_subtask_record с subtask_id={subtask_id}===")
    query = """DELETE FROM "SubTasks" WHERE "SubTaskID" = :SubTaskID"""
    deleted_count = await general.run_query_delete(
        db,
        query,
        {"SubTaskID": subtask_id},
        commit=True,
        error_message=f"Не удалось удалить подзадачу ID={subtask_id}"
    )

    if deleted_count == 0:
        logger.warning(f"[SUBTASKS_CRUD] Подзадача ID={subtask_id} не найдена в базе")
    else:
        logger.info(f"[SUBTASKS_CRUD] Удалена запись подзадачи ID={subtask_id}")

# TODO: СИНХРОННАЯ!!!
'''функция сохранения файлов'''
def save_files(db, files: list, subtask_id: int, folder: str, prefix: str, table: str):
    logger.debug(f"=== Запуск функции save_files с subtask_id={subtask_id}===")
    file_map = {}
    for idx, file in enumerate(files or []):
        ext = file.filename.split('.')[-1]
        filename = f"{prefix}_{subtask_id}_{idx+1}.{ext}"
        full_path = os.path.join(folder, filename)
        try:
            with open(full_path, "wb") as f:
                shutil.copyfileobj(file.file, f)
            logger.info(f"[SUBTASKS_CRUD] Файл сохранен: {filename}")
        except Exception:
            logger.exception(f"[SUBTASKS_CRUD] Ошибка при сохранении файла {file.filename}")
            continue

        # Относительный путь для базы и URL
        relative_path = os.path.relpath(full_path, settings.UPLOADS_DIR).replace("\\", "/")

        db_path = f"Uploads/{relative_path}"  # сохраняем в базу
        file_map[idx] = f"/{db_path}"  # для фронта


        insert_query = f"INSERT INTO {table} (SubTaskID, FileName, FilePath) VALUES (:SubTaskID, :FileName, :FilePath)"
        general.run_query_insert(db, insert_query, {"SubTaskID": subtask_id, "FileName": filename, "FilePath": db_path})

    return file_map

async def prepare_files_data(files: List[UploadFile], file_type: str = "file") -> list:
    """
    Преобразует список UploadFile в сериализуемый список с base64 и логирует каждый файл.
    Args:
        files: список UploadFile
        file_type: строка для логов, например "решение" или "дополнительный"

    Returns:
        list: список словарей с filename, content_type и base64-данными
    """
    logger.debug("=== Запуск функции prepare_files_data ===")

    files_data = []
    for idx, f in enumerate(files, start=1):
        content = await f.read()
        files_data.append({
            "filename": f.filename,
            "content_type": f.content_type,
            "data": base64.b64encode(content).decode('utf-8')
        })
        logger.info(f"{file_type.capitalize()} файл {idx}: {f.filename}, content_type={f.content_type}, size={len(content)} bytes")
    return files_data


'''Логирование и проверка списка файлов (для проверки передачи файлов с фронта)'''
async def log_and_validate_files(files: Optional[List], label: str):
    logger.debug("=== Запуск функции log_and_validate_files ===")
    count = len(files) if files else 0
    logger.info(f"Получено файлов ({label}): {count}")

    for idx, file in enumerate(files or [], start=1):
        filename = getattr(file, "filename", None)
        logger.info(f"Файл {idx} ({label}): {filename if filename else 'None'}")
        if not filename:
            logger.warning(f"Файл без имени пропущен ({label})")



# TODO: пока не нужна, но может пригодтся (перенес логику записи в Celery)
'''Сохраняет список файлов во временную директорию с уникальными именами'''
async def save_temp_files(files: List[UploadFile], target_dir: Path) -> List[str]:
    logger.debug("=== Запуск функции save_temp_files ===")
    """
    files: Список файлов .
    target_dir: Директория, куда будут сохранены файлы.
    return: Список путей к сохранённым файлам.
    """
    saved_paths = []
    target_dir.mkdir(parents=True, exist_ok=True)  # гарантируем, что папка существует
    logger.info(f"[SUBTASKS] Сохраняем файлы в папку: {target_dir.resolve()}")
    for idx, file in enumerate(files or [], start=1):                        # перебираем файлы
        unique_name = f"{uuid4()}_{file.filename}"  # создаем уникальное имя для файла с оригинальным окончанием
        temp_path = target_dir / unique_name        # формируем путь (директория + имя)

        # Сохраняем файл
        with open(temp_path, "wb") as f:
            f.write(await file.read())

        saved_paths.append(str(temp_path))          # путь добавляем в список как строку
        logger.info(f"[SUBTASKS] Файл {idx}: {file.filename} сохранён как {unique_name}")
    logger.info(f"[SUBTASKS] Всего файлов сохранено: {len(saved_paths)}")
    return saved_paths

# TODO: пока не нужна, но может пригодтся (перенес логику записи в Celery)
"""Сохраняет временные пути файлов подзадачи в таблицу SubTaskTemp и возвращает ID записи"""
async def save_subtask_temp_record(db: AsyncSession, subtask_id: int, student_id: int, temp_solution_paths: list, temp_files_paths: list) -> int:
    logger.debug(f"=== Запуск функции save_subtask_temp_record для задачи с subtask_id={subtask_id}===")
    logger.info(f"Добавляем запись о временных файлах в таблицу SubTaskTemp")
    insert_query = """
        INSERT INTO "SubTaskTemp" ("SubTaskID", "StudentID", "SolutionTempPath", "FilesTempPaths")
        OUTPUT INSERTED."ID"
        VALUES (:SubTaskID, :StudentID, :SolutionTempPath, :FilesTempPaths)
    """

    inserted_id = await general.run_query_insert(
        db=db,
        query=insert_query,
        params={
            "SubTaskID": subtask_id,
            "StudentID": student_id,
            "SolutionTempPath": json.dumps(temp_solution_paths),
            "FilesTempPaths": json.dumps(temp_files_paths)
        },
        return_id=True
    )

    return inserted_id