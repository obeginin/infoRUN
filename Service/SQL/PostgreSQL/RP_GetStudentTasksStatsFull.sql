CREATE OR REPLACE FUNCTION GetStudentTasksStatsFull(
    p_StudentID INT DEFAULT NULL
)
RETURNS TABLE(
    StudentID INT,
    Description TEXT,
    Done INT,
    InProgress INT,
    NoStart INT,
    TotalSubVar INT
) AS $$
BEGIN
    -- Детальная статистика по каждому SubTask
    RETURN QUERY
    SELECT 
        st."StudentID",
        s."Description",
        COUNT(CASE WHEN st."CompletionStatus" = 'Выполнено' THEN 1 END) AS Done,
        COUNT(CASE WHEN st."CompletionStatus" = 'В процессе' THEN 1 END) AS InProgress,
        COUNT(CASE WHEN st."CompletionStatus" = 'Не приступал' THEN 1 END) AS NoStart,
        COUNT(*) AS TotalSubVar
    FROM "StudentTasks" st
        JOIN "Students" sd ON sd."ID" = st."StudentID"
        JOIN "SubTasks" s ON s."SubTaskID" = st."SubTaskID"
        JOIN "Tasks" t ON t."TaskID" = s."TaskID"
    WHERE (p_StudentID IS NULL OR st."StudentID" = p_StudentID)
    GROUP BY st."StudentID", s."Description"

    UNION ALL

    -- Итоговая строка по всем вариантам студента
    SELECT
        p_StudentID AS StudentID,
        'ИТОГО' AS Description,
        SUM(Done) AS Done,
        SUM(InProgress) AS InProgress,
        SUM(NoStart) AS NoStart,
        SUM(TotalSubVar) AS TotalSubVar
    FROM (
        SELECT
            COUNT(CASE WHEN st."CompletionStatus" = 'Выполнено' THEN 1 END) AS Done,
            COUNT(CASE WHEN st."CompletionStatus" = 'В процессе' THEN 1 END) AS InProgress,
            COUNT(CASE WHEN st."CompletionStatus" = 'Не приступал' THEN 1 END) AS NoStart,
            COUNT(*) AS TotalSubVar
        FROM "StudentTasks" st
        WHERE (p_StudentID IS NULL OR st."StudentID" = p_StudentID)
        GROUP BY st."StudentID", st."SubTaskID"
    ) AS sub;
END;
$$ LANGUAGE plpgsql;