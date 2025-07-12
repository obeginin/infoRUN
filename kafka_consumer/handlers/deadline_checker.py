from datetime import datetime
from sqlalchemy import text
import logging

logger = logging.getLogger(__name__)
"""
def check_deadlines(db):
    today = datetime.utcnow().date()
    try:
        result = db.execute(text("
            SELECT * FROM StudentTasks
            WHERE DeadlineDate = :today AND CompletionStatus != 'Выполнено'
        "), {"today": today}).mappings().all()

        for task in result:
            db.execute(text("
                        INSERT INTO PendingNotifications (StudentID, SubTaskID, TaskID, Message, Deadline)
                        VALUES (:StudentID, :SubTaskID, :TaskID, :Message, :Deadline)
                    "), {
                "StudentID": task["StudentID"],
                "SubTaskID": task.get("SubTaskID"),
                "TaskID": task.get("TaskID"),
                "Message": "Сегодня срок выполнения задания!",
                "Deadline": task["DeadlineDate"]
            })
        db.commit()
        logger.info(f"Добавлено {len(result)} уведомлений в PendingNotifications")
    except Exception:
        logger.exception("Ошибка при проверке дедлайнов задач")
"""