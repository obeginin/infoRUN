--����� ������
/*

*/
CREATE TABLE Students (
			ID bigint IDENTITY(1,1) PRIMARY KEY, -- id ������������ (��������� ����)
			Login nvarchar(50) UNIQUE, -- ����� ������������ (����������)
			Last_Name nvarchar(50),
			First_Name nvarchar(50),
			Middle_Name nvarchar(50),
			Email nvarchar(50),
			Sex nvarchar(2),
			BirthDate datetime,
			Comment nvarchar(MAX),
			Password VARCHAR(255),  -- ��� ������
			Role nvarchar(15) 
		);

CREATE TABLE Tasks (
			TaskID INT IDENTITY(1,1) PRIMARY KEY, -- id ������ (��������� ����)
			TaskNumber INT NOT NULL UNIQUE,  -- ����� ������ (1, 2, 3... 27) �� ������ ���� ������� � ����������
			TaskTitle NVARCHAR(255) NOT NULL -- �������� ������
		);

CREATE TABLE SubTasks (
		SubTaskID INT IDENTITY(1,1) PRIMARY KEY, --id ��������� (��������� ����)
		TaskID INT NOT NULL,  -- ����� � �������
		SubTaskNumber INT NOT NULL,  -- ����� ��������� (1.1, 1.2, ...)
		ImagePath NVARCHAR(255), --���� ������
		Description NVARCHAR(MAX),  -- �������� ���������
		Answer NVARCHAR(32), --����� ������
		SolutionPath NVARCHAR(255), --������� ������
		FOREIGN KEY (TaskID) REFERENCES Tasks(TaskID) ON UPDATE CASCADE -- ������� ����
		);

CREATE TABLE StudentTasks (
		StudentTaskID INT IDENTITY(1,1) PRIMARY KEY,
		StudentID bigint NOT NULL,  -- ������
		SubTaskID INT NOT NULL,  -- ���������
		StudentAnswer NVARCHAR(32), --����� �������
		CompletionStatus NVARCHAR(20) CHECK (CompletionStatus IN ('Not Started', 'In Progress', 'Completed')),
		Score DECIMAL(5,2) NULL,  -- ����� �� ���������
		SolutionStudentPath NVARCHAR(255), --������� ������ ��������
		StartDate DATETIME NULL, -- ���� ������ ���������� �������
		ModifiedDate DATETIME NULL, -- ���� ��������� 
		CompletionDate DATETIME NULL, -- ���� ����� ��� ������� ���������� �����
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
	VALUES ('ivanov', '������', '����', '��������', 'ivanov@example.com', 'M', '1990-06-01 00:00:00.000', '�����������'),
		('petrov', '������', '����', '��������', 'petrov@example.com', 'M', '1990-07-21 00:00:00.000', '�����������'),
		('sidorov', '��������', '������', '���������', 'sidorova@example.com', '�', '1992-01-30 00:00:00.000', '�����������'),
		('smirnov', '�������', '����', '��������', 'smirnov@example.com', 'M', '1988-09-09 00:00:00.000', '�����������'),
		('andreev', '�������', '������', '���������', 'andreev@example.com', 'M', '1995-11-10 00:00:00.000', '�����������'),
		('volkov', '������', '������', '�������������', 'volkov@example.com', 'M', '1993-05-25 00:00:00.000', '�����������');
INSERT INTO Tasks (TaskNumber, TaskTitle) VALUES (1,'������ �������'),(2,'������ �������'),(3,'������ �������'),(4,'��������� �������');
INSERT INTO Tasks (TaskNumber, TaskTitle) VALUES (1,'������ �������'),(2,'������ �������'),(3,'������ �������'),(4,'��������� �������');
INSERT INTO SubTasks (TaskID, SubTaskNumber, Description) VALUES (1,'1.1','1 ������'),(1,'1.2','2 ������'),(1,'1.3','3 ������'),(2,'2.1','1 ������'),(2,'2.2','2 ������');

delete Students where id=219359
*/

INSERT INTO Students (Login, Last_Name, First_Name, Middle_Name, Email, Sex, BirthDate, Comment,Password,Role)
	VALUES ('ivanov', '������', '����', '��������', 'ivanov@example.com', 'M', '1990-06-01 00:00:00.000', '�����������','$pbkdf2-sha256$29000$HWPMube2tnYuZYwRwngPQQ$eSDzbZ3puIYCkdzcU94.2a5.ZvXUWXlIGjuSuM4ij/Y','admin'),
		('petrovv', '������', '����', '��������', 'petrov@example.com', 'M', '1990-06-01 00:00:00.000', '�����������','$pbkdf2-sha256$29000$HWPMube2tnYuZYwRwngPQQ$eSDzbZ3puIYCkdzcU94.2a5.ZvXUWXlIGjuSuM4ij/Y','student'),
		('sidorov', '��������', '������', '���������', 'sidorova@example.com', '�', '1999-09-01 00:00:00.000', '�����������','$pbkdf2-sha256$29000$HWPMube2tnYuZYwRwngPQQ$eSDzbZ3puIYCkdzcU94.2a5.ZvXUWXlIGjuSuM4ij/Y','student'),
		('smirnov', '�������', '����', '��������', 'smirnov@example.com', 'M', '2005-02-12 00:00:00.000', '�����������','$pbkdf2-sha256$29000$HWPMube2tnYuZYwRwngPQQ$eSDzbZ3puIYCkdzcU94.2a5.ZvXUWXlIGjuSuM4ij/Y','student'),
		('andreev', '�������', '������', '���������', 'andreev@example.com', 'M', '2012-02-12 00:00:00.000', '�����������','$pbkdf2-sha256$29000$HWPMube2tnYuZYwRwngPQQ$eSDzbZ3puIYCkdzcU94.2a5.ZvXUWXlIGjuSuM4ij/Y','student');

INSERT INTO Students (Login, Last_Name, First_Name, Middle_Name, Email, Sex, BirthDate, Comment,Password,Role)
	VALUES 
    
    ('alekseev','��������', '�������',  '������������','alekseev@example.com','M', '1989-09-12 00:00:00.000', '�����������','$pbkdf2-sha256$29000$HWPMube2tnYuZYwRwngPQQ$eSDzbZ3puIYCkdzcU94.2a5.ZvXUWXlIGjuSuM4ij/Y','admin'),
    ('kozlova', '�������',  '���������','���������', 'kozlova@example.com',  'F', '1995-06-23 00:00:00.000', '�����������'),
    ('morozov', '�������',  '�������',  '�������������','morozov@example.com','M', '1990-12-30 00:00:00.000', '�����������'),
	('novikova','��������', '�����',    '���������', 'novikova@example.com', 'F', '1994-11-05 00:00:00.000', '�����������'),
	('fedorova','��������', '����',     '��������',  'fedorova@example.com', 'F', '1993-01-10 00:00:00.000', '�����������');

INSERT INTO Tasks (TaskNumber, TaskTitle) VALUES (1,'������ �������'),(2,'������ �������'),(3,'������ �������'),(4,'��������� �������');
INSERT INTO Tasks (TaskNumber, TaskTitle) VALUES (5,'���_5'),(6,'���_6'),(7,'���_7'),(8,'���_8');
/*update Tasks set TaskTitle='��������� �������' where TaskID=4
delete Tasks where TaskID in (1,2,3,4) --������� ������
*/

INSERT INTO SubTasks (TaskID, SubTaskNumber, Description) 
	VALUES (1,'1.1','1 ������'),(1,'1.2','2 ������'),(1,'1.3','3 ������'),(2,'2.1','1 ������'),(2,'2.2','2 ������'),(2,'2.3','3 ������');

/*exec dbo.Create_Table_SubTasks
select * from SubTasks
drop table SubTasks
*/


/*���������� �������� � �������*/
Alter TABLE StudentTasks 
ADD
		Attempts INT DEFAULT 0
GO

Alter TABLE Students 
ADD
		Role NVARCHAR(15) --���� ������

GO

--��������� ����� �������
EXEC sp_rename 'Students.HashedPassword', 'Password', 'COLUMN';
EXEC sp_rename 'Users', 'Students';
SELECT name FROM sys.tables;
--��������� ���� ������� 
ALTER TABLE Students
ALTER COLUMN Password VARCHAR(255);


/*�������� ��������*/
CREATE NONCLUSTERED INDEX IX_StudentTasks_Student_SubTask
ON dbo.StudentTasks (StudentID, SubTaskID);
GO

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

/*�������� ���� ��� �����*/
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
    ROWTERMINATOR = '\r\n',  -- ����� ���� \n � ����������� �� �������
    FIRSTROW = 1, -- ���� ��� ���������� 1, ����� 2
	CODEPAGE = '65001'
);
/*������ �������� �������� id*/
DBCC CHECKIDENT ('StudentTasks', RESEED, 0); --8-��� id ��������� ������



SELECT *  FROM [Logus.HMS].[dbo].[Invoice] where GenericNo like '%124815%'
select * from OnlineAcquiringOperation where InvoiceGenericNo like '%124815%'


SELECT StudentTaskID,StudentID, Login, SubTaskID,CompletionStatus,Score,CompletionDate,StudentAnswer 
                 FROM StudentTasks 
                 JOIN Students ON Students.ID = StudentTasks.StudentID 
                 WHERE StudentTasks.StudentID = 1
--������ �� ��������� ������ ��������
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