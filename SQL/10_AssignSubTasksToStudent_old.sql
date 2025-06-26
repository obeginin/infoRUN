/*
Создаем Хранимку, которая будет создаст задачи для каждого пользователя (автоматичкски).--
Для тех, что уже есть в базе (для одного пользователя по его id)

exec dbo.AssignSubTasksToStudent @StudentID = 1 --запуск хранимки с параметром
*/
IF EXISTS(SELECT 1 FROM sys.procedures WHERE OBJECT_SCHEMA_NAME([object_id]) = 'dbo' and name = 'AssignSubTasksToStudent')
    DROP PROCEDURE dbo.AssignSubTasksToStudent
GO

CREATE PROCEDURE dbo.AssignSubTasksToStudent
    @StudentID BIGINT = NULL  -- Параметр: ID пользователя (если NULL — обрабатываем всех)
AS
BEGIN
    DECLARE @SubTaskID INT

    -- Цикл по всем подзадачам, которые нужно назначить
    DECLARE SubTaskCursor CURSOR FOR
    SELECT SubTaskID
    FROM SubTasks

    OPEN SubTaskCursor
    FETCH NEXT FROM SubTaskCursor INTO @SubTaskID

    -- Присваиваем каждую подзадачу пользователю
    WHILE @@FETCH_STATUS = 0
    BEGIN
        INSERT INTO StudentTasks (StudentID, SubTaskID, CompletionStatus)
        VALUES (@StudentID, @SubTaskID, 'Not Started')  -- Назначаем подзадачу пользователю с начальным статусом "Not Started"
        
        FETCH NEXT FROM SubTaskCursor INTO @SubTaskID
    END

    CLOSE SubTaskCursor
    DEALLOCATE SubTaskCursor
END;
GO

