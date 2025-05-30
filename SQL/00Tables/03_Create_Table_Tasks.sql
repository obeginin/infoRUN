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
			TaskID INT IDENTITY(1,1) PRIMARY KEY, -- id задачи (первичный ключ)
			TaskNumber INT NOT NULL UNIQUE,  -- Номер задачи (1, 2, 3... 27) не должен быть нулевым и уникальным
			TaskTitle NVARCHAR(255) NOT NULL -- Название задачи
		);
	END
END;

/*
DROP PROCEDURE Create_Table_Tasks --удалить хранимку

drop table Tasks --удалить таблицу (вместе с данными)
SELECT name FROM sys.tables; --вывод всех таблиц БД

вставляем данные в таблицу
INSERT INTO Tasks (TaskNumber, TaskTitle) VALUES (1,'первое задание'),(2,'второе задание'),(3,'третье задание'),(4,'четвертое задание');
update Tasks set TaskTitle='четвертое задание' where TaskID=4
delete Tasks where TaskID in (1,2,3,4) --удаляем строки


ALTER TABLE Tasks
ALTER COLUMN TaskNumber INT NOT NULL ;

select * from users
select * from Tasks
select * from SubTasks
select * from StudentTasks



*/