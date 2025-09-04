-- Подключаем расширение для генерации UUID
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Создание таблицы EmailLogs
CREATE TABLE IF NOT EXISTS EmailLogs (
    id SERIAL PRIMARY KEY,
    event_type VARCHAR(255),
    to_email VARCHAR(255),
    subject VARCHAR(255),
    body TEXT,
    status VARCHAR(50) DEFAULT 'pending',
    sent_at TIMESTAMP NULL,
    error_message TEXT NULL,
    retry_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    task_uuid UUID NOT NULL DEFAULT gen_random_uuid()
);

-- Создание уникального индекса для task_uuid
CREATE UNIQUE INDEX IF NOT EXISTS IX_EmailLogs_TaskUUID ON EmailLogs(task_uuid);

-- Функция для автообновления updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Триггер, который вызывает функцию при UPDATE
DROP TRIGGER IF EXISTS TR_EmailLogs_Update ON EmailLogs;

CREATE TRIGGER TR_EmailLogs_Update
BEFORE UPDATE ON EmailLogs
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();