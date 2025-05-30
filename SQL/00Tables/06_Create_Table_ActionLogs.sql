--Создаем Хранимку на создание таблицы для логирования--
IF EXISTS(SELECT 1 FROM sys.procedures WHERE OBJECT_SCHEMA_NAME([object_id]) = 'dbo' and name = 'Create_Table_ActionLogs')
    DROP PROCEDURE dbo.Create_Table_ActionLogs
GO

CREATE PROCEDURE dbo.Create_Table_ActionLogs
AS
BEGIN
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'ActionLogs')
    BEGIN
        CREATE TABLE ActionLogs (
            LogID INT IDENTITY(1,1) PRIMARY KEY,  -- уникальный идентификатор записи лога
            ActionType NVARCHAR(100),  -- тип действия (например, "Создание задачи")
            Description NVARCHAR(MAX),  -- описание действия
            LogDate DATETIME DEFAULT GETDATE()  -- дата и время действия
        );
    END
END;
GO