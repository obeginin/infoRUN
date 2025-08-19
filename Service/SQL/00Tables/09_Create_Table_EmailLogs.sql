-- таблица для статуса отправки задач
CREATE TABLE EmailLogs (
    id INT IDENTITY PRIMARY KEY,
    event_type VARCHAR(255),
    to_email VARCHAR(255),
    subject VARCHAR(255),
	body NVARCHAR(MAX) NULL,
    status VARCHAR(50) DEFAULT 'pending', --  / sent / failed
	sent_at DATETIME NULL,
    error_message NVARCHAR(MAX) NULL,
	retry_count INT DEFAULT 0,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE(),
	task_uuid UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID()
);
ALTER TABLE EmailLogs ADD body NVARCHAR(MAX) NULL;


ALTER TABLE EmailLogs
ADD task_uuid UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID();
-- чтобы гарантировать, что не будет дубликатов
CREATE UNIQUE INDEX IX_EmailLogs_TaskUUID ON EmailLogs(task_uuid);



-- Триггер для автообновления updated_at
CREATE TRIGGER TR_EmailLogs_Update
ON EmailLogs
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE e
    SET updated_at = GETDATE()
    FROM EmailLogs e
    INNER JOIN inserted i ON e.id = i.id;
END;