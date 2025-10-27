
--DROP FUNCTION get_students_tasks
CREATE OR REPLACE FUNCTION get_students_tasks(
    student_task_id INT DEFAULT NULL,
    student_id INT DEFAULT NULL,
    sub_task_id INT DEFAULT NULL,
    task_id INT DEFAULT NULL,
    subject_id INT DEFAULT NULL,
    variant_id INT DEFAULT NULL,
    completion_status VARCHAR DEFAULT NULL,
    search VARCHAR DEFAULT NULL,
    sort_column1 VARCHAR DEFAULT 'StudentTaskID',
    sort_column2 VARCHAR DEFAULT NULL,
    sort_direction1 VARCHAR DEFAULT 'ASC',
    sort_direction2 VARCHAR DEFAULT 'ASC',
    p_offset INT DEFAULT 0,
    p_limit INT DEFAULT 500000
)
RETURNS TABLE(
    "StudentTaskID" INT,
    "StudentID" BIGINT,
    "SubTaskID" INT,
    "StudentAnswer" VARCHAR,
    "CompletionStatus" VARCHAR,
    "Score" NUMERIC,
    "StartDate" TIMESTAMP,
    "ModifiedDate" TIMESTAMP,
    "CompletionDate" TIMESTAMP,
    "DeadlineDate" TIMESTAMP,
    "Attempts" INT,
    "Login" VARCHAR,
    "SubjectID" INT,
    "SubjectName" VARCHAR,
    "TaskID" INT,
    "TaskTitle" VARCHAR,
    "SubTaskNumber" TEXT,
    "Blocks" TEXT,
    "Description" TEXT,
    "VariantID" INT,
    "VariantName" VARCHAR,
    "TypeVariant" VARCHAR,
    "YearVariant" VARCHAR,
    "NumberVarinat" INT,
    "DifficultyLevel" INT,
    "Comment" VARCHAR
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
        s."Blocks",
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
        (student_task_id IS NULL OR st."StudentTaskID" = student_task_id)
        AND (student_id IS NULL OR st."StudentID" = student_id)
        AND (sub_task_id IS NULL OR st."SubTaskID" = sub_task_id)
        AND (task_id IS NULL OR s."TaskID" = task_id)
        AND (subject_id IS NULL OR sj."ID" = subject_id)
        AND (variant_id IS NULL OR v."VariantID" = variant_id)
        AND (completion_status IS NULL OR st."CompletionStatus" = completion_status)
        AND (
            search IS NULL
            OR s."Description" ILIKE '%' || search || '%'
            OR sd."Login" ILIKE '%' || search || '%'
            OR v."VariantName" ILIKE '%' || search || '%'
            OR v."Comment" ILIKE '%' || search || '%'
        )
    ORDER BY
        -- ASC CASEs
        CASE WHEN sort_column1 = 'StudentTaskID' AND sort_direction1 = 'ASC' THEN st."StudentTaskID" END ASC,
        CASE WHEN sort_column1 = 'StudentID' AND sort_direction1 = 'ASC' THEN st."StudentID" END ASC,
        CASE WHEN sort_column1 = 'SubTaskID' AND sort_direction1 = 'ASC' THEN st."SubTaskID" END ASC,
        CASE WHEN sort_column1 = 'TaskID' AND sort_direction1 = 'ASC' THEN s."TaskID" END ASC,
        CASE WHEN sort_column1 = 'SubjectID' AND sort_direction1 = 'ASC' THEN sj."ID" END ASC,
        CASE WHEN sort_column1 = 'VariantID' AND sort_direction1 = 'ASC' THEN v."VariantID" END ASC,
        CASE WHEN sort_column1 = 'StartDate' AND sort_direction1 = 'ASC' THEN st."StartDate" END ASC,
        CASE WHEN sort_column1 = 'ModifiedDate' AND sort_direction1 = 'ASC' THEN st."ModifiedDate" END ASC,
        CASE WHEN sort_column1 = 'CompletionDate' AND sort_direction1 = 'ASC' THEN st."CompletionDate" END ASC,
        CASE WHEN sort_column1 = 'DeadlineDate' AND sort_direction1 = 'ASC' THEN st."DeadlineDate" END ASC,
        CASE WHEN sort_column1 = 'Attempts' AND sort_direction1 = 'ASC' THEN st."Attempts" END ASC,
        CASE WHEN sort_column1 = 'TypeVariant' AND sort_direction1 = 'ASC' THEN v."Type" END ASC,
        CASE WHEN sort_column1 = 'YearVariant' AND sort_direction1 = 'ASC' THEN v."Year" END ASC,
        CASE WHEN sort_column1 = 'NumberVarinat' AND sort_direction1 = 'ASC' THEN v."Number"::INTEGER ELSE NULL::INTEGER END ASC,
        CASE WHEN sort_column1 = 'DifficultyLevel' AND sort_direction1 = 'ASC' THEN v."DifficultyLevel" END ASC,
        -- DESC CASEs


        CASE WHEN sort_column1 = 'StudentTaskID' AND sort_direction1 = 'DESC' THEN st."StudentTaskID" END DESC,
        CASE WHEN sort_column1 = 'StudentID' AND sort_direction1 = 'DESC' THEN st."StudentID" END DESC,
        CASE WHEN sort_column1 = 'SubTaskID' AND sort_direction1 = 'DESC' THEN st."SubTaskID" END DESC,
        CASE WHEN sort_column1 = 'TaskID' AND sort_direction1 = 'DESC' THEN s."TaskID" END DESC,
        CASE WHEN sort_column1 = 'SubjectID' AND sort_direction1 = 'DESC' THEN sj."ID" END DESC,
        CASE WHEN sort_column1 = 'VariantID' AND sort_direction1 = 'DESC' THEN v."VariantID" END DESC,
        CASE WHEN sort_column1 = 'StartDate' AND sort_direction1 = 'DESC' THEN st."StartDate" END DESC,
        CASE WHEN sort_column1 = 'ModifiedDate' AND sort_direction1 = 'DESC' THEN st."ModifiedDate" END DESC,
        CASE WHEN sort_column1 = 'CompletionDate' AND sort_direction1 = 'DESC' THEN st."CompletionDate" END DESC,
        CASE WHEN sort_column1 = 'DeadlineDate' AND sort_direction1 = 'DESC' THEN st."DeadlineDate" END DESC,
        CASE WHEN sort_column1 = 'Attempts' AND sort_direction1 = 'DESC' THEN st."Attempts" END DESC,
        CASE WHEN sort_column1 = 'TypeVariant' AND sort_direction1 = 'DESC' THEN v."Type" END DESC,
        CASE WHEN sort_column1 = 'YearVariant' AND sort_direction1 = 'DESC' THEN v."Year" END DESC,
		CASE WHEN sort_column1 = 'NumberVarinat' AND sort_direction1 = 'DESC' THEN v."Number"::INTEGER ELSE NULL::INTEGER END DESC,        
        CASE WHEN sort_column1 = 'DifficultyLevel' AND sort_direction1 = 'DESC' THEN v."DifficultyLevel" END DESC
    OFFSET COALESCE(p_offset, 0)
    LIMIT COALESCE(p_limit, 500000);
END;
$$ LANGUAGE plpgsql;
--drop function get_students_tasks
--select * from get_students_tasks()