--������� ��������, ������� ����� ��� ������ ������������ ��������� ������ (�������!!!)--
IF EXISTS(SELECT 1 FROM sys.procedures WHERE OBJECT_SCHEMA_NAME([object_id]) = 'dbo' and name = 'AddStudentWithTasks')
	DROP PROCEDURE dbo.AddStudentWithTasks
GO
CREATE PROCEDURE dbo.AddStudentWithTasks
    @Login NVARCHAR(50),
    @Last_Name NVARCHAR(50),
    @First_Name NVARCHAR(50),
    @Middle_Name NVARCHAR(50),
    @Email NVARCHAR(50),
    @Sex NVARCHAR(2),
    @BirthDate DATETIME,
    @Comment NVARCHAR(MAX)
AS
BEGIN
    SET NOCOUNT ON;

    -- ��������� ������������
    INSERT INTO Students (Login, Last_Name, First_Name, Middle_Name, Email, Sex, BirthDate, Comment)
    VALUES (@Login, @Last_Name, @First_Name, @Middle_Name, @Email, @Sex, @BirthDate, @Comment);

    -- �������� ID ������ ��� ������������ ������������
    DECLARE @NewUserID BIGINT = SCOPE_IDENTITY();

    -- ��������� ������ � StudentTasks ��� ���� ��������
    INSERT INTO StudentTasks (StudentID, SubTaskID, CompletionStatus)
    SELECT @NewUserID, SubTaskID, 'Not Started'
    FROM SubTasks;
END;


/*
EXEC AddStudentWithTasks
    @Login = 'ivanov01',
    @Last_Name = '������',
    @First_Name = '����',
    @Middle_Name = '���������',
    @Email = 'ivanov@example.com',
    @Sex = '�',
    @BirthDate = '2000-01-01',
    @Comment = '����� �������';
*/