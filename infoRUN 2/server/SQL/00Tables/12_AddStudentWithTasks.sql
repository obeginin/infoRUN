--Создаем Хранимку, которая будет для нового пользователя добавлять задачи (ВРУЧНУЮ!!!)--
IF EXISTS(SELECT 1 FROM sys.procedures WHERE OBJECT_SCHEMA_NAME([object_id]) = 'dbo' and name = 'AddStudentWithTasks')
	DROP PROCEDURE dbo.AddStudentWithTasks
GO
CREATE PROCEDURE dbo.AddStudentWithTasks
    @Login NVARCHAR(50),
    @Last_Name NVARCHAR(50),
    @First_Name NVARCHAR(50),
    @Middle_Name NVARCHAR(50),
    @Email NVARCHAR(50),
    @Sex NVARCHAR(2),
    @BirthDate DATETIME,
    @Comment NVARCHAR(MAX)
AS
BEGIN
    SET NOCOUNT ON;

    -- Добавляем пользователя
    INSERT INTO Students (Login, Last_Name, First_Name, Middle_Name, Email, Sex, BirthDate, Comment)
    VALUES (@Login, @Last_Name, @First_Name, @Middle_Name, @Email, @Sex, @BirthDate, @Comment);

    -- Получаем ID только что добавленного пользователя
    DECLARE @NewUserID BIGINT = SCOPE_IDENTITY();

    -- Вставляем записи в StudentTasks для всех подзадач
    INSERT INTO StudentTasks (StudentID, SubTaskID, CompletionStatus)
    SELECT @NewUserID, SubTaskID, 'Not Started'
    FROM SubTasks;
END;


/*
EXEC AddStudentWithTasks
    @Login = 'ivanov01',
    @Last_Name = 'Иванов',
    @First_Name = 'Иван',
    @Middle_Name = 'Сергеевич',
    @Email = 'ivanov@example.com',
    @Sex = 'М',
    @BirthDate = '2000-01-01',
    @Comment = 'Новый студент';
*/