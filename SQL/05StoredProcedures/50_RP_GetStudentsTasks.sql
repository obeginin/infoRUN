/*
 StudentTaskID

exec GetStudentsTasks @StudentTaskID=1
EXEC dbo.GetStudentTaskDetails 1

*/
IF EXISTS(SELECT 1 FROM sys.procedures WHERE OBJECT_SCHEMA_NAME([object_id]) = 'dbo' and name = 'GetStudentsTasks')
	DROP PROCEDURE dbo.GetStudentsTasks
GO

CREATE PROCEDURE GetStudentsTasks
    @StudentTaskID INT				= NULL,
    @StudentID INT					= NULL,
    @SubTaskID INT					= NULL,
    @TaskID INT						= NULL,
	@VariantID INT					= NULL,
    @CompletionStatus NVARCHAR(20)  = NULL, 
	@SortColumn NVARCHAR(50)		= NULL, -- Выбор колонки для сортировки
    @SortDirection NVARCHAR(4)		= 'ASC', -- Сортировка (по возрастанию ASC ) DESC -по убыванию
	@Description  NVARCHAR(MAX)		= NULL
	
AS
BEGIN
	/*вывод параметров в консоль SSMS
	PRINT 'Params:';
	PRINT 'StudentTaskID: ' + ISNULL(CAST(@StudentTaskID AS NVARCHAR), 'NULL');
	PRINT 'StudentID: ' + ISNULL(CAST(@StudentID AS NVARCHAR), 'NULL');
	PRINT 'SubTaskID: ' + ISNULL(CAST(@SubTaskID AS NVARCHAR), 'NULL');
	PRINT 'TaskID: ' + ISNULL(CAST(@TaskID AS NVARCHAR), 'NULL');
	PRINT 'CompletionStatus: ' + ISNULL(@CompletionStatus, 'NULL');
    */
	SELECT 
        st.StudentTaskID, 
        st.StudentID,
        st.SubTaskID,
        st.StudentAnswer,
        st.CompletionStatus, 
        st.Score,
        st.CompletionDate,
        sd.Login,
        --sd.Role, Надо возможно заменить
        s.TaskID,
		t.TaskTitle,
        s.SubTaskNumber,
        s.ImagePath,
        s.Description,
		v.VariantID,
		v.Name,
        s.Answer,
        s.SolutionPath,
		(SELECT COUNT(*) FROM StudentTasks where StudentID= @StudentID) AS TotalSubTasks, -- --Количество задач студента
		(SELECT COUNT(*) FROM StudentTasks where StudentID=@StudentID and CompletionStatus='Выполнено') AS CompletedSubTasks, --Количество выполненных задач
		COUNT(*) OVER() AS TotalCount --  Общее количество задач
    FROM StudentTasks st
        JOIN Students sd ON sd.ID = st.StudentID 
        JOIN SubTasks s ON s.SubTaskID = st.SubTaskID
		JOIN Tasks t on t.TaskID = s.TaskID
		JOIN Variants v on v.VariantID = s.VariantID 
    WHERE 
		(@StudentTaskID IS NULL OR st.StudentTaskID = @StudentTaskID) AND
        (@StudentID IS NULL OR st.StudentID = @StudentID) AND
        (@SubTaskID IS NULL OR st.SubTaskID = @SubTaskID) AND
        (@TaskID IS NULL OR s.TaskID = @TaskID) AND
        (@CompletionStatus IS NULL OR st.CompletionStatus = @CompletionStatus) AND
		(@Description IS NULL OR s.Description = @Description) AND 
		(@VariantID IS NULL OR v.VariantID = @VariantID)
	ORDER BY
    CASE 
        WHEN @SortDirection = 'ASC' THEN 
            CASE 
                WHEN @SortColumn = 'StudentTaskID' THEN st.StudentTaskID
                WHEN @SortColumn = 'StudentID' THEN st.StudentID
                WHEN @SortColumn = 'TaskID' THEN s.TaskID
                WHEN @SortColumn = 'Login' THEN sd.Login
                WHEN @SortColumn = 'CompletionDate' THEN st.CompletionDate
                WHEN @SortColumn = 'Description' THEN s.Description
                WHEN @SortColumn = 'Score' THEN st.Score
				WHEN @SortColumn = 'VariantID' THEN v.VariantID
            END
    END ASC,
    CASE 
        WHEN @SortDirection = 'DESC' THEN 
            CASE 
                WHEN @SortColumn = 'StudentTaskID' THEN st.StudentTaskID
                WHEN @SortColumn = 'StudentID' THEN st.StudentID
                WHEN @SortColumn = 'TaskID' THEN s.TaskID
                WHEN @SortColumn = 'Login' THEN sd.Login
                WHEN @SortColumn = 'CompletionDate' THEN st.CompletionDate
                WHEN @SortColumn = 'Description' THEN s.Description
                WHEN @SortColumn = 'Score' THEN st.Score
				WHEN @SortColumn = 'VariantID' THEN v.VariantID
            END
    END DESC
END
GO
/*	
	ORDER BY
        CASE 
            WHEN @SortColumn = 'StudentTaskID' AND @SortDirection = 'ASC' THEN st.StudentTaskID 
        END ASC,
        CASE 
            WHEN @SortColumn = 'StudentTaskID' AND @SortDirection = 'DESC' THEN st.StudentTaskID 
        END DESC,
        CASE 
            WHEN @SortColumn = 'TaskID' AND @SortDirection = 'ASC' THEN s.TaskID 
        END ASC,
        CASE 
            WHEN @SortColumn = 'TaskID' AND @SortDirection = 'DESC' THEN s.TaskID 
        END DESC,
		CASE 
            WHEN @SortColumn = 'StudentID' AND @SortDirection = 'ASC' THEN st.StudentID
        END ASC,
        CASE 
            WHEN @SortColumn = 'StudentID' AND @SortDirection = 'DESC' THEN st.StudentID 
        END DESC,
		CASE 
            WHEN @SortColumn = 'Login' AND @SortDirection = 'ASC' THEN sd.Login
        END ASC,
        CASE 
            WHEN @SortColumn = 'Login' AND @SortDirection = 'DESC' THEN sd.Login
        END DESC,
        CASE 
            WHEN @SortColumn = 'CompletionDate' AND @SortDirection = 'ASC' THEN st.CompletionDate 
        END ASC,
        CASE 
            WHEN @SortColumn = 'CompletionDate' AND @SortDirection = 'DESC' THEN st.CompletionDate 
        END DESC,
		CASE 
            WHEN @SortColumn = 'Description' AND @SortDirection = 'ASC' THEN s.Description 
        END ASC,
		CASE 
            WHEN @SortColumn = 'Description' AND @SortDirection = 'DESC' THEN s.Description
        END ASC;
		*/


/*SELECT DISTINCT CompletionStatus FROM StudentTasks;

EXEC GetStudentsTasks; 
EXEC GetStudentsTasks @StudentID = 3;  id=2
EXEC GetStudentsTasks @StudentID = 2, @Description = N'; id=2
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