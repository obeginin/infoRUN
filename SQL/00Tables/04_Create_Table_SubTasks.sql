--������� ��������, ������� ������� ������� � ��������--
IF EXISTS(SELECT 1 FROM sys.procedures WHERE OBJECT_SCHEMA_NAME([object_id]) = 'dbo' and name = 'Create_Table_SubTasks')
	DROP PROCEDURE dbo.Create_Table_SubTasks
GO

CREATE PROCEDURE dbo.Create_Table_SubTasks
AS
BEGIN
	IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'SubTasks')
	BEGIN
		CREATE TABLE SubTasks (
		SubTaskID INT IDENTITY(1,1) PRIMARY KEY, --id ��������� (��������� ����)
		TaskID INT NOT NULL,  -- ����� � �������
		SubTaskNumber INT NOT NULL,  -- ����� ��������� (1.1, 1.2, ...)
		VariantID INT,
		ImagePath NVARCHAR(255), --���� ������
		Description NVARCHAR(MAX),  -- �������� ���������
		Answer NVARCHAR(32), --�����
		SolutionPath NVARCHAR(255), --������� ������
		FOREIGN KEY (TaskID) REFERENCES Tasks(TaskID) ON UPDATE CASCADE, -- ������� ����
		FOREIGN KEY (VariantID) REFERENCES Variants(VariantID) ON UPDATE CASCADE
		);
	END
END;



/*
exec dbo.Create_Table_SubTasks
INSERT INTO SubTasks (TaskID, SubTaskNumber, Description) VALUES (1,'1.1','1 ������');
select * from SubTasks
DROP PROCEDURE dbo.Create_Table_SubTasks
drop table SubTasks
*/


