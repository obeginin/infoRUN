DROP FUNCTION IF EXISTS GetSubtasks(
    INT, INT, INT, INT,
    VARCHAR, DATE, VARCHAR,
    VARCHAR, VARCHAR,
    VARCHAR, VARCHAR,
    INT, INT
);

CREATE OR REPLACE FUNCTION GetSubtasks(
    p_subtask_id INT DEFAULT NULL,
    p_task_id INT DEFAULT NULL,
    p_subject_id INT DEFAULT NULL,
    p_variant_id INT DEFAULT NULL,
    p_search VARCHAR DEFAULT NULL,
    p_upload_date DATE DEFAULT NULL,
    p_creator VARCHAR DEFAULT NULL,
    p_sort_column1 VARCHAR DEFAULT NULL,
    p_sort_column2 VARCHAR DEFAULT NULL,
    p_sort_direction1 VARCHAR DEFAULT 'ASC',
    p_sort_direction2 VARCHAR DEFAULT 'ASC',
    p_offset INT DEFAULT 0,
    p_limit INT DEFAULT 500000
)
RETURNS TABLE (
    subtaskid INT,
    subtasknumber VARCHAR,
    subjectid INT,
    subjectname VARCHAR,
    description TEXT,
    taskid INT,
    tasktitle VARCHAR,
    variantid INT,
    variantname VARCHAR,
    typevariant VARCHAR,
    yearvariant VARCHAR,
    numbervariant INT,
    difficultylevel INT,
    blocks JSONB,
    comment TEXT,
    uploaddate DATE,
    creator VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    EXECUTE format(
        $f$
        SELECT 
            s.subtaskid,
            s.subtasknumber,
            sb.id AS subjectid,
            sb.name AS subjectname,
            sb.description,
            t.taskid,
            t.tasktitle,
            v.variantid,
            v.variantname,
            v.type AS typevariant,
            v.year AS yearvariant,
            v.number AS numbervariant,
            v.difficultylevel,
            s.blocks,
            v.comment,
            s.uploaddate,
            s.creator
        FROM subtasks s
        JOIN tasks t ON t.taskid = s.taskid
        JOIN variants v ON v.variantid = s.variantid
        JOIN subjects sb ON sb.id = t.subjectid
        WHERE 
            ($1 IS NULL OR s.subtaskid = $1)
            AND ($2 IS NULL OR s.taskid = $2)
            AND ($3 IS NULL OR sb.id = $3)
            AND ($4 IS NULL OR v.variantid = $4)
            AND (
                $5 IS NULL
                OR s.blocks::text ILIKE '%%' || $5 || '%%'
                OR t.tasktitle ILIKE '%%' || $5 || '%%'
                OR v.variantname ILIKE '%%' || $5 || '%%'
                OR v.comment ILIKE '%%' || $5 || '%%'
            )
        ORDER BY %I %s
        LIMIT $12 OFFSET $11
        $f$,
        COALESCE(p_sort_column1, 's.subtaskid'),  -- основная колонка сортировки
        COALESCE(p_sort_direction1, 'ASC')
    )
    USING p_subtask_id, p_task_id, p_subject_id, p_variant_id, p_search,
          p_upload_date, p_creator, p_sort_column1, p_sort_column2,
          p_sort_direction1, p_sort_direction2, p_limit, p_offset;
END;
$$;

-- Пример вызова:
SELECT * FROM get_subtask();
SELECT * FROM get_subtask(p_subtask_id := 2);