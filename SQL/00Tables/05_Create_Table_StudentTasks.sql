IF EXISTS(SELECT 1 FROM sys.procedures WHERE OBJECT_SCHEMA_NAME([object_id]) = 'dbo' and name = 'Create_Table_StudentTasks')
	DROP PROCEDURE dbo.Create_Table_StudentTasks
GO

--������� ��������, ������� ������� ������� � ��������--
CREATE PROCEDURE Create_Table_StudentTasks
AS
BEGIN
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'StudentTasks')
	BEGIN
		CREATE TABLE StudentTasks (
		StudentTaskID INT IDENTITY(1,1) PRIMARY KEY,
		StudentID bigint NOT NULL,  -- ������
		SubTaskID INT NOT NULL,  -- ���������
		StudentAnswer NVARCHAR(32), --����� �������
		CompletionStatus NVARCHAR(20) CHECK (CompletionStatus IN ('�� ���������', '� ��������', '���������')),
		Score DECIMAL(5,2) NULL,  -- ����� �� ���������
		SolutionStudentPath NVARCHAR(255), --������� ������ ��������
		StartDate DATETIME NULL, -- ���� ������ ���������� �������
		ModifiedDate DATETIME NULL, -- ���� ��������� 
		CompletionDate DATETIME NULL, -- ���� ����� ��� ������� ���������� �����
		Attempts INT DEFAULT 0, -- ���������� �������
		FOREIGN KEY (StudentID) REFERENCES Students(ID),
		FOREIGN KEY (SubTaskID) REFERENCES SubTasks(SubTaskID)
		);
	END
END
update StudentTasks set Attempts=0
/*
exec dbo.Create_Table_StudentTasks


select * from StudentTasks


drop table StudentTasks
*/

/*
���������� �������� � �������
Alter TABLE StudentTasks 
ADD
		StudentAnswer NVARCHAR(32) --����� �������
GO
*/

/*
������:
�������� ���������� UPDATE � ������������ CHECK "CK__StudentTa__Compl__7DCDAAA2". �������� ��������� � ���� ������ "BASE", ������� "dbo.StudentTasks", column 'CompletionStatus'.
��� ���������� ������, ������� �� ��������� �� ����������� 
SELECT name 
FROM sys.check_constraints 
WHERE parent_object_id = OBJECT_ID('dbo.StudentTasks');

������� �����������
ALTER TABLE StudentTasks
DROP CONSTRAINT CK_StudentTasks_CompletionStatus;

��������� ������

update StudentTasks set CompletionStatus='���������' where StudentTaskID=1

������ ����� �����������
ALTER TABLE StudentTasks
ADD CONSTRAINT CK_StudentTasks_CompletionStatus
CHECK (CompletionStatus IN ('�� ���������', '� ��������', '���������'));
*/