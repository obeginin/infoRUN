/*������� �������� (������� - ��� �������, ������� ����� ������������ ��� ���������� ������ ������������ � ���� ������ (�������������).--
�� �������� ��� ��� �������������, ��� ��� ���� � ����
���� ����� ���������� ����� ������� ���� ������������ ��������� ��������� �������� (���� ����� ��� � �� �����)
�������� ������ ��� ������ ������������


*/
IF EXISTS(SELECT 1 FROM sys.triggers WHERE OBJECT_SCHEMA_NAME([object_id]) = 'dbo' and name = 'trg_AfterInsertStudent')
    DROP TRIGGER dbo.trg_AfterInsertStudent
GO

--���� ���� ������ �������, ������� ����� ����������� ����� ������� ������ � ������� users
CREATE TRIGGER dbo.trg_AfterInsertStudent
ON dbo.Students
AFTER INSERT
AS
BEGIN
    DECLARE @StudentID BIGINT

    -- �������� ID ������ ��� ������������ ������������
    SELECT @StudentID = ID FROM inserted

    -- ����� �������� ��������� ��� ���������� �������� ������ ������������
    EXEC dbo.AssignSubTasksToStudent @StudentID
END;
GO

/*
���������� ��� �������� �������� 
SELECT 
    name AS trigger_name,
    parent_class_desc,
    OBJECT_NAME(parent_id) AS table_name,
    is_disabled
FROM sys.triggers
WHERE is_ms_shipped = 0;
*/


