--создаем хранимку на создание таблицы для логирования--
IF EXISTS(SELECT 1 FROM sys.procedures WHERE OBJECT_SCHEMA_NAME([object_id]) = 'dbo' and name = 'Create_Table_StudentActionLogs')
    DROP PROCEDURE dbo.Create_Table_StudentActionLogs
GO

CREATE PROCEDURE dbo.Create_Table_StudentActionLogs
AS
BEGIN
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'StudentActionLogs')
    BEGIN
        CREATE TABLE StudentActionLogs (
			LogID INT IDENTITY PRIMARY KEY,
			StudentID INT NOT NULL,
			StudentLogin NVARCHAR(50) NOT NULL,
			EventType NVARCHAR(50) NOT NULL,            -- тип действия: login_success, task_viewed, profile_updated
			DescriptionEvent NVARCHAR(100),				-- описание действия
			EventTime DATETIME DEFAULT GETDATE(),
			IPAddress NVARCHAR(45),
			UserAgent NVARCHAR(MAX),
			Metadata NVARCHAR(MAX)                      -- хранит специфичные поля в виде JSON
		);
    END
END;
GO
/*
exec Create_Table_StudentActionLogs

drop table StudentActionLogs
*/
select * from StudentActionLogs
