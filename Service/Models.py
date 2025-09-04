from sqlalchemy import Column, BigInteger, Integer, String, DateTime, ForeignKey, DECIMAL, Boolean, func, Text
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
    Phone = Column(String(25))
    Sex = Column(String(2))  # Пол
    BirthDate = Column(DateTime)  # Дата рождения
    Comment = Column(String)  # Комментарий
    Password = Column(String) # пароль
    RoleID = Column(Integer, default=3)  # Подзадача
    IsActive = Column(Boolean, nullable=False, default=True)
    IsDeleted = Column(DateTime, nullable=True, default=None)
    IsConfirmed = Column(Boolean, default=False)




class EmailLog(Base):
    __tablename__ = "EmailLogs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_type = Column(String(255), nullable=True)
    to_email = Column(String(255), nullable=False)
    subject = Column(String(255), nullable=False)
    template_name = Column(String(255), nullable=True)
    body = Column(Text, nullable=True)
    status = Column(String(50), default="pending")  # pending / sent / failed
    error_message = Column(String, nullable=True)
    retry_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
