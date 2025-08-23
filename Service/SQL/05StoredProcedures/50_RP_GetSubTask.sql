/*
�������� ��������
*/


IF EXISTS(SELECT 1 FROM sys.procedures WHERE OBJECT_SCHEMA_NAME([object_id]) = 'dbo' and name = 'GetSubtask')
	DROP PROCEDURE dbo.GetSubtask
GO

CREATE PROCEDURE GetSubtask

    @SubTaskID INT					= NULL,			-- �� id ������
    @TaskID INT						= NULL,			-- �� id ���������
	@SubjectID INT					= NULL,			-- �� id ��������
	@VariantID INT					= NULL,			-- �� id ��������
	@Search NVARCHAR(100)			= NULL,			-- ����� �� ��������� ����� (�����, �������� � �.�.)
	@UploadDate Date				= NULL,
	@Creator NVARCHAR(50)			= NULL,
	@SortColumn1 NVARCHAR(50)		= NULL,			-- ����� ������� ��� ���������� 1 �������
	@SortColumn2 NVARCHAR(50)		= NULL,			-- ����� ������� ��� ���������� 2 �������
    @SortDirection1 NVARCHAR(4)		= 'ASC',		-- ���������� (�� ����������� ASC ) DESC -�� ��������
	@SortDirection2	NVARCHAR(4)		= 'ASC',
	@Offset INT						= NULL,			-- � ����� ������ �������� ��������
	@Limit INT						= NULL			-- ���������� ���������� �����
	--@Description  NVARCHAR(MAX)		= NULL
	
AS
BEGIN
	
	SELECT 
        s.SubTaskID,						-- id ������
		s.SubTaskNumber,					-- ���� ����� � ������ ��������� (1.1, 1.2, ...)
		sb.ID as SubjectID,					-- id ��������
		sb.Name as SubjectName,				-- ������� (�����������, ����������)
		sb.Description,						-- �������� ��������
		t.TaskID,							-- id ��������� 
		t.TaskTitle,						-- ��������� (���_1, ���_2)
		v.VariantID,						-- id ��������
		v.VariantName,						-- �������
		v.Type as TypeVariant,				-- ��� �������� ("�������", "�����������", "���������", "��������")
		v.Year as YearVariant,				-- ��� ��������
		v.Number as NumberVarinat,			-- ����������� ����� �������� (���� ��������� 1, 2, 3 � �.�.)
		v.DifficultyLevel,					-- ������� ��������� ��������
		s.Blocks,							-- Json ����� ������
		v.Comment,							-- ����������� ��������
		s.UploadDate,						-- ���� �������� �������
		s.Creator							-- ������������ ��������� ������

		
    FROM SubTasks s 
		JOIN Tasks t on t.TaskID = s.TaskID
		JOIN Variants v on v.VariantID = s.VariantID 
		JOIN Subjects sb on sb.ID=t.SubjectID
    WHERE 
			(@SubTaskID IS NULL OR s.SubTaskID = @SubTaskID) 
		AND (@TaskID IS NULL OR s.TaskID = @TaskID) 
		AND (@SubjectID IS NULL OR sb.ID = @SubjectID)
		AND (@VariantID IS NULL OR v.VariantID = @VariantID)
		AND (
			@Search IS NULL
			OR s.Blocks LIKE '%' + @Search + '%'	
			OR t.TaskTitle LIKE '%' + @Search + '%'
			OR v.VariantName LIKE '%' + @Search + '%'
			OR v.Comment LIKE '%' + @Search + '%'
		)

	ORDER BY
	-- ������ ����������
    CASE 
        WHEN @SortDirection1 = 'ASC' THEN 
            CASE 
				WHEN @SortColumn1 = 'SubTaskID' THEN s.SubTaskID
                WHEN @SortColumn1 = 'TaskID' THEN s.TaskID
                WHEN @SortColumn1 = 'SubjectID' THEN sb.ID
                WHEN @SortColumn1 = 'VariantID' THEN v.VariantID  
				WHEN @SortColumn1 = 'UploadDate' THEN s.UploadDate
				WHEN @SortColumn1 = 'Creator' THEN s.Creator
            END
    END ASC,
    CASE 
        WHEN @SortDirection1 = 'DESC' THEN 
            CASE 
                WHEN @SortColumn1 = 'SubTaskID' THEN s.SubTaskID
                WHEN @SortColumn1 = 'TaskID' THEN s.TaskID
                WHEN @SortColumn1 = 'SubjectID' THEN sb.ID
                WHEN @SortColumn1 = 'VariantID' THEN v.VariantID  
				WHEN @SortColumn1 = 'UploadDate' THEN s.UploadDate
				WHEN @SortColumn1 = 'Creator' THEN s.Creator
            END    
	END DESC,

	-- ������ ���������� (������ ���� �������!)
	CASE 
        WHEN @SortColumn2 IS NOT NULL AND @SortDirection2 = 'ASC' THEN 
            CASE 
                WHEN @SortColumn1 = 'SubTaskID' THEN s.SubTaskID
                WHEN @SortColumn1 = 'TaskID' THEN s.TaskID
                WHEN @SortColumn1 = 'SubjectID' THEN sb.ID
                WHEN @SortColumn1 = 'VariantID' THEN v.VariantID  
				WHEN @SortColumn1 = 'UploadDate' THEN s.UploadDate
				WHEN @SortColumn1 = 'Creator' THEN s.Creator
            END
    END ASC,
    CASE 
        WHEN @SortColumn2 IS NOT NULL AND @SortDirection2 = 'DESC' THEN 
            CASE 
                WHEN @SortColumn1 = 'SubTaskID' THEN s.SubTaskID
                WHEN @SortColumn1 = 'TaskID' THEN s.TaskID
                WHEN @SortColumn1 = 'SubjectID' THEN sb.ID
                WHEN @SortColumn1 = 'VariantID' THEN v.VariantID  
				WHEN @SortColumn1 = 'UploadDate' THEN s.UploadDate
				WHEN @SortColumn1 = 'Creator' THEN s.Creator
            END
    
	END DESC
OFFSET ISNULL(@Offset, 0) ROWS
FETCH NEXT ISNULL(@Limit, 500000) ROWS ONLY
END
GO



exec GetSubtask
exec GetSubtask @SubTaskID=2
