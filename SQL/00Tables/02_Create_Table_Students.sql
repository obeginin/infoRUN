/*
exec Create_Table_Students --Выполнить хранимку
*/
IF EXISTS(SELECT 1 FROM sys.procedures WHERE OBJECT_SCHEMA_NAME([object_id]) = 'dbo' and name = 'Create_Table_Students')
	DROP PROCEDURE dbo.Create_Table_Students
GO

--Создаем Хранимку, которая создает таблицу Students--
CREATE PROCEDURE Create_Table_Students
AS
BEGIN
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Students')
	BEGIN
		CREATE TABLE Students (
			ID bigint IDENTITY(1,1) PRIMARY KEY, -- id пользователя (первичный ключ)
			Login nvarchar(50) UNIQUE, -- логин пользователя (уникальный)
			Last_Name nvarchar(50),
			First_Name nvarchar(50),
			Middle_Name nvarchar(50),
			Email nvarchar(50),
			Sex nvarchar(2),
			BirthDate datetime,
			Comment nvarchar(MAX),
			Password VARCHAR(255),-- Хеш пароля (надо сделать NOT NULL)
			Role nvarchar(15) -- роль (админс, user)
		);
	END
END;

/*


DROP PROCEDURE Create_Table_Students

drop table Students
*/
