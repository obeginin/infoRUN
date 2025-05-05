from sqlalchemy.orm import Session
from sqlalchemy import text
from Models import Student
from Schemas.students import StudentTaskRead
# Crud\Students.py
''' 
CRUD - основная логика работы запроса
описываем функции, которые выполняют SQL запросы к БД, результат возвращается в виде кортежа
'''

''' Получение всех студентов'''
def get_all_students(db: Session):
    query = text(f"SELECT * FROM Students")
    result = db.execute(query).fetchall()
    return result

''' Получения студента по ID'''
def get_student_id(db: Session, Student_id: int):
    query = text(f"SELECT * FROM Students where ID={Student_id}")
    result = db.execute(query).fetchall()
    return result

''' Получения всех задач всех студентов '''
def get_all_students_tasks(db: Session):
    query = text("SELECT * FROM StudentTasks")
    result = db.execute(query).fetchall()
    student_tasks = [
        {"StudentTaskID": row.StudentTaskID,
        "StudentID": row.StudentID,
         "SubTaskID": row.SubTaskID,
         "CompletionStatus": row.CompletionStatus,
         "Score": row.Score,
         "CompletionDate": row.CompletionDate,
         "StudentAnswer": row.StudentAnswer}
        for row in result]
    return student_tasks

''' Получения всех задач студента по ID'''
def get_student_all_tasks(db: Session, student_id: int):
    query = text(f"SELECT StudentTaskID,StudentID, Login, SubTaskID,CompletionStatus,Score,CompletionDate,StudentAnswer FROM StudentTasks join Students on ID=StudentID where studentID={student_id}")
    result = db.execute(query).fetchall()
    student_tasks = [
        {"StudentTaskID": row.StudentTaskID,
        "StudentID": row.StudentID,
         "Login": row.Login,
         "SubTaskID": row.SubTaskID,
         "CompletionStatus": row.CompletionStatus,
         "Score": row.Score,
         "CompletionDate": row.CompletionDate,
         "StudentAnswer": row.StudentAnswer}
        for row in result]
    return student_tasks


''' Получения задачи студента по SubTaskID'''
def get_task_student(db: Session, student_id: int, SubTaskID: int) -> list[StudentTaskRead]:
    query = text(f"select * from StudentTasks join Students on ID=StudentID where StudentID={student_id} and SubTaskID={SubTaskID}")
    result = db.execute(query).fetchall()
    task_student = [
        {"StudentTaskID": row.StudentTaskID,
        "StudentID": row.StudentID,
         "Login": row.Login,
         "SubTaskID": row.SubTaskID,
         "CompletionStatus": row.CompletionStatus,
         "Score": row.Score,
         "CompletionDate": row.CompletionDate,
         "StudentAnswer": row.StudentAnswer}
        for row in result]
    return task_student