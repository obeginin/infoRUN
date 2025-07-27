 # Опеределяет какой обработчки вызвать по action_type
from handlers.students_handler import handle_student_action, handle_system_event
from handlers.email_handlers import handle_email_event
def handle_action(message: dict, db, topic: str):
    if topic == "students.actions":
        action_type = message.get('action_type')
        data = message.get("data")
        if action_type == 'student_action':
            handle_student_action(db, data) # передаём db и данные
        elif action_type == 'system_event':
            handle_system_event(db, data) # тоже передаём db и данные
        else:
            print(f"Неизвестный тип действия: {action_type}")
    elif topic == "email.notifications":
        handle_email_event(message)  # передаём весь email event
    else:
        print(f"Неизвестный топик: {topic}")


