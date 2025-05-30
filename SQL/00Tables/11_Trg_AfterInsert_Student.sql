/*Создаем Хранимку (ТРИГГЕР - это событие, которое будет отрабатывать при добавлении нового пользователя в базу данных (автоматичкски).--
Не работает для тех пользователей, что уже есть в базе
надо будет доработать чтобы работал если одновременно добавляют несколько учеников (хотя может это и не нужно)
работает только для одного пользователя


*/
IF EXISTS(SELECT 1 FROM sys.triggers WHERE OBJECT_SCHEMA_NAME([object_id]) = 'dbo' and name = 'trg_AfterInsertStudent')
    DROP TRIGGER dbo.trg_AfterInsertStudent
GO

--Этот блок создаёт триггер, который будет срабатывать после вставки данных в таблицу users
CREATE TRIGGER dbo.trg_AfterInsertStudent
ON dbo.Students
AFTER INSERT
AS
BEGIN
    DECLARE @StudentID BIGINT

    -- Получаем ID только что вставленного пользователя
    SELECT @StudentID = ID FROM inserted

    -- Вызов хранимой процедуры для назначения подзадач новому пользователю
    EXEC dbo.AssignSubTasksToStudent @StudentID
END;
GO

/*
посмотреть все активные триггеры 
SELECT 
    name AS trigger_name,
    parent_class_desc,
    OBJECT_NAME(parent_id) AS table_name,
    is_disabled
FROM sys.triggers
WHERE is_ms_shipped = 0;
*/


