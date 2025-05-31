/*������� �������� (������� - ��� �������, ������� ����� ������������ ��� ���������� ����� ��������� � ���� ������ (�������������).--
�� �������� ��� ��� �����, ��� ��� ���� � ����


��� ��������
INSERT INTO SubTasks (TaskID, SubTaskNumber, Description) VALUES (3, '3', '��������333333');
select * from SubTasks
select * from StudentTasks
*/

IF EXISTS (SELECT 1 FROM sys.triggers WHERE OBJECT_SCHEMA_NAME([object_id]) = 'dbo' AND name = 'trg_AfterInsertSubTask')
    DROP TRIGGER dbo.trg_AfterInsertSubTask;
GO

CREATE TRIGGER dbo.trg_AfterInsertSubTask
ON dbo.SubTasks
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    -- ������� ����� ������� � StudentTasks ��� ������ ��������� � ������� ��������
    INSERT INTO StudentTasks (StudentID, SubTaskID, CompletionStatus)
    SELECT 
        s.ID AS StudentID,
        i.SubTaskID,
        '�� ���������'
    FROM Students s
    CROSS JOIN inserted i
    WHERE NOT EXISTS (
        SELECT 1 
        FROM StudentTasks st
        WHERE st.StudentID = s.ID AND st.SubTaskID = i.SubTaskID
    );
END;
GO