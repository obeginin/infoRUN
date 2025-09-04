/*
Основная хранимка
*/


IF EXISTS(SELECT 1 FROM sys.procedures WHERE OBJECT_SCHEMA_NAME([object_id]) = 'dbo' and name = 'GetSubtask')
	DROP PROCEDURE dbo.GetSubtask
GO

CREATE PROCEDURE GetSubtask

    @SubTaskID INT					= NULL,			-- по id задачи
    @TaskID INT						= NULL,			-- по id категории
	@SubjectID INT					= NULL,			-- по id предмета
	@VariantID INT					= NULL,			-- по id варианта
	@Search NVARCHAR(100)			= NULL,			-- Поиск по ключевому слову (логин, описание и т.п.)
	@UploadDate Date				= NULL,
	@Creator NVARCHAR(50)			= NULL,
	@SortColumn1 NVARCHAR(50)		= NULL,			-- Выбор колонки для сортировки 1 уровень
	@SortColumn2 NVARCHAR(50)		= NULL,			-- Выбор колонки для сортировки 2 уровень
    @SortDirection1 NVARCHAR(4)		= 'ASC',		-- Сортировка (по возрастанию ASC ) DESC -по убыванию
	@SortDirection2	NVARCHAR(4)		= 'ASC',
	@Offset INT						= NULL,			-- с какой строки начинать выводить
	@Limit INT						= NULL			-- количество выведенных строк
	--@Description  NVARCHAR(MAX)		= NULL
	
AS
BEGIN
	
	SELECT 
        s.SubTaskID,						-- id задачи
		s.SubTaskNumber,					-- типы задач в данной категории (1.1, 1.2, ...)
		sb.ID as SubjectID,					-- id предмета
		sb.Name as SubjectName,				-- предмет (информатика, математика)
		sb.Description,						-- описание предмета
		t.TaskID,							-- id категории 
		t.TaskTitle,						-- категория (ЕГЭ_1, ЕГЭ_2)
		v.VariantID,						-- id варианта
		v.VariantName,						-- Вариант
		v.Type as TypeVariant,				-- Тип варианта ("Вариант", "Контрольная", "Олимпиада", "Практика")
		v.Year as YearVariant,				-- Год варианта
		v.Number as NumberVarinat,			-- Специальный номер варианта (если применимо 1, 2, 3 и т.д.)
		v.DifficultyLevel,					-- Уровень сложности варианта
		s.Blocks,							-- Json багет задачи
		v.Comment,							-- Комментарий варианта
		s.UploadDate,						-- Дата создания задания
		s.Creator							-- Пользователь создавший задачу

		
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
	-- Первая сортировка
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

	-- Вторая сортировка (только если указана!)
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
