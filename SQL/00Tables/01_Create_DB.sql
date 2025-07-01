--Создаем Хранимку, которая создает базу данных BASE--
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'infoRUN')
BEGIN
    CREATE DATABASE infoRUN;
	CREATE DATABASE LogDB;
END
GO  -- Разделяем блоки

USE infoRUN
GO  -- Указываем использование базы


