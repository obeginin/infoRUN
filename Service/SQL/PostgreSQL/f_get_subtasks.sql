DROP FUNCTION IF EXISTS get_subtasks(
    INT, INT, INT, INT,
    VARCHAR, DATE, VARCHAR,
    VARCHAR, VARCHAR,
    VARCHAR, VARCHAR,
    INT, INT
);

CREATE OR REPLACE FUNCTION get_subtasks(
    subtask_id INT DEFAULT NULL,
    task_id INT DEFAULT NULL,
    subject_id INT DEFAULT NULL,
    variant_id INT DEFAULT NULL,
    search VARCHAR DEFAULT NULL,
    created_date DATE DEFAULT NULL,
    creator VARCHAR DEFAULT NULL,
    sort_column1 VARCHAR DEFAULT 'SubTaskID',
    sort_column2 VARCHAR DEFAULT 'SubTaskID',
    sort_direction1 VARCHAR DEFAULT 'ASC',
    sort_direction2 VARCHAR DEFAULT 'ASC',
    p_offset INT DEFAULT 0,
    p_limit INT DEFAULT 500000
)
RETURNS TABLE (
    "SubTaskID" INT,
    "SubTaskNumber" TEXT,
    "SubjectID" INT,
    "SubjectName" VARCHAR(100),
    "EnglishName" VARCHAR(100),
    "TaskID" INT,
    "TaskTitle" VARCHAR,
    "VariantID" INT,
    "VariantName" VARCHAR,
    "TypeVariant" VARCHAR,
    "YearVariant" VARCHAR,
    "NumberVariant" INT,
    "DifficultyLevel" INT,
    "Description" TEXT,
    "Blocks" TEXT,
    "Comment" TEXT,
    "Creator" VARCHAR(255),
    "CreatedDate" TIMESTAMP,
    "Editor" VARCHAR(255),
    "EditedDate" TIMESTAMP
)
LANGUAGE sql
AS $$
    SELECT 
        s."SubTaskID",
        s."SubTaskNumber",
        sb."ID" AS "SubjectID",
        sb."Name" AS "SubjectName",
        sb."EnglishName",
        t."TaskID",
        t."TaskTitle",
        v."VariantID",
        v."VariantName",
        v."Type" AS "TypeVariant",
        v."Year" AS "YearVariant",
        v."Number" AS "NumberVariant",
        v."DifficultyLevel",
        s."Description",
        s."Blocks",
        v."Comment" AS "Comment",
        s."Creator",
        s."CreatedDate",
        s."Editor",
        s."EditedDate"
    FROM "SubTasks" s
    LEFT JOIN "Tasks" t ON t."TaskID" = s."TaskID"
    LEFT JOIN "Variants" v ON v."VariantID" = s."VariantID"
    LEFT JOIN "Subjects" sb ON sb."ID" = t."SubjectID"
    WHERE
        (subtask_id IS NULL OR s."SubTaskID" = subtask_id)
        AND (task_id IS NULL OR s."TaskID" = task_id)
        AND (subject_id IS NULL OR sb."ID" = subject_id)
        AND (variant_id IS NULL OR v."VariantID" = variant_id)
		AND (creator IS NULL OR s."Creator" = creator)
		
        AND (
            search IS NULL
            OR s."Blocks"::text ILIKE '%' || search || '%'
            OR t."TaskTitle" ILIKE '%' || search || '%'
            OR v."VariantName" ILIKE '%' || search || '%'
            OR v."Comment" ILIKE '%' || search || '%'
        )
    ORDER BY
        CASE WHEN sort_column1 = 'SubTaskID' AND sort_direction1 = 'ASC' THEN s."SubTaskID" END ASC,
        CASE WHEN sort_column1 = 'SubTaskNumber' AND sort_direction1 = 'ASC' THEN s."SubTaskNumber" END ASC,
        CASE WHEN sort_column2 = 'SubTaskID' AND sort_direction2 = 'ASC' THEN s."SubTaskID" END ASC,
        CASE WHEN sort_column2 = 'SubTaskNumber' AND sort_direction2 = 'ASC' THEN s."SubTaskNumber" END ASC,
        CASE WHEN sort_column1 = 'SubTaskID' AND sort_direction1 = 'DESC' THEN s."SubTaskID" END DESC,
        CASE WHEN sort_column1 = 'SubTaskNumber' AND sort_direction1 = 'DESC' THEN s."SubTaskNumber" END DESC,
        CASE WHEN sort_column2 = 'SubTaskID' AND sort_direction2 = 'DESC' THEN s."SubTaskID" END DESC,
        CASE WHEN sort_column2 = 'SubTaskNumber' AND sort_direction2 = 'DESC' THEN s."SubTaskNumber" END DESC
    OFFSET COALESCE(p_offset, 0)
    LIMIT COALESCE(p_limit, 500000);
$$;
-- Пример вызова:
--
--SELECT * FROM get_subtasks();
--SELECT * FROM get_subtasks(subtask_id := 4);