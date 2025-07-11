from sqlalchemy import Column, BigInteger, Integer, String, DateTime, ForeignKey, DECIMAL, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Models.py
'''В данном файле описываем все таблицы аналогично таблица из базы данных
данные модели используются для ORM работы
'''

Base = declarative_base()
# Модель для таблицы Students



class Student(Base):
    __tablename__ = 'Students'

    ID = Column(BigInteger, primary_key=True, autoincrement=True)  # ID пользователя. autoincrement=True (автоназначение)
    Login = Column(String(50), unique=True, index=True)  # Логин пользователя
    Last_Name = Column(String(50))  # Фамилия
    First_Name = Column(String(50))  # Имя
    Middle_Name = Column(String(50))  # Отчество
    Email = Column(String(50))  # Email
    Sex = Column(String(2))  # Пол
    BirthDate = Column(DateTime)  # Дата рождения
    Comment = Column(String)  # Комментарий
    Password = Column(String) # пароль
    RoleID = Column(Integer, default=3)  # Подзадача
    IsActive = Column(Boolean, nullable=False, default=True)
    IsDeleted = Column(DateTime, nullable=True, default=None)

# Модель для таблицы Tasks
class Task(Base):
    __tablename__ = 'Tasks'

    TaskID = Column(Integer, primary_key=True, autoincrement=True)  # ID задачи
    TaskNumber = Column(Integer, unique=True, nullable=False)  # Номер задачи
    TaskTitle = Column(String(255), nullable=False)  # Название задачи

# Модель для таблицы SubTasks
class SubTask(Base):
    __tablename__ = 'SubTasks'

    SubTaskID = Column(Integer, primary_key=True, autoincrement=True)  # ID подзадачи
    TaskID = Column(Integer, ForeignKey('Tasks.TaskID'), nullable=False)  # Связь с задачей
    SubTaskNumber = Column(Integer, nullable=False)  # Номер подзадачи
    ImagePath = Column(String(255))  # Путь к изображению
    Description = Column(String)  # Описание подзадачи
    Answer = Column(String(32))  # Ответ
    SolutionPath = Column(String(255))  # Путь к решению задачи

    # Связь с моделью Task
    task = relationship('Task', backref='subtasks')
    files = relationship("SubTaskFiles", back_populates="subtask")
# Модель для таблицы StudentTasks
class StudentTask(Base):
    __tablename__ = 'StudentTasks'

    StudentTaskID = Column(Integer, primary_key=True, autoincrement=True)  # ID задачи студента
    StudentID = Column(BigInteger, ForeignKey('Students.ID'), nullable=False)  # Студент
    SubTaskID = Column(Integer, ForeignKey('SubTasks.SubTaskID'), nullable=False)  # Подзадача
    StudentAnswer = Column(String(32))  # Ответ студента
    CompletionStatus = Column(String(20), nullable=False)  # Статус выполнения
    Score = Column(DECIMAL(5, 2), nullable=True)  # Баллы
    CompletionDate = Column(DateTime, nullable=True)  # Дата выполнения
    SolutionStudentPath = Column(String(255), nullable=True)  # путь к решению студента

    # Связь с пользователем (студентом)
    student = relationship('Student', backref='student_tasks')

class SubTaskFiles(Base):
    __tablename__ = "SubTaskFiles"

    ID = Column(Integer, primary_key=True, index=True)
    SubTaskID = Column(Integer, ForeignKey("SubTasks.SubTaskID"))
    FileName = Column(String)
    FilePath = Column(String)
    UploadDate = Column(DateTime, nullable=True)

    subtask = relationship("SubTask", back_populates="files")


