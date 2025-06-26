/*Создаем Хранимку (ТРИГГЕР - это событие, которое будет отрабатывать при добавлении новой подзадачи в базу данных (автоматичкски).--
Не работает для тех задач, что уже есть в базе


Для проверки
INSERT INTO SubTasks (TaskID, SubTaskNumber, Description) VALUES (3, '3', 'Описание333333');
select * from SubTasks
select * from StudentTasks
*/

IF EXISTS (SELECT 1 FROM sys.triggers WHERE OBJECT_SCHEMA_NAME([object_id]) = 'dbo' AND name = 'trg_AfterInsertSubTask')
    DROP TRIGGER dbo.trg_AfterInsertSubTask;
GO

CREATE TRIGGER dbo.trg_AfterInsertSubTask
ON dbo.SubTasks
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    -- Вставка новых записей в StudentTasks для каждой подзадачи и каждого студента
    INSERT INTO StudentTasks (StudentID, SubTaskID, CompletionStatus)
    SELECT 
        s.ID AS StudentID,
        i.SubTaskID,
        'Не приступал'
    FROM Students s
    CROSS JOIN inserted i
    WHERE NOT EXISTS (
        SELECT 1 
        FROM StudentTasks st
        WHERE st.StudentID = s.ID AND st.SubTaskID = i.SubTaskID
    );
END;
GO