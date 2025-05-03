from sqlalchemy.orm import Session
from Database import SessionLocal # ссылаемся на файл с конфигом БД

# Dependency
''''''
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()