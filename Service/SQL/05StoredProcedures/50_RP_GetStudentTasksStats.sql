
IF EXISTS(SELECT 1 FROM sys.procedures WHERE OBJECT_SCHEMA_NAME([object_id]) = 'dbo' and name = 'GetStudentTasksStats')
	DROP PROCEDURE dbo.GetStudentTasksStats
GO

CREATE PROCEDURE GetStudentTasksStats
    @StudentID INT = NULL,
    @SubjectID INT = NULL,
    @VariantID INT = NULL
AS
BEGIN
    SELECT 
        COUNT(*) AS TotalSubTasks,
        COUNT(CASE WHEN CompletionStatus = 'Выполнено' THEN 1 END) AS CompletedSubTasks,
        COUNT(CASE WHEN CompletionStatus = 'В процессе' THEN 1 END) AS InProgressSubTasks,
        COUNT(CASE WHEN CompletionStatus IS NULL OR CompletionStatus = 'Не приступал' THEN 1 END) AS NotStartedSubTasks,
        AVG(CAST(Score AS FLOAT)) AS AverageScore,
        MIN(StartDate) AS FirstStartDate,
		MAX(CompletionDate) AS LastCompletedDate
    FROM StudentTasks
    WHERE 
        (@StudentID IS NULL OR StudentID = @StudentID)
        AND (@SubjectID IS NULL OR SubTaskID IN (
            SELECT SubTaskID FROM SubTasks s
            JOIN Tasks t ON t.TaskID = s.TaskID
            WHERE t.SubjectID = @SubjectID
        ))
        AND (@VariantID IS NULL OR SubTaskID IN (
            SELECT SubTaskID FROM SubTasks WHERE VariantID = @VariantID
        ));
END
GO
/*
exec GetStudentTasksStats @StudentID=2
exec GetStudentTasksStats @SubjectID=10
exec GetStudentTasksStats @VariantID=8
*/