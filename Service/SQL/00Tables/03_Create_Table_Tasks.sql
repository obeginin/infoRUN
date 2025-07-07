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