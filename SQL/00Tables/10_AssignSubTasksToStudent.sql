/*
������� ��������, ������� ����� ��������� ������ ��� ������� ������������ (�������������).--
� ������ ������ �������� � ���� ���������:
���� �������� �������� � ���� ������������, �� ������� ��� ����������� student
���� �������� �������� ��� ����������, ������ ���������� ��� ���� �������������, ��� ���� � ����

exec dbo.AssignSubTasksToStudent @StudentID = 7 --������ �������� � ���������� (��� ������ ������������)
EXEC dbo.AssignSubTasksToStudent;  --������ �������� ��� ���������� (��� ���� ��������� ������������)
AssignSubTasksToStudent
*/
IF EXISTS(SELECT 1 FROM sys.procedures WHERE OBJECT_SCHEMA_NAME([object_id]) = 'dbo' AND name = 'AssignSubTasksToStudent')
    DROP PROCEDURE dbo.AssignSubTasksToStudent
GO

CREATE PROCEDURE dbo.AssignSubTasksToStudent
    @StudentID BIGINT = NULL  -- ��������: ID ������������ (���� NULL � ������������ ����)
AS
BEGIN
    SET NOCOUNT ON;

    -- �������� ����������: ���� @StudentID IS NULL
    IF @StudentID IS NULL
    BEGIN
        INSERT INTO StudentTasks (StudentID, SubTaskID, CompletionStatus)
        SELECT 
            sd.ID AS StudentID,
            s.SubTaskID,
            '�� ���������'
        FROM Students sd
        CROSS JOIN SubTasks s
        WHERE 
		NOT EXISTS ( -- �������� �� ��, ��� ������ ������� ��� ��� 
            SELECT 1 
            FROM StudentTasks st 
            WHERE st.StudentID = sd.ID AND st.SubTaskID = s.SubTaskID
        )
    END
    ELSE
    BEGIN
        -- ���������� ����� ������ ��� ������ ������������
        INSERT INTO StudentTasks (StudentID, SubTaskID, CompletionStatus)
        SELECT 
            @StudentID,
            s.SubTaskID,
            '�� ���������'
        FROM SubTasks s
        WHERE NOT EXISTS ( -- �������� �� ��, ��� ������ ������� ��� ��� 
            SELECT 1 
            FROM StudentTasks st 
            WHERE st.StudentID = @StudentID AND st.SubTaskID = s.SubTaskID
        )
    END
END;
GO