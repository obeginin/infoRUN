 #Опеределяет какой обработчки вызвать по action_type
from handlers.students_handler import handle_student_action, handle_system_event

def handle_action(message: dict, db):
    action_type = message.get('action_type')
    data = message.get("data")
    print("роут handle_action")
    if action_type == 'student_action':
        handle_student_action(db, data)    # передаём db и данные
    elif action_type == 'system_event':
        handle_system_event(db, data)      # тоже передаём db и данные
    else:
        print(f"Неизвестный тип сообщения: {action_type}")

