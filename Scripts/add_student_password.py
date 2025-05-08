''' скрипт для заполнения паролей уже имеющихся пользователей'''
from sqlalchemy.orm import Session
from Database import SessionLocal
from Models import Student
from Security.password import hash_password


def add_passwords_to_students(db: Session):
    students = db.query(Student).filter(Student.Password == None).all()

    if not students:
        print("Нет студентов без пароля!")
        return

    for student in students:
        plain_password = "default123"  # временный пароль
        student.Password = hash_password(plain_password)
        #student.Password = (plain_password)
        print(f"Установлен пароль для {student.Login}")
        db.add(student)

    db.commit()
    print(f"Пароли для {len(students)} студентов обновлены!")
    db.close()


if __name__ == "__main__":
    # Получаем сессию для работы с базой данных
    db = SessionLocal()

    try:
        add_passwords_to_students(db)
    finally:
        db.close()