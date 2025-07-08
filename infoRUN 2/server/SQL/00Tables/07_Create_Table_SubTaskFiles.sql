/*
�������� ��� �������� �������, � ������� �������� ����� � ���� ������ � ��������

exec dbo.Create_Table_SubTaskFiles
*/
IF EXISTS(SELECT 1 FROM sys.procedures WHERE OBJECT_SCHEMA_NAME([object_id]) = 'dbo' and name = 'Create_Table_SubTaskFiles')
	DROP PROCEDURE dbo.Create_Table_SubTaskFiles
GO

--������� ��������, ������� ������� ������� � ��������--
CREATE PROCEDURE Create_Table_SubTaskFiles
AS
BEGIN
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'SubTaskFiles')
	BEGIN
		CREATE TABLE SubTaskFiles (
		ID INT PRIMARY KEY IDENTITY,
		SubTaskID INT FOREIGN KEY REFERENCES SubTasks(SubTaskID),
		FileName NVARCHAR(255),
		FilePath NVARCHAR(500),
		UploadDate DATETIME DEFAULT GETDATE()
	);
	END
END

/*

update SubTaskFiles set Attempts=0

select * from SubTaskFiles


drop table SubTaskFiles
*/


