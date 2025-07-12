

-- сохраняем данные для отправки уведомления в базу с логами
CREATE TABLE PendingNotifications (
    NotificationID INT IDENTITY(1,1) PRIMARY KEY,
    StudentID INT NOT NULL,
    SubTaskID INT NULL,
    TaskID INT NULL,
    Message NVARCHAR(255) NOT NULL,
    Deadline DATE NOT NULL,
    CreatedAt DATETIME DEFAULT GETDATE(),
    Status NVARCHAR(50) DEFAULT 'waiting'
);

select * from PendingNotifications