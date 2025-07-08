from Database import SessionLocal # ссылаемся на файл с конфигом БД

# Dependency.py
'''файл с зависимостями '''

'''Зависимость для получения базы данных'''
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()