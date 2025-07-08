# Работа с пользователеми
from sqlalchemy import text


def handle_student_action(db, message: dict):
    print(1)
    query = text("""
            INSERT INTO StudentActionLogs (StudentID, StudentLogin, EventType, DescriptionEvent, EventTime, IPAddress, UserAgent, Metadata)
            VALUES (:StudentID, :StudentLogin, :event_type, :description, GETDATE(), :ip_address, :user_agent, :metadata)
        """)

    db.execute(query, {
        "StudentID": message.get("StudentID"),
        "StudentLogin": message.get("StudentLogin"),
        "event_type": message.get("EventType"),
        "description": message.get("DescriptionEvent"),
        "ip_address": message.get("IPAddress"),
        "user_agent": message.get("UserAgent"),
        "metadata": message.get("Metadata"),
    })
    db.commit()
    print(f"Успешно добавлено в таблицу LogDB")
    # Здесь логика обработки действий пользователя

def handle_system_event(message: dict):
    event = message.get('event')
    print(f"Обработка системного события: {event}")
    # Здесь логика обработки системных событий
