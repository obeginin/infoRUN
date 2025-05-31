/*
exec Create_Table_Students --��������� ��������
*/
IF EXISTS(SELECT 1 FROM sys.procedures WHERE OBJECT_SCHEMA_NAME([object_id]) = 'dbo' and name = 'Create_Table_Students')
	DROP PROCEDURE dbo.Create_Table_Students
GO

--������� ��������, ������� ������� ������� Students--
CREATE PROCEDURE Create_Table_Students
AS
BEGIN
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Students')
	BEGIN
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
			Password VARCHAR(255),-- ��� ������ (���� ������� NOT NULL)
			Role nvarchar(15) -- ���� (������, user)
		);
	END
END;

/*


DROP PROCEDURE Create_Table_Students

drop table Students

INSERT INTO Students (Login, Last_Name, First_Name, Middle_Name, Email, Sex, BirthDate, Comment,Password,Role)
	VALUES 

INSERT INTO Students (Login, Last_Name, First_Name, Middle_Name, Email, Sex, BirthDate, Comment,Password,Role)
	VALUES ('obeginin', '�������', '����', '������������', 'lezhik.from@gmail.com', 'M', '', '�����������','$pbkdf2-sha256$29000$3zunFMK4955zjpEyxngPYQ$nECQLRTK9OFP8I6QErp5iVHRy6D4j4/mC7IgkxDGTEY','admin'),
	('jkochetova', '��������', '����', '������������', 'petrov@example.com', '�', '', '�����������','$pbkdf2-sha256$29000$3zunFMK4955zjpEyxngPYQ$nECQLRTK9OFP8I6QErp5iVHRy6D4j4/mC7IgkxDGTEY','admin'),
		('petr', '������', '����', '��������', 'petrov@example.com', 'M', '', '�����������','$pbkdf2-sha256$29000$N4bwvvceQ2gtBaD03htDyA$BLHTA0T4Q.f1kZMSLoQjTm1.Pr7hUMpK/dFKMtDdAkk','student'),
		('stepa', '��������', '������', '����������', 'sidorova@example.com', '�', '', '�����������','$pbkdf2-sha256$29000$N4bwvvceQ2gtBaD03htDyA$BLHTA0T4Q.f1kZMSLoQjTm1.Pr7hUMpK/dFKMtDdAkk','student'),
		('ivan', '������', '����', '��������', 'smirnov@example.com', 'M', '', '�����������','$pbkdf2-sha256$29000$N4bwvvceQ2gtBaD03htDyA$BLHTA0T4Q.f1kZMSLoQjTm1.Pr7hUMpK/dFKMtDdAkk','student'),
		('rustam', '��������', '������', '����������', 'andreev@example.com', 'M', '', '�����������','$pbkdf2-sha256$29000$N4bwvvceQ2gtBaD03htDyA$BLHTA0T4Q.f1kZMSLoQjTm1.Pr7hUMpK/dFKMtDdAkk','student'),
		('test', '������', '����', '��������', 'test@gmail.com', 'M', '', '�����������','$pbkdf2-sha256$29000$N4bwvvceQ2gtBaD03htDyA$BLHTA0T4Q.f1kZMSLoQjTm1.Pr7hUMpK/dFKMtDdAkk','student');

*/
