IF EXISTS(SELECT 1 FROM sys.procedures WHERE OBJECT_SCHEMA_NAME([object_id]) = 'dbo' and name = 'Create_Table_Tasks')
	DROP PROCEDURE dbo.Create_Table_Tasks
GO
--exec Create_Table_Tasks --��������� ��������

CREATE PROCEDURE Create_Table_Tasks
AS
BEGIN
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Tasks')
	BEGIN
		CREATE TABLE Tasks (
			TaskID INT IDENTITY(1,1) PRIMARY KEY, -- id ������ (��������� ����)
			TaskNumber INT NOT NULL UNIQUE,  -- ����� ������ (1, 2, 3... 27) �� ������ ���� ������� � ����������
			TaskTitle NVARCHAR(255) NOT NULL -- �������� ������
		);
	END
END;

/*
DROP PROCEDURE Create_Table_Tasks --������� ��������

drop table Tasks --������� ������� (������ � �������)
SELECT name FROM sys.tables; --����� ���� ������ ��

��������� ������ � �������
INSERT INTO Tasks (TaskNumber, TaskTitle) VALUES (1,'������ �������'),(2,'������ �������'),(3,'������ �������'),(4,'��������� �������');
update Tasks set TaskTitle='��������� �������' where TaskID=4
delete Tasks where TaskID in (1,2,3,4) --������� ������


ALTER TABLE Tasks
ALTER COLUMN TaskNumber INT NOT NULL ;

select * from users
select * from Tasks
select * from SubTasks
select * from StudentTasks



*/