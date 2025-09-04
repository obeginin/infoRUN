--Общий скрипт
/*

*/
CREATE TABLE Students (
			ID bigint IDENTITY(1,1) PRIMARY KEY, -- id пользователя (первичный ключ)
			Login nvarchar(50) UNIQUE, -- логин пользователя (уникальный)
			Last_Name nvarchar(50),
			First_Name nvarchar(50),
			Middle_Name nvarchar(50),
			Email nvarchar(50),
			Sex nvarchar(2),
			BirthDate datetime,
			Comment nvarchar(MAX),
			Password VARCHAR(255),  -- Хеш пароля
			Role nvarchar(15) 
		);

CREATE TABLE Tasks (
			TaskID INT IDENTITY(1,1) PRIMARY KEY, -- id задачи (первичный ключ)
			TaskNumber INT NOT NULL UNIQUE,  -- Номер задачи (1, 2, 3... 27) не должен быть нулевым и уникальным
			TaskTitle NVARCHAR(255) NOT NULL -- Название задачи
		);

CREATE TABLE SubTasks (
		SubTaskID INT IDENTITY(1,1) PRIMARY KEY, --id подзадачи (первичный ключ)
		TaskID INT NOT NULL,  -- Связь с задачей
		SubTaskNumber INT NOT NULL,  -- Номер подзадачи (1.1, 1.2, ...)
		ImagePath NVARCHAR(255), --фото задачи
		Description NVARCHAR(MAX),  -- Описание подзадачи
		Answer NVARCHAR(32), --Ответ задачи
		SolutionPath NVARCHAR(255), --Решение задачи
		FOREIGN KEY (TaskID) REFERENCES Tasks(TaskID) ON UPDATE CASCADE -- Внешний ключ
		);

CREATE TABLE StudentTasks (
		StudentTaskID INT IDENTITY(1,1) PRIMARY KEY,
		StudentID bigint NOT NULL,  -- Ученик
		SubTaskID INT NOT NULL,  -- Подзадача
		StudentAnswer NVARCHAR(32), --Ответ ученика
		CompletionStatus NVARCHAR(20) CHECK (CompletionStatus IN ('Not Started', 'In Progress', 'Completed')),
		Score DECIMAL(5,2) NULL,  -- Баллы за подзадачу
		SolutionStudentPath NVARCHAR(255), --Решение задачи Студента
		StartDate DATETIME NULL, -- Дата начала выполнения задания
		ModifiedDate DATETIME NULL, -- Дата зименения 
		CompletionDate DATETIME NULL, -- Дата когда был получен правильный ответ
		FOREIGN KEY (StudentID) REFERENCES Students(ID),
		FOREIGN KEY (SubTaskID) REFERENCES SubTasks(SubTaskID)
		);

CREATE TABLE ActionLogs (
    LogID INT IDENTITY(1,1) PRIMARY KEY,
    ActionType NVARCHAR(100),
    Description NVARCHAR(MAX),
    LogDate DATETIME DEFAULT GETDATE()
);
/*
INSERT INTO Students (Login, Last_Name, First_Name, Middle_Name, Email, Sex, BirthDate, Comment)
	VALUES ('ivanov', 'Иванов', 'Иван', 'Иванович', 'ivanov@example.com', 'M', '1990-06-01 00:00:00.000', 'Комментарий'),
		('petrov', 'Петров', 'Петр', 'Петрович', 'petrov@example.com', 'M', '1990-07-21 00:00:00.000', 'Комментарий'),
		('sidorov', 'Сидорова', 'Сидора', 'Сидоровна', 'sidorova@example.com', 'Ж', '1992-01-30 00:00:00.000', 'Комментарий'),
		('smirnov', 'Смирнов', 'Смир', 'Смирович', 'smirnov@example.com', 'M', '1988-09-09 00:00:00.000', 'Комментарий'),
		('andreev', 'Андреев', 'Андрей', 'Андреевич', 'andreev@example.com', 'M', '1995-11-10 00:00:00.000', 'Комментарий'),
		('volkov', 'Волков', 'Володи', 'Володимирович', 'volkov@example.com', 'M', '1993-05-25 00:00:00.000', 'Комментарий');
INSERT INTO Tasks (TaskNumber, TaskTitle) VALUES (1,'первое задание'),(2,'второе задание'),(3,'третье задание'),(4,'четвертое задание');
INSERT INTO Tasks (TaskNumber, TaskTitle) VALUES (1,'первое задание'),(2,'второе задание'),(3,'третье задание'),(4,'четвертое задание');
INSERT INTO SubTasks (TaskID, SubTaskNumber, Description) VALUES (1,'1.1','1 задача'),(1,'1.2','2 задача'),(1,'1.3','3 задача'),(2,'2.1','1 задача'),(2,'2.2','2 задача');

delete Students where id=219359
*/

INSERT INTO Students (Login, Last_Name, First_Name, Middle_Name, Email, Sex, BirthDate, Comment,Password,Role)
	VALUES ('obeginin', 'Бегинин', 'Олег', 'Вячеславович', 'lezhik.from@gmail.com', 'M', '', 'Комментарий','$pbkdf2-sha256$29000$3zunFMK4955zjpEyxngPYQ$nECQLRTK9OFP8I6QErp5iVHRy6D4j4/mC7IgkxDGTEY','admin'),
	('jkochetova', 'Кочетова', 'Юлия', 'Вячеславовна', 'petrov@example.com', 'Ж', '', 'Комментарий','$pbkdf2-sha256$29000$3zunFMK4955zjpEyxngPYQ$nECQLRTK9OFP8I6QErp5iVHRy6D4j4/mC7IgkxDGTEY','admin'),
		('petr', 'Петров', 'Петр', 'Петрович', 'petrov@example.com', 'M', '', 'Комментарий','$pbkdf2-sha256$29000$N4bwvvceQ2gtBaD03htDyA$BLHTA0T4Q.f1kZMSLoQjTm1.Pr7hUMpK/dFKMtDdAkk','student'),
		('stepa', 'Степанов', 'Степан', 'Степанович', 'sidorova@example.com', 'М', '', 'Комментарий','$pbkdf2-sha256$29000$N4bwvvceQ2gtBaD03htDyA$BLHTA0T4Q.f1kZMSLoQjTm1.Pr7hUMpK/dFKMtDdAkk','student'),
		('ivan', 'Иванов', 'Иван', 'Иванович', 'smirnov@example.com', 'M', '', 'Комментарий','$pbkdf2-sha256$29000$N4bwvvceQ2gtBaD03htDyA$BLHTA0T4Q.f1kZMSLoQjTm1.Pr7hUMpK/dFKMtDdAkk','student'),
		('rustam', 'Рустамов', 'Рустам', 'Рустамович', 'andreev@example.com', 'M', '', 'Комментарий','$pbkdf2-sha256$29000$N4bwvvceQ2gtBaD03htDyA$BLHTA0T4Q.f1kZMSLoQjTm1.Pr7hUMpK/dFKMtDdAkk','student');

INSERT INTO Students (Login, Last_Name, First_Name, Middle_Name, Email, Sex, BirthDate, Comment,Password,Role)
	VALUES 
    
    ('alekseev','Алексеев', 'Алексей',  'Владимирович','alekseev@example.com','M', '1989-09-12 00:00:00.000', 'Комментарий','$pbkdf2-sha256$29000$HWPMube2tnYuZYwRwngPQQ$eSDzbZ3puIYCkdzcU94.2a5.ZvXUWXlIGjuSuM4ij/Y','admin'),
    ('kozlova', 'Козлова',  'Екатерина','Андреевна', 'kozlova@example.com',  'F', '1995-06-23 00:00:00.000', 'Комментарий'),
    ('morozov', 'Морозов',  'Дмитрий',  'Станиславович','morozov@example.com','M', '1990-12-30 00:00:00.000', 'Комментарий'),
	('novikova','Новикова', 'Мария',    'Сергеевна', 'novikova@example.com', 'F', '1994-11-05 00:00:00.000', 'Комментарий'),
	('fedorova','Федорова', 'Анна',     'Игоревна',  'fedorova@example.com', 'F', '1993-01-10 00:00:00.000', 'Комментарий');

INSERT INTO Tasks (TaskNumber, TaskTitle) VALUES (1,'первое задание'),(2,'второе задание'),(3,'третье задание'),(4,'четвертое задание');
INSERT INTO Tasks (TaskNumber, TaskTitle) VALUES (5,'ЕГЭ_5'),(6,'ЕГЭ_6'),(7,'ЕГЭ_7'),(8,'ЕГЭ_8');
/*update Tasks set TaskTitle='четвертое задание' where TaskID=4
delete Tasks where TaskID in (1,2,3,4) --удаляем строки
*/

INSERT INTO SubTasks (TaskID, SubTaskNumber, Description) 
	VALUES (1,'1.1','1 задача'),(1,'1.2','2 задача'),(1,'1.3','3 задача'),(2,'2.1','1 задача'),(2,'2.2','2 задача'),(2,'2.3','3 задача');

/*exec dbo.Create_Table_SubTasks
select * from SubTasks
drop table SubTasks
*/


/*Добавление столбцов в таблицу*/
Alter TABLE StudentTasks 
ADD
		Attempts INT DEFAULT 0
GO

Alter TABLE Students 
ADD
		Role NVARCHAR(15) --фото задачи

GO

--изменение имени столбца
EXEC sp_rename 'Students.HashedPassword', 'Password', 'COLUMN';
EXEC sp_rename 'Users', 'Students';
SELECT name FROM sys.tables;
--изменение типа столбца 
ALTER TABLE Students
ALTER COLUMN Password VARCHAR(255);


/*создание индексов*/
CREATE NONCLUSTERED INDEX IX_StudentTasks_Student_SubTask
ON dbo.StudentTasks (StudentID, SubTaskID);
GO

--Обновление адреса файла
select * from SubTasks where SubTaskID =180
update  SubTasks set ImagePath='Uploads/images/task_57_sub_3.png' where SubTaskID =57

select * from Students
select * from Tasks
select * from SubTasks  
select * from StudentTasks where StudentID=2 and SubTaskID=3
SELECT * FROM SubTasks where TaskID=1 ORDER BY SubTaskNumber
SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Students';
select * from Tasks
SELECT StudentTaskID,StudentID, Login, SubTaskID,CompletionStatus,Score,CompletionDate,StudentAnswer FROM StudentTasks 
join Students on ID=StudentID
where studentID=2
SELECT * FROM Students IS NULL;
UPDATE SubTasks SET ImagePath='Uploads\task_4_sub_2.png'  where SubTaskID=33
delete SubTasks
SELECT SubTaskID, TaskID, SubTaskNumber, ImagePath, Description, Answer, SolutionPath FROM SubTasks ORDER BY TaskID
SELECT MAX(SubTaskNumber) FROM SubTasks WHERE TaskID =1
SELECT MAX(SubTaskNumber) FROM SubTasks WHERE TaskID=2
update Students set Role='student' where id=5
update Students set Password='$pbkdf2-sha256$29000$HWPMube2tnYuZYwRwngPQQ$eSDzbZ3puIYCkdzcU94.2a5.ZvXUWXlIGjuSuM4ij/Y' where id=4
SELECT * FROM StudentTasks 
join Students on ID=StudentID
where studentID=2

/*изменяем путь для файла*/
update SubTasks set ImagePath='Uploads\images\task_1_sub_1.png' where SubTaskID=5   
select * from SubTasks  where SubTaskID=5


SELECT Answer FROM SubTasks where SubTaskID
UPDATE Students SET  = '$2b$12$8/9g9mTJK1Ro8oZPzy4FOOQcPf1VZgf0sH6xB6WQrB9ZH5FTZxQ9W'
WHERE login = 'ivanov';

/*
drop table StudentTasks
drop table SubTasks
drop table Tasks
drop table Students


select * from Users
delete Users where id >8
*/

BULK INSERT Users
FROM 'C:\t.csv'
WITH (
    FIELDTERMINATOR = ';',
    ROWTERMINATOR = '\r\n',  -- может быть \n в зависимости от системы
    FIRSTROW = 1, -- если нет заголовков 1, иначе 2
	CODEPAGE = '65001'
);
/*Задать значение нумераци id*/
DBCC CHECKIDENT ('StudentTasks', RESEED, 0); --8-это id последней записи



SELECT *  FROM [Logus.HMS].[dbo].[Invoice] where GenericNo like '%124815%'
select * from OnlineAcquiringOperation where InvoiceGenericNo like '%124815%'


SELECT StudentTaskID,StudentID, Login, SubTaskID,CompletionStatus,Score,CompletionDate,StudentAnswer 
                 FROM StudentTasks 
                 JOIN Students ON Students.ID = StudentTasks.StudentID 
                 WHERE StudentTasks.StudentID = 1
--запрос на получения задачи студента
select 
	st.StudentTaskID, 
	st.StudentID,
	st.SubTaskID,
	st.StudentAnswer,
	st.CompletionStatus, 
	st.Score,
	st.CompletionDate,
	sd.Login,
	sd.Role,
	s.TaskID,
	s.SubTaskNumber,
	s.ImagePath,
	s.Description,
	s.Answer,
	s.SolutionPath
from StudentTasks st
	join Students sd on sd.ID=st.StudentID 
	join SubTasks s on s.SubTaskID=st.SubTaskID
where st.StudentTaskID=2