 -- Хранимка для подсчета выполненных заданий по вариантам
 IF EXISTS(SELECT 1 FROM sys.procedures WHERE OBJECT_SCHEMA_NAME([object_id]) = 'dbo' and name = 'GetStudentsTasksStatistic')
	DROP PROCEDURE dbo.GetStudentsTasksStatistic
GO
 CREATE PROCEDURE GetStudentsTasksStatistic
 @StudentID INT	= NULL
AS
BEGIN
	SELECT 
		st.StudentID,
		s.Description,
		
		--(SELECT COUNT(*) FROM StudentTasks where Description='PRO100EGE Вариант №7' and StudentID =@StudentID) as TotalSubVar,
		COUNT(CASE WHEN  st.CompletionStatus = 'Выполнено' THEN 1 END) AS Done, --суммируем выполненные
		COUNT(CASE WHEN  st.CompletionStatus = 'В Процессе' THEN 1 END) AS inProgress, --суммируем в процессе
		COUNT(CASE WHEN  st.CompletionStatus = 'Не приступал' THEN 1 END) AS NoStart, --суммируем не пристумал
		COUNT (*) as TotalSubVar	-- находим количество задач данного варианта
		/*CASE 
			WHEN COUNT(*) = 
				COUNT(CASE WHEN st.CompletionStatus = 'Выполнено' THEN 1 END) +
				COUNT(CASE WHEN st.CompletionStatus = 'В Процессе' THEN 1 END) +
				COUNT(CASE WHEN st.CompletionStatus = 'Не приступал' THEN 1 END)
			THEN CAST(1 AS BIT)
			ELSE CAST(0 AS BIT)
		END AS StatusMatch -- проверка подсчета
		*/
    FROM StudentTasks st
        JOIN Students sd ON sd.ID = st.StudentID 
        JOIN SubTasks s ON s.SubTaskID = st.SubTaskID
		JOIN Tasks t on t.TaskID = s.TaskID
	WHERE 
        (@StudentID IS NULL OR st.StudentID = @StudentID) 
	group BY st.StudentID, s.Description

	-- Итоговая строка по всем вариантам студента
	UNION ALL
    SELECT
        @StudentID AS StudentID,
        'ИТОГО' AS Description,
        SUM(Done) AS Done,
        SUM(InProgress) AS InProgress,
        SUM(NoStart) AS NoStart,
        SUM(TotalSubVar) AS TotalSubVar
        
    FROM
    (
        SELECT 
            COUNT(CASE WHEN st.CompletionStatus = 'Выполнено' THEN 1 END) AS Done,
            COUNT(CASE WHEN st.CompletionStatus = 'В Процессе' THEN 1 END) AS InProgress,
            COUNT(CASE WHEN st.CompletionStatus = 'Не приступал' THEN 1 END) AS NoStart,
            COUNT(*) AS TotalSubVar
        FROM StudentTasks st
        WHERE (@StudentID IS NULL OR st.StudentID = @StudentID)
        GROUP BY st.StudentID, st.SubTaskID
    ) AS sub;
END;
GO
exec GetStudentsTasksStatistic @StudentID = 2