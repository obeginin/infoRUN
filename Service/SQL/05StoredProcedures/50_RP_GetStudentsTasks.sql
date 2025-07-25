/*
Основная хранимка
*/
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
	@SortColumn NVARCHAR(50)		= NULL,			-- Выбор колонки для сортировки ()
    @SortDirection NVARCHAR(4)		= 'ASC',		-- Сортировка (по возрастанию ASC ) DESC -по убыванию
	@Offset INT						= 0,			-- с какой строки начинать выводить
	@Limit INT						= 50			-- количество выведенных строк
	--@Description  NVARCHAR(MAX)		= NULL
	
AS
BEGIN
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
		v.Number,							-- Специальный номер варианта (если применимо 1, 2, 3 и т.д.)
		v.DifficultyLevel,					-- Уровень сложности варианта
		v.Comment							-- Комментарий варианта

		--(SELECT COUNT(*) FROM StudentTasks where StudentID= @StudentID) AS TotalSubTasks, -- --Количество задач студента
		--(SELECT COUNT(*) FROM StudentTasks where StudentID=@StudentID and CompletionStatus='Выполнено') AS CompletedSubTasks, --Количество выполненных задач
		--COUNT(*) OVER() AS TotalCount --  Общее количество задач
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
		
		--AND (@Description IS NULL OR s.Description = @Description)
	ORDER BY
    CASE 
        WHEN @SortDirection = 'ASC' THEN 
            CASE 
                WHEN @SortColumn = 'StudentTaskID' THEN st.StudentTaskID
                WHEN @SortColumn = 'StudentID' THEN st.StudentID
				WHEN @SortColumn = 'SubTaskID' THEN st.SubTaskID
                WHEN @SortColumn = 'TaskID' THEN s.TaskID
                WHEN @SortColumn = 'SubjectID' THEN sj.ID
                WHEN @SortColumn = 'VariantID' THEN v.VariantID  
				WHEN @SortColumn = 'StartDate' THEN st.StartDate
				WHEN @SortColumn = 'ModifiedDate' THEN st.ModifiedDate
				WHEN @SortColumn = 'CompletionDate' THEN st.CompletionDate
				WHEN @SortColumn = 'DeadlineDate' THEN st.DeadlineDate
				WHEN @SortColumn = 'TypeVariant' THEN v.Type
				WHEN @SortColumn = 'YearVariant' THEN v.Year
				WHEN @SortColumn = 'Attempts' THEN st.Attempts

				
				-- StudentTaskID, StudentID, SubTaskID, TaskID, SubjectID, VariantID, CompletionDate, StartDate, ModifiedDate, DeadlineDate, Attempts, TypeVariant, YearVariant
				--WHEN @SortColumn = 'Login' THEN sd.Login
				--WHEN @SortColumn = 'Description' THEN s.Description
            END
    END ASC,
    CASE 
        WHEN @SortDirection = 'DESC' THEN 
            CASE 
                WHEN @SortColumn = 'StudentTaskID' THEN st.StudentTaskID
                WHEN @SortColumn = 'StudentID' THEN st.StudentID
				WHEN @SortColumn = 'SubTaskID' THEN st.SubTaskID
                WHEN @SortColumn = 'TaskID' THEN s.TaskID
                WHEN @SortColumn = 'SubjectID' THEN sj.ID
                WHEN @SortColumn = 'VariantID' THEN v.VariantID  
				WHEN @SortColumn = 'StartDate' THEN st.StartDate
				WHEN @SortColumn = 'ModifiedDate' THEN st.ModifiedDate
				WHEN @SortColumn = 'CompletionDate' THEN st.CompletionDate
				WHEN @SortColumn = 'DeadlineDate' THEN st.DeadlineDate
				WHEN @SortColumn = 'TypeVariant' THEN v.Type
				WHEN @SortColumn = 'YearVariant' THEN v.Year
				WHEN @SortColumn = 'Attempts' THEN st.Attempts
            END
    
	END DESC
OFFSET @Offset ROWS
FETCH NEXT @Limit ROWS ONLY;
END
GO


/*SELECT DISTINCT CompletionStatus FROM StudentTasks;


EXEC GetStudentsTasks; 
EXEC GetStudentsTasks @StudentID = 3;  id=2
EXEC GetStudentsTasks @StudentID = 2, @Description = N'; id=2
EXEC GetStudentsTasks @StudentTaskID=1
EXEC GetStudentsTasks @TaskID = 2;
EXEC GetStudentsTasks @SubTaskID = 2, @CompletionStatus = N'';
EXEC GetStudentsTasks @CompletionStatus = N''; 
EXEC GetStudentsTasks @StudentTaskID = 2;
EXEC GetStudentsTasks @Description = N'';



EXEC GetStudentsTasks @SortColumn = 'StudentTaskID', @SortDirection = 'ASC';
EXEC GetStudentsTasks @SortColumn = 'StudentTaskID', @SortDirection = 'DESC';
EXEC GetStudentsTasks @SortColumn = 'TaskID', @SortDirection = 'ASC';
EXEC GetStudentsTasks @SortColumn = 'TaskID', @SortDirection = 'DESC';

EXEC GetStudentsTasks @SortColumn = 'CompletionDate', @SortDirection = 'ASC'; 
EXEC GetStudentsTasks @SortColumn = 'CompletionDate', @SortDirection = 'DESC'; 


EXEC GetStudentsTasks @SortColumn = 'StudentID', @SortDirection = 'ASC';
EXEC GetStudentsTasks @SortColumn = 'StudentID', @SortDirection = 'DESC';
EXEC GetStudentsTasks @SortColumn = 'Login', @SortDirection = 'ASC';
EXEC GetStudentsTasks @SortColumn = 'Login', @SortDirection = 'DESC';


EXEC GetStudentsTasks @StudentID = 1, @SortColumn = 'StudentTaskID', @SortDirection = 'ASC';
*/ 

/*
select* from Tasks
select* from SubTasks

select ID, Login from Students
select distinct Description from SubTasks
SELECT TaskTitle FROM Tasks


select* from StudentTasks where StudentID=2 and CompletionStatus='Выполнено'
SELECT COUNT(*) FROM StudentTasks where StudentID=2 and CompletionStatus='Выполнено'
SELECT COUNT(*) FROM StudentTasks where  CompletionStatus='Выполнено'
select * from SubTaskFiles
select * from Variants
select * from SubTasks*/