/*
Создаем Хранимку, которая будет создавать задачи для каждого пользователя (автоматичкски).--
в данном случае работает в двух состояних:
если передать параметр в виде пользователя, то создаст для конкретного student
если запусить хранимку без параметров, значит выполнится для всех пользователей, что есть в базе

exec dbo.AssignSubTasksToStudent @StudentID = 7 --запуск хранимки с параметром (для одного пользователя)
EXEC dbo.AssignSubTasksToStudent;  --запуск хранимки БЕЗ параметров (для всех имеющихся пользователя)
AssignSubTasksToStudent
*/
IF EXISTS(SELECT 1 FROM sys.procedures WHERE OBJECT_SCHEMA_NAME([object_id]) = 'dbo' AND name = 'AssignSubTasksToStudent')
    DROP PROCEDURE dbo.AssignSubTasksToStudent
GO

CREATE PROCEDURE dbo.AssignSubTasksToStudent
    @StudentID BIGINT = NULL  -- Параметр: ID пользователя (если NULL — обрабатываем всех)
AS
BEGIN
    SET NOCOUNT ON;

    -- Массовое добавление: если @StudentID IS NULL
    IF @StudentID IS NULL
    BEGIN
        INSERT INTO StudentTasks (StudentID, SubTaskID, CompletionStatus)
        SELECT 
            sd.ID AS StudentID,
            s.SubTaskID,
            'Не приступал'
        FROM Students sd
        CROSS JOIN SubTasks s
        WHERE 
		NOT EXISTS ( -- Проверка на то, что данных записей ещё нет 
            SELECT 1 
            FROM StudentTasks st 
            WHERE st.StudentID = sd.ID AND st.SubTaskID = s.SubTaskID
        )
    END
    ELSE
    BEGIN
        -- Добавление задач только для одного пользователя
        INSERT INTO StudentTasks (StudentID, SubTaskID, CompletionStatus)
        SELECT 
            @StudentID,
            s.SubTaskID,
            'Не приступал'
        FROM SubTasks s
        WHERE NOT EXISTS ( -- Проверка на то, что данных записей ещё нет 
            SELECT 1 
            FROM StudentTasks st 
            WHERE st.StudentID = @StudentID AND st.SubTaskID = s.SubTaskID
        )
    END
END;
GO