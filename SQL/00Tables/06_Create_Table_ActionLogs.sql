--—оздаем ’ранимку на создание таблицы дл¤ логировани¤--
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
            ActionType NVARCHAR(100),  -- тип действи¤ (например, "—оздание задачи")
            Description NVARCHAR(MAX),  -- описание действи¤
            LogDate DATETIME DEFAULT GETDATE()  -- дата и врем¤ действи¤
        );
    END
END;
GO