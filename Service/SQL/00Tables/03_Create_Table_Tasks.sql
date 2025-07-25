IF EXISTS(SELECT 1 FROM sys.procedures WHERE OBJECT_SCHEMA_NAME([object_id]) = 'dbo' and name = 'Create_Table_Tasks')
	DROP PROCEDURE dbo.Create_Table_Tasks
GO
--exec Create_Table_Tasks --Выполнить хранимку

CREATE PROCEDURE Create_Table_Tasks
AS
BEGIN
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Tasks')
	BEGIN
		CREATE TABLE Tasks (
			TaskID INT IDENTITY(1,1) PRIMARY KEY,		-- id категории (первичный ключ)
			SubjectID INT NOT NULL,						-- id предмета
			TaskNumber INT NOT NULL UNIQUE,				-- Номер задачи (1, 2, 3... 27) обязательно уникальный и не должен быть нулевым 
			TaskTitle NVARCHAR(255) NOT NULL			-- Название категории
			FOREIGN KEY (SubjectID) REFERENCES Subjects(ID)
		);
	END
END;


IF EXISTS(SELECT 1 FROM sys.procedures WHERE OBJECT_SCHEMA_NAME([object_id]) = 'dbo' and name = 'Create_Table_Subjects')
	DROP PROCEDURE dbo.Create_Table_Subjects
GO
--exec Create_Table_Subjects --Выполнить хранимку

CREATE PROCEDURE Create_Table_Subjects
AS
BEGIN
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Subjects')
	BEGIN
		CREATE TABLE Subjects (
			ID INT IDENTITY(1,1) PRIMARY KEY,			-- id предмета
			Name NVARCHAR(100) NOT NULL UNIQUE,			-- название предмет
			Description NVARCHAR(MAX) NULL				-- описание предмета
		);
	END
END;

/*
SELECT * FROM Subjects

INSERT INTO Subjects (Name, Description) VALUES
  (N'Математика', N'Подготовка к ЕГЭ по математике'),
  (N'Русский язык', N'Подготовка к ЕГЭ по русскому языку'),
  (N'Физика', N'Подготовка к ЕГЭ по физике'),
  (N'Химия', N'Подготовка к ЕГЭ по химии'),
  (N'Биология', N'Подготовка к ЕГЭ по биологии'),
  (N'История', N'Подготовка к ЕГЭ по истории'),
  (N'Обществознание', N'Подготовка к ЕГЭ по обществознанию'),
  (N'Литература', N'Подготовка к ЕГЭ по литературе'),
  (N'Английский язык', N'Подготовка к ЕГЭ по английскому языку'),
  (N'Информатика', N'Подготовка к ЕГЭ по информатике');
  */







/*
DROP PROCEDURE Create_Table_Tasks --удалить хранимку

drop table Tasks --удалить таблицу (вместе с данными)
SELECT name FROM sys.tables; --вывод всех таблиц БД

вставляем данные в таблицу
INSERT INTO Tasks (TaskNumber, TaskTitle) 
VALUES 
	(1,'ЕГЭ_1'),(2,'ЕГЭ_2'),(3,'ЕГЭ_3'),(4,'ЕГЭ_4'),(5,'ЕГЭ_5'),(6,'ЕГЭ_6'),(7,'ЕГЭ_7'),(8,'ЕГЭ_8');

INSERT INTO Tasks (TaskNumber, TaskTitle) VALUES (1,'первое задание'),(2,'второе задание'),(3,'третье задание'),(4,'четвертое задание');

Автоматическая втавка строк от 1 до 27
WITH Numbers AS (
    SELECT 1 AS n
    UNION ALL
    SELECT n + 1 FROM Numbers WHERE n < 27
)
INSERT INTO Tasks (TaskNumber, TaskTitle)
SELECT n, CONCAT('ЕГЭ_', n)
FROM Numbers
OPTION (MAXRECURSION 0);

update Tasks set TaskTitle='четвертое задание' where TaskID=4
delete Tasks where TaskID in (1,2,3,4) --удаляем строки


ALTER TABLE Tasks
ALTER COLUMN TaskNumber INT NOT NULL ;

select * from users
select * from Tasks
select * from SubTasks
select * from StudentTasks



*/