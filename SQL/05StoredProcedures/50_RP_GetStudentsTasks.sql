/*
С помощью данного скрипта находм подробную информацию о выбранной задачи студента по StudentTaskID

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
    @CompletionStatus NVARCHAR(20)  = NULL, 
	@SortColumn NVARCHAR(50)		= NULL, -- Выбор поля для сортировки
    @SortDirection NVARCHAR(4)		= 'ASC', -- выбор сортировки (по умолчанию ASC по возрастанию) DESC -по убыванию
	@Description  NVARCHAR(MAX)		= NULL
AS
BEGIN
	/*отладочный вывод в сообщения SSMS
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
        sd.Role,
        s.TaskID,
		t.TaskTitle,
        s.SubTaskNumber,
        s.ImagePath,
        s.Description,
        s.Answer,
        s.SolutionPath,
		(SELECT COUNT(*) FROM StudentTasks where StudentID= @StudentID) AS TotalSubTasks, --Количество задач студента
		(SELECT COUNT(*) FROM StudentTasks where StudentID=@StudentID and CompletionStatus='Выполнено') AS CompletedSubTasks, --Количество решеных задач студента
		COUNT(*) OVER() AS TotalCount --  Добавлено общее количество всех найденных записей
    FROM StudentTasks st
        JOIN Students sd ON sd.ID = st.StudentID 
        JOIN SubTasks s ON s.SubTaskID = st.SubTaskID
		JOIN Tasks t on t.TaskID = s.TaskID
    WHERE 
		(@StudentTaskID IS NULL OR st.StudentTaskID = @StudentTaskID) AND
        (@StudentID IS NULL OR st.StudentID = @StudentID) AND
        (@SubTaskID IS NULL OR st.SubTaskID = @SubTaskID) AND
        (@TaskID IS NULL OR s.TaskID = @TaskID) AND
        (@CompletionStatus IS NULL OR st.CompletionStatus = @CompletionStatus) AND
		(@Description IS NULL OR s.Description = @Description)
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

EXEC GetStudentsTasks; Вывод всех задач всех студентов
EXEC GetStudentsTasks @StudentID = 2; Вывод всех задач студента с id=2
EXEC GetStudentsTasks @StudentID = 2, @Description = N'Крылов Вариант №14'; Вывод всех задач студента с id=2
EXEC GetStudentsTasks @TaskID = 2; по категории задания
EXEC GetStudentsTasks @SubTaskID = 2, @CompletionStatus = N'Не приступал';
EXEC GetStudentsTasks @CompletionStatus = N'Выполнено'; по статусу выполнения
EXEC GetStudentsTasks @StudentTaskID = 2; конкретная задача
EXEC GetStudentsTasks @Description = N'Крылов Вариант №14'; конкретная задача


С сортировкой 
EXEC GetStudentsTasks @SortColumn = 'StudentTaskID', @SortDirection = 'ASC';
EXEC GetStudentsTasks @SortColumn = 'StudentTaskID', @SortDirection = 'DESC';
EXEC GetStudentsTasks @SortColumn = 'TaskID', @SortDirection = 'ASC';
EXEC GetStudentsTasks @SortColumn = 'TaskID', @SortDirection = 'DESC';

EXEC GetStudentsTasks @SortColumn = 'CompletionDate', @SortDirection = 'ASC'; Сортировка по дате по убыванию:
EXEC GetStudentsTasks @SortColumn = 'CompletionDate', @SortDirection = 'DESC'; Сортировка по дате по убыванию:

Сортировка не отрабатывает
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
*/

select* from StudentTasks where StudentID=2 and CompletionStatus='Выполнено'
SELECT COUNT(*) FROM StudentTasks where StudentID=2 and CompletionStatus='Выполнено'
SELECT COUNT(*) FROM StudentTasks where  CompletionStatus='Выполнено'
