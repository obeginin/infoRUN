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
			--Role nvarchar(15), -- роль (админс, user) СТАРОЕ УДАЛИТЬ!!!!
			RoleID INT NOT NULL, -- id роли
			FOREIGN KEY (RoleID) REFERENCES Roles(RoleID)
		);
	END
END;


EXEC sp_help 'Students';
--по умолчанию проставляем роль "Ученик"
ALTER TABLE Students
ADD CONSTRAINT DF_Students_RoleID DEFAULT 3 FOR RoleID;
update Students set RoleID=3
/*
select * from students
Добавить новый столбец
ALTER TABLE Students ADD RoleID INT;
Добавить внешний ключ по этому столбцу
ALTER TABLE Students
ADD CONSTRAINT FK_Students_RoleID FOREIGN KEY (RoleID) REFERENCES Roles(RoleID);

ALTER TABLE Students
ADD CONSTRAINT DF_Students_RoleID DEFAULT 3 FOR RoleID;
DROP PROCEDURE Create_Table_Students

drop table Students

INSERT INTO Students (Login, Last_Name, First_Name, Middle_Name, Email, Sex, BirthDate, Comment,Password,Role)
	VALUES 

INSERT INTO Students (Login, Last_Name, First_Name, Middle_Name, Email, Sex, BirthDate, Comment,Password,Role)
	VALUES ('obeginin', 'Бегинин', 'Олег', 'Вячеславович', 'lezhik.from@gmail.com', 'M', '', 'Комментарий','$pbkdf2-sha256$29000$3zunFMK4955zjpEyxngPYQ$nECQLRTK9OFP8I6QErp5iVHRy6D4j4/mC7IgkxDGTEY','admin'),
	('jkochetova', 'Кочетова', 'Юлия', 'Вячеславовна', 'petrov@example.com', 'Ж', '', 'Комментарий','$pbkdf2-sha256$29000$3zunFMK4955zjpEyxngPYQ$nECQLRTK9OFP8I6QErp5iVHRy6D4j4/mC7IgkxDGTEY','admin'),
		('petr', 'Петров', 'Петр', 'Петрович', 'petrov@example.com', 'M', '', 'Комментарий','$pbkdf2-sha256$29000$N4bwvvceQ2gtBaD03htDyA$BLHTA0T4Q.f1kZMSLoQjTm1.Pr7hUMpK/dFKMtDdAkk','student'),
		('stepa', 'Степанов', 'Степан', 'Степанович', 'sidorova@example.com', 'М', '', 'Комментарий','$pbkdf2-sha256$29000$N4bwvvceQ2gtBaD03htDyA$BLHTA0T4Q.f1kZMSLoQjTm1.Pr7hUMpK/dFKMtDdAkk','student'),
		('ivan', 'Иванов', 'Иван', 'Иванович', 'smirnov@example.com', 'M', '', 'Комментарий','$pbkdf2-sha256$29000$N4bwvvceQ2gtBaD03htDyA$BLHTA0T4Q.f1kZMSLoQjTm1.Pr7hUMpK/dFKMtDdAkk','student'),
		('rustam', 'Рустамов', 'Рустам', 'Рустамович', 'andreev@example.com', 'M', '', 'Комментарий','$pbkdf2-sha256$29000$N4bwvvceQ2gtBaD03htDyA$BLHTA0T4Q.f1kZMSLoQjTm1.Pr7hUMpK/dFKMtDdAkk','student'),
		('test', 'Тестов', 'Тест', 'Тестович', 'test@gmail.com', 'M', '', 'Комментарий','$pbkdf2-sha256$29000$N4bwvvceQ2gtBaD03htDyA$BLHTA0T4Q.f1kZMSLoQjTm1.Pr7hUMpK/dFKMtDdAkk','student');

*/
INSERT INTO Students (Login, Last_Name, First_Name, Middle_Name, Email, Sex, BirthDate, Comment,Password,Role) 
VALUES ('test1', 'Тестов', 'Тест', 'Тестович', 'test@gmail.com', 'M', '', 'Комментарий','$pbkdf2-sha256$29000$N4bwvvceQ2gtBaD03htDyA$BLHTA0T4Q.f1kZMSLoQjTm1.Pr7hUMpK/dFKMtDdAkk','student');