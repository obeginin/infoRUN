from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

from sqlalchemy.orm import Session
from sqlalchemy import text
from Database import SessionLocal

# Открываем сессию
db: Session = SessionLocal()

try:
    # Сырой SELECT через сессию
    result_users = db.execute(text("SELECT * FROM users"))
    users = result_users.fetchall()

    result_tasks = db.execute(text("SELECT * FROM tasks"))
    tasks = result_tasks.fetchall()

    print("✅ Данные из users:")
    for u in users:
        print(u)

    print("\n✅ Данные из tasks:")
    for t in tasks:
        print(t)

except Exception as e:
    print("❌ Ошибка:", e)

finally:
    db.close()  # Не забудь закрыть сессию!



'''
Через engine.connect()  
DATABASE_URL = (
    "mssql+pyodbc://localhost/BASE"
    "?driver=ODBC+Driver+18+for+SQL+Server"

    "&trusted_connection=yes"
    "&TrustServerCertificate=yes")
engine = create_engine(DATABASE_URL)  # функция create_engine создаёт объект соединения с базой данных.



try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * from users"))
        users = result.fetchall()
        print("Успешное подключение! ✅ Результат:")
        for i in users:
            print(i)
except Exception as e:
    print("❌ Ошибка подключения:", e)'''

