from sqlalchemy import text
from Database import SessionLocal
'''Выполнение хранимых процедур'''
# Открываем сессию
db = SessionLocal()

try:
    # Чтение SQL-скриптов с хранимыми процедурами
    with open(r"C:\Users\obeginin\Desktop\учебники\Скрипты SQL\BASE\02_Create_Table_Users.sql", "r") as file:
        procedure1 = file.read()

    # Выполнение хранимой процедуры
    db.execute(text(procedure1))
    db.commit()  # Коммитим, если нужно
    print("Процедура выполнена успешно!")

except Exception as e:
    print(f"❌ Ошибка при выполнении хранимой процедуры: {str(e)}")
    db.rollback()  # Откатываем изменения в случае ошибки

finally:
    db.close()  # Закрываем сессию