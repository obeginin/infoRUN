--Создаем Хранимку, которая создает таблицу с задачами--
IF EXISTS(SELECT 1 FROM sys.procedures WHERE OBJECT_SCHEMA_NAME([object_id]) = 'dbo' and name = 'Create_Table_SubTasks')
	DROP PROCEDURE dbo.Create_Table_SubTasks
GO

CREATE PROCEDURE dbo.Create_Table_SubTasks
AS
BEGIN
	IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'SubTasks')
	BEGIN
		CREATE TABLE SubTasks (
		SubTaskID INT IDENTITY(1,1) PRIMARY KEY, --id подзадачи (первичный ключ)
		TaskID INT NOT NULL,  -- Связь с задачей
		SubTaskNumber INT NOT NULL,  -- Номер подзадачи (1.1, 1.2, ...)
		ImagePath NVARCHAR(255), --фото задачи
		Description NVARCHAR(MAX),  -- Описание подзадачи
		Answer NVARCHAR(32), --Ответ
		SolutionPath NVARCHAR(255), --Решение задачи
		FOREIGN KEY (TaskID) REFERENCES Tasks(TaskID) ON UPDATE CASCADE -- Внешний ключ
		);
	END
END;


/*
exec dbo.Create_Table_SubTasks
INSERT INTO SubTasks (TaskID, SubTaskNumber, Description) VALUES (1,'1.1','1 задача');
select * from SubTasks
DROP PROCEDURE dbo.Create_Table_SubTasks
drop table SubTasks
*/


