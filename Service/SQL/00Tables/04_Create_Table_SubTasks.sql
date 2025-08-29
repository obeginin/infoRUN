
IF EXISTS(SELECT 1 FROM sys.procedures WHERE OBJECT_SCHEMA_NAME([object_id]) = 'dbo' and name = 'Create_Table_SubTasks')
	DROP PROCEDURE dbo.Create_Table_SubTasks
GO

CREATE PROCEDURE dbo.Create_Table_SubTasks
AS
BEGIN
	IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'SubTasks')
	BEGIN
		CREATE TABLE SubTasks (
		SubTaskID INT IDENTITY(1,1) PRIMARY KEY,				-- id задачи 
		TaskID INT NOT NULL,									-- id категории
		SubTaskNumber INT NOT NULL,								-- типы задач в данной категории (1.1, 1.2, ...)
		VariantID INT,											-- id варианта
		ImagePath NVARCHAR(255),								-- адрес с изображением задачи
		Description NVARCHAR(MAX),								-- описание задачи
		Answer NVARCHAR(32),									-- ответ задачи (НАДО ПЕРЕНСТИ В ОТДЕЛЬНУЮ ТАБЛИЦУ)
		SolutionPath NVARCHAR(255),								-- адрес с решением задачи
		FOREIGN KEY (TaskID) REFERENCES Tasks(TaskID) ON UPDATE CASCADE,		 -- внешний ключ на id категории
		FOREIGN KEY (VariantID) REFERENCES Variants(VariantID) ON UPDATE CASCADE -- внешний ключ на id варианта
		);
	END
END;



/*
exec dbo.Create_Table_SubTasks
INSERT INTO SubTasks (TaskID, SubTaskNumber, Description) VALUES (1,'1.1','1 ������');
select * from SubTasks
DROP PROCEDURE dbo.Create_Table_SubTasks
drop table SubTasks
*/



CREATE TABLE SubTasksImages (
	ID INT IDENTITY(1,1) PRIMARY KEY,
	SubTaskID INT REFERENCES SubTasks(SubTaskID) ON DELETE CASCADE,
	FileName NVARCHAR(255) NOT NULL,
	FilePath NVARCHAR(500) NOT NULL,
	UploadDate DATETIME DEFAULT GETDATE()
	);

CREATE TABLE SubTaskFiles (
	ID INT PRIMARY KEY IDENTITY,
	SubTaskID INT FOREIGN KEY REFERENCES SubTasks(SubTaskID),
	FileName NVARCHAR(255),
	FilePath NVARCHAR(500),
	UploadDate DATETIME DEFAULT GETDATE()
	);

CREATE TABLE SubTaskSolutions (
	ID INT IDENTITY(1,1) PRIMARY KEY,
	SubTaskID INT REFERENCES SubTasks(SubTaskID) ON DELETE CASCADE,
	FileName NVARCHAR(255) NOT NULL,
	FilePath NVARCHAR(500) NOT NULL,
	UploadDate DATETIME DEFAULT GETDATE()
	);