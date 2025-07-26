/*
Основная хранимка
*/

/*вывод параметров в консоль SSMS
	PRINT 'Params:';
	PRINT 'StudentTaskID: ' + ISNULL(CAST(@StudentTaskID AS NVARCHAR), 'NULL');
	PRINT 'StudentID: ' + ISNULL(CAST(@StudentID AS NVARCHAR), 'NULL');
	PRINT 'SubTaskID: ' + ISNULL(CAST(@SubTaskID AS NVARCHAR), 'NULL');
	PRINT 'TaskID: ' + ISNULL(CAST(@TaskID AS NVARCHAR), 'NULL');
	PRINT 'CompletionStatus: ' + ISNULL(@CompletionStatus, 'NULL');


	select * from StudentTasks
	select * from SubTasks
	select * from Tasks
	select * from Variants
	select * from Subjects
    */

	--(SELECT COUNT(*) FROM StudentTasks where StudentID= @StudentID) AS TotalSubTasks, -- --Количество задач студента
		--(SELECT COUNT(*) FROM StudentTasks where StudentID=@StudentID and CompletionStatus='Выполнено') AS CompletedSubTasks, --Количество выполненных задач
		--COUNT(*) OVER() AS TotalCount --  Общее количество задач
IF EXISTS(SELECT 1 FROM sys.procedures WHERE OBJECT_SCHEMA_NAME([object_id]) = 'dbo' and name = 'GetStudentsTasks')
	DROP PROCEDURE dbo.GetStudentsTasks
GO

CREATE PROCEDURE GetStudentsTasks
    @StudentTaskID INT				= NULL,			-- по Номеру задачи Студента
    @StudentID INT					= NULL,			-- по id студента
    @SubTaskID INT					= NULL,			-- по id задачи
    @TaskID INT						= NULL,			-- по id категории
	@SubjectID INT					= NULL,			-- по id предмета
	@VariantID INT					= NULL,			-- по id варианта
    @CompletionStatus NVARCHAR(20)  = NULL,			-- по статусу выполнения 
	@Search NVARCHAR(100)			= NULL,			-- Поиск по ключевому слову (логин, описание и т.п.)
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
        st.StudentTaskID,					-- id задачи студента
        st.StudentID,						-- id студента
        st.SubTaskID,						-- id задачи
        st.StudentAnswer,					-- ответ студента
        st.CompletionStatus,				-- статус выполнения
        st.Score,							-- типо оценка
		st.StartDate,						-- Дата начала выполнения задания
		st.ModifiedDate,					-- Дата внесения изменений в задание
        st.CompletionDate,					-- Дата выполнения (получения правильного ответа)
		st.DeadlineDate,					-- Срок выполнения
		st.Attempts,						-- Количество попыток
        sd.Login,							-- Логин пользователя
        sj.ID,								-- id предмета
		sj.Name,							-- предмет (информатика, математика)
		t.TaskID,							-- id категории 
		t.TaskTitle,						-- категория (ЕГЭ_1, ЕГЭ_2)
        s.SubTaskNumber,					-- типы задач в данной категории (1.1, 1.2, ...)
        s.ImagePath,						-- адрес с изображением задачи
        s.Description,						-- описание задачи
		v.VariantID,						-- id варианта
		v.VariantName,						-- Вариант
		v.Type as TypeVariant,				-- Тип варианта ("Вариант", "Контрольная", "Олимпиада", "Практика")
		v.Year as YearVariant,				-- Год варианта
		v.Number as NumberVarinat,			-- Специальный номер варианта (если применимо 1, 2, 3 и т.д.)
		v.DifficultyLevel,					-- Уровень сложности варианта
		v.Comment							-- Комментарий варианта

		
    FROM StudentTasks st
        JOIN Students sd ON sd.ID = st.StudentID 
        JOIN SubTasks s ON s.SubTaskID = st.SubTaskID
		JOIN Tasks t on t.TaskID = s.TaskID
		JOIN Variants v on v.VariantID = s.VariantID 
		JOIN Subjects sj on sj.ID=t.SubjectID
    WHERE 
			(@StudentTaskID IS NULL OR st.StudentTaskID = @StudentTaskID) 
		AND (@StudentID IS NULL OR st.StudentID = @StudentID) 
		AND (@SubTaskID IS NULL OR st.SubTaskID = @SubTaskID) 
		AND (@TaskID IS NULL OR s.TaskID = @TaskID) 
		AND (@SubjectID IS NULL OR sj.ID = @SubjectID)
		AND (@VariantID IS NULL OR v.VariantID = @VariantID)
		AND (@CompletionStatus IS NULL OR st.CompletionStatus = @CompletionStatus) 
		AND (
			@Search IS NULL
			OR s.Description LIKE '%' + @Search + '%'
			OR sd.Login LIKE '%' + @Search + '%'
			OR v.VariantName LIKE '%' + @Search + '%'
			OR v.Comment LIKE '%' + @Search + '%'
		)
		--AND (@Description IS NULL OR s.Description = @Description)
	ORDER BY
	-- Первая сортировка
    CASE 
        WHEN @SortDirection1 = 'ASC' THEN 
            CASE 
                WHEN @SortColumn1 = 'StudentTaskID' THEN st.StudentTaskID
                WHEN @SortColumn1 = 'StudentID' THEN st.StudentID
				WHEN @SortColumn1 = 'SubTaskID' THEN st.SubTaskID
                WHEN @SortColumn1 = 'TaskID' THEN s.TaskID
                WHEN @SortColumn1 = 'SubjectID' THEN sj.ID
                WHEN @SortColumn1 = 'VariantID' THEN v.VariantID  
				WHEN @SortColumn1 = 'StartDate' THEN st.StartDate
				WHEN @SortColumn1 = 'ModifiedDate' THEN st.ModifiedDate
				WHEN @SortColumn1 = 'CompletionDate' THEN st.CompletionDate
				WHEN @SortColumn1 = 'DeadlineDate' THEN st.DeadlineDate
				WHEN @SortColumn1 = 'TypeVariant' THEN v.Type
				WHEN @SortColumn1 = 'YearVariant' THEN v.Year
				WHEN @SortColumn1 = 'NumberVarinat' THEN v.Number
				WHEN @SortColumn1 = 'DifficultyLevel' THEN v.DifficultyLevel
				WHEN @SortColumn1 = 'Attempts' THEN st.Attempts

				
				-- Поля для сортировки: StudentTaskID, StudentID, SubTaskID, TaskID, SubjectID, VariantID, StartDate, ModifiedDate, CompletionDate,  DeadlineDate, TypeVariant, YearVariant, NumberVarinat, DifficultyLevel, Attempts,
				--WHEN @SortColumn1 = 'Login' THEN sd.Login
				--WHEN @SortColumn1 = 'Description' THEN s.Description
            END
    END ASC,
    CASE 
        WHEN @SortDirection1 = 'DESC' THEN 
            CASE 
                WHEN @SortColumn1 = 'StudentTaskID' THEN st.StudentTaskID
                WHEN @SortColumn1 = 'StudentID' THEN st.StudentID
				WHEN @SortColumn1 = 'SubTaskID' THEN st.SubTaskID
                WHEN @SortColumn1 = 'TaskID' THEN s.TaskID
                WHEN @SortColumn1 = 'SubjectID' THEN sj.ID
                WHEN @SortColumn1 = 'VariantID' THEN v.VariantID  
				WHEN @SortColumn1 = 'StartDate' THEN st.StartDate
				WHEN @SortColumn1 = 'ModifiedDate' THEN st.ModifiedDate
				WHEN @SortColumn1 = 'CompletionDate' THEN st.CompletionDate
				WHEN @SortColumn1 = 'DeadlineDate' THEN st.DeadlineDate
				WHEN @SortColumn1 = 'TypeVariant' THEN v.Type
				WHEN @SortColumn1 = 'YearVariant' THEN v.Year
				WHEN @SortColumn1 = 'NumberVarinat' THEN v.Number
				WHEN @SortColumn1 = 'DifficultyLevel' THEN v.DifficultyLevel
				WHEN @SortColumn1 = 'Attempts' THEN st.Attempts
            END    
	END DESC,

	-- Вторая сортировка (только если указана!)
	CASE 
        WHEN @SortColumn2 IS NOT NULL AND @SortDirection2 = 'ASC' THEN 
            CASE 
                WHEN @SortColumn2 = 'StudentTaskID' THEN st.StudentTaskID
                WHEN @SortColumn2 = 'StudentID' THEN st.StudentID
				WHEN @SortColumn2 = 'SubTaskID' THEN st.SubTaskID
                WHEN @SortColumn2 = 'TaskID' THEN s.TaskID
                WHEN @SortColumn2 = 'SubjectID' THEN sj.ID
                WHEN @SortColumn2 = 'VariantID' THEN v.VariantID  
				WHEN @SortColumn2 = 'StartDate' THEN st.StartDate
				WHEN @SortColumn2 = 'ModifiedDate' THEN st.ModifiedDate
				WHEN @SortColumn2 = 'CompletionDate' THEN st.CompletionDate
				WHEN @SortColumn2 = 'DeadlineDate' THEN st.DeadlineDate
				WHEN @SortColumn2 = 'TypeVariant' THEN v.Type
				WHEN @SortColumn2 = 'YearVariant' THEN v.Year
				WHEN @SortColumn1 = 'NumberVarinat' THEN v.Number
				WHEN @SortColumn1 = 'DifficultyLevel' THEN v.DifficultyLevel
				WHEN @SortColumn1 = 'Attempts' THEN st.Attempts
            END
    END ASC,
    CASE 
        WHEN @SortColumn2 IS NOT NULL AND @SortDirection2 = 'DESC' THEN 
            CASE 
                WHEN @SortColumn2 = 'StudentTaskID' THEN st.StudentTaskID
                WHEN @SortColumn2 = 'StudentID' THEN st.StudentID
				WHEN @SortColumn2 = 'SubTaskID' THEN st.SubTaskID
                WHEN @SortColumn2 = 'TaskID' THEN s.TaskID
                WHEN @SortColumn2 = 'SubjectID' THEN sj.ID
                WHEN @SortColumn2 = 'VariantID' THEN v.VariantID  
				WHEN @SortColumn2 = 'StartDate' THEN st.StartDate
				WHEN @SortColumn2 = 'ModifiedDate' THEN st.ModifiedDate
				WHEN @SortColumn2 = 'CompletionDate' THEN st.CompletionDate
				WHEN @SortColumn2 = 'DeadlineDate' THEN st.DeadlineDate
				WHEN @SortColumn2 = 'TypeVariant' THEN v.Type
				WHEN @SortColumn2 = 'YearVariant' THEN v.Year
				WHEN @SortColumn1 = 'NumberVarinat' THEN v.Number
				WHEN @SortColumn1 = 'DifficultyLevel' THEN v.DifficultyLevel
				WHEN @SortColumn1 = 'Attempts' THEN st.Attempts
            END
    
	END DESC
OFFSET ISNULL(@Offset, 0) ROWS
FETCH NEXT ISNULL(@Limit, 50) ROWS ONLY
END
GO


/*SELECT DISTINCT CompletionStatus FROM StudentTasks;


EXEC GetStudentsTasks @Limit=5000;						-- все задачи всех студентов
EXEC GetStudentsTasks @StudentID = 3;					-- задачи конкретного студента с id=3
EXEC GetStudentsTasks @StudentTaskID=1					-- конкретная задачу студента по её id
EXEC GetStudentsTasks @TaskID = 2;						-- все задачи категории с id=2
EXEC GetStudentsTasks @CompletionStatus = N'Выполенено';-- все задачи со статусом "Выполенено"

EXEC GetStudentsTasks @StudentID = 2




EXEC GetStudentsTasks @SortColumn1 = 'StudentTaskID', @SortDirection1 = 'ASC';
EXEC GetStudentsTasks @SortColumn1 = 'StudentID', @SortDirection1 = 'DESC', @SortColumn2 = 'StudentTaskID', @SortDirection2 = 'ASC';
EXEC GetStudentsTasks @SortColumn1 = 'TaskID', @SortDirection1 = 'ASC';
EXEC GetStudentsTasks @SortColumn1 = 'TaskID', @SortDirection1 = 'DESC';

EXEC GetStudentsTasks @SortColumn1 = 'CompletionDate', @SortDirection1 = 'ASC'; 
EXEC GetStudentsTasks @SortColumn1 = 'CompletionDate', @SortDirection1 = 'DESC'; 


EXEC GetStudentsTasks @SortColumn1 = 'StudentID', @SortDirection1 = 'ASC';
EXEC GetStudentsTasks @SortColumn1 = 'StudentID', @SortDirection1 = 'DESC';

EXEC GetStudentsTasks @Search = 'Крылов'

EXEC GetStudentsTasks @StudentID = 2, @SortColumn1 = 'StudentTaskID', @SortDirection1 = 'DESC';
*/ 

/*


select* from StudentTasks where StudentID=2 and CompletionStatus='Выполнено'
SELECT COUNT(*) FROM StudentTasks where StudentID=2 and CompletionStatus='Выполнено'
SELECT COUNT(*) FROM StudentTasks where  CompletionStatus='Выполнено'
select * from SubTaskFiles
select * from Variants
select * from SubTasks*/