CREATE OR REPLACE FUNCTION GetStudentTasksStats(
    p_StudentID INT DEFAULT NULL,
    p_SubjectID INT DEFAULT NULL,
    p_VariantID INT DEFAULT NULL
)
RETURNS TABLE(
    TotalSubTasks INT,
    CompletedSubTasks INT,
    InProgressSubTasks INT,
    NotStartedSubTasks INT,
    AverageScore NUMERIC,
    FirstStartDate TIMESTAMP,
    LastCompletedDate TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        COUNT(*) AS TotalSubTasks,
        COUNT(CASE WHEN "CompletionStatus" = 'Выполнено' THEN 1 END) AS CompletedSubTasks,
        COUNT(CASE WHEN "CompletionStatus" = 'В процессе' THEN 1 END) AS InProgressSubTasks,
        COUNT(CASE WHEN "CompletionStatus" IS NULL OR "CompletionStatus" = 'Не приступал' THEN 1 END) AS NotStartedSubTasks,
        AVG("Score") AS AverageScore,
        MIN("StartDate") AS FirstStartDate,
        MAX("CompletionDate") AS LastCompletedDate
    FROM "StudentTasks" st
    WHERE 
        (p_StudentID IS NULL OR st."StudentID" = p_StudentID)
        AND (p_SubjectID IS NULL OR st."SubTaskID" IN (
            SELECT s."SubTaskID"
            FROM "SubTasks" s
            JOIN "Tasks" t ON t."TaskID" = s."TaskID"
            WHERE t."SubjectID" = p_SubjectID
        ))
        AND (p_VariantID IS NULL OR st."SubTaskID" IN (
            SELECT "SubTaskID" FROM "SubTasks" WHERE "VariantID" = p_VariantID
        ));
END;
$$ LANGUAGE plpgsql;