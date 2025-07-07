/*
������� ��������, ������� ����� ������� ������ ��� ������� ������������ (�������������).--
��� ���, ��� ��� ���� � ���� (��� ������ ������������ �� ��� id)

exec dbo.AssignSubTasksToStudent @StudentID = 1 --������ �������� � ����������
*/
IF EXISTS(SELECT 1 FROM sys.procedures WHERE OBJECT_SCHEMA_NAME([object_id]) = 'dbo' and name = 'AssignSubTasksToStudent')
    DROP PROCEDURE dbo.AssignSubTasksToStudent
GO

CREATE PROCEDURE dbo.AssignSubTasksToStudent
    @StudentID BIGINT = NULL  -- ��������: ID ������������ (���� NULL � ������������ ����)
AS
BEGIN
    DECLARE @SubTaskID INT

    -- ���� �� ���� ����������, ������� ����� ���������
    DECLARE SubTaskCursor CURSOR FOR
    SELECT SubTaskID
    FROM SubTasks

    OPEN SubTaskCursor
    FETCH NEXT FROM SubTaskCursor INTO @SubTaskID

    -- ����������� ������ ��������� ������������
    WHILE @@FETCH_STATUS = 0
    BEGIN
        INSERT INTO StudentTasks (StudentID, SubTaskID, CompletionStatus)
        VALUES (@StudentID, @SubTaskID, 'Not Started')  -- ��������� ��������� ������������ � ��������� �������� "Not Started"
        
        FETCH NEXT FROM SubTaskCursor INTO @SubTaskID
    END

    CLOSE SubTaskCursor
    DEALLOCATE SubTaskCursor
END;
GO

