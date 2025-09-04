CREATE OR REPLACE FUNCTION GetStudentsTasks(
    p_StudentTaskID INT DEFAULT NULL,
    p_StudentID INT DEFAULT NULL,
    p_SubTaskID INT DEFAULT NULL,
    p_TaskID INT DEFAULT NULL,
    p_SubjectID INT DEFAULT NULL,
    p_VariantID INT DEFAULT NULL,
    p_CompletionStatus VARCHAR DEFAULT NULL,
    p_Search VARCHAR DEFAULT NULL,
    p_SortColumn1 VARCHAR DEFAULT 'StudentTaskID',
    p_SortColumn2 VARCHAR DEFAULT NULL,
    p_SortDirection1 VARCHAR DEFAULT 'ASC',
    p_SortDirection2 VARCHAR DEFAULT 'ASC',
    p_Offset INT DEFAULT 0,
    p_Limit INT DEFAULT 500000
)
RETURNS TABLE(
    StudentTaskID INT,
    StudentID INT,
    SubTaskID INT,
    StudentAnswer VARCHAR,
    CompletionStatus VARCHAR,
    Score NUMERIC,
    StartDate TIMESTAMP,
    ModifiedDate TIMESTAMP,
    CompletionDate TIMESTAMP,
    DeadlineDate TIMESTAMP,
    Attempts INT,
    Login VARCHAR,
    SubjectID INT,
    SubjectName VARCHAR,
    TaskID INT,
    TaskTitle VARCHAR,
    SubTaskNumber INT,
    ImagePath VARCHAR,
    Description TEXT,
    VariantID INT,
    VariantName VARCHAR,
    TypeVariant VARCHAR,
    YearVariant VARCHAR,
    NumberVarinat INT,
    DifficultyLevel INT,
    Comment VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        st."StudentTaskID",
        st."StudentID",
        st."SubTaskID",
        st."StudentAnswer",
        st."CompletionStatus",
        st."Score",
        st."StartDate",
        st."ModifiedDate",
        st."CompletionDate",
        st."DeadlineDate",
        st."Attempts",
        sd."Login",
        sj."ID" as "SubjectID",
        sj."Name" as "SubjectName",
        t."TaskID",
        t."TaskTitle",
        s."SubTaskNumber",
        s."ImagePath",
        s."Description",
        v."VariantID",
        v."VariantName",
        v."Type" as "TypeVariant",
        v."Year" as "YearVariant",
        v."Number" as "NumberVarinat",
        v."DifficultyLevel",
        v."Comment"
    FROM "StudentTasks" st
        LEFT JOIN "Students" sd ON sd."ID" = st."StudentID"
        LEFT JOIN "SubTasks" s ON s."SubTaskID" = st."SubTaskID"
        LEFT JOIN "Tasks" t ON t."TaskID" = s."TaskID"
        LEFT JOIN "Variants" v ON v."VariantID" = s."VariantID"
        LEFT JOIN "Subjects" sj ON sj."ID" = t."SubjectID"
    WHERE 
        (p_StudentTaskID IS NULL OR st."StudentTaskID" = p_StudentTaskID)
        AND (p_StudentID IS NULL OR st."StudentID" = p_StudentID)
        AND (p_SubTaskID IS NULL OR st."SubTaskID" = p_SubTaskID)
        AND (p_TaskID IS NULL OR s."TaskID" = p_TaskID)
        AND (p_SubjectID IS NULL OR sj."ID" = p_SubjectID)
        AND (p_VariantID IS NULL OR v."VariantID" = p_VariantID)
        AND (p_CompletionStatus IS NULL OR st."CompletionStatus" = p_CompletionStatus)
        AND (
            p_Search IS NULL
            OR s."Description" ILIKE '%' || p_Search || '%'
            OR sd."Login" ILIKE '%' || p_Search || '%'
            OR v."VariantName" ILIKE '%' || p_Search || '%'
            OR v."Comment" ILIKE '%' || p_Search || '%'
        )
    ORDER BY
        CASE WHEN p_SortDirection1 = 'ASC' THEN
            CASE p_SortColumn1
                WHEN 'StudentTaskID' THEN st."StudentTaskID"
                WHEN 'StudentID' THEN st."StudentID"
                WHEN 'SubTaskID' THEN st."SubTaskID"
                WHEN 'TaskID' THEN s."TaskID"
                WHEN 'SubjectID' THEN sj."ID"
                WHEN 'VariantID' THEN v."VariantID"
                WHEN 'StartDate' THEN st."StartDate"
                WHEN 'ModifiedDate' THEN st."ModifiedDate"
                WHEN 'CompletionDate' THEN st."CompletionDate"
                WHEN 'DeadlineDate' THEN st."DeadlineDate"
                WHEN 'TypeVariant' THEN v."Type"
                WHEN 'YearVariant' THEN v."Year"
                WHEN 'NumberVarinat' THEN v."Number"
                WHEN 'DifficultyLevel' THEN v."DifficultyLevel"
                WHEN 'Attempts' THEN st."Attempts"
            END
        END ASC,
        CASE WHEN p_SortDirection1 = 'DESC' THEN
            CASE p_SortColumn1
                WHEN 'StudentTaskID' THEN st."StudentTaskID"
                WHEN 'StudentID' THEN st."StudentID"
                WHEN 'SubTaskID' THEN st."SubTaskID"
                WHEN 'TaskID' THEN s."TaskID"
                WHEN 'SubjectID' THEN sj."ID"
                WHEN 'VariantID' THEN v."VariantID"
                WHEN 'StartDate' THEN st."StartDate"
                WHEN 'ModifiedDate' THEN st."ModifiedDate"
                WHEN 'CompletionDate' THEN st."CompletionDate"
                WHEN 'DeadlineDate' THEN st."DeadlineDate"
                WHEN 'TypeVariant' THEN v."Type"
                WHEN 'YearVariant' THEN v."Year"
                WHEN 'NumberVarinat' THEN v."Number"
                WHEN 'DifficultyLevel' THEN v."DifficultyLevel"
                WHEN 'Attempts' THEN st."Attempts"
            END
        END DESC
    OFFSET COALESCE(p_Offset, 0)
    LIMIT COALESCE(p_Limit, 500000);
END;
$$ LANGUAGE plpgsql;