--Создаем Хранимку, которая создает базу данных BASE--
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'BASE')
BEGIN
    CREATE DATABASE BASE;
END
GO  -- Разделяем блоки

USE BASE
GO  -- Указываем использование базы


