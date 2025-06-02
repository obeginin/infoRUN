/*
� ������� ������� ������� ������ ��������� ���������� � ��������� ������ �������� �� StudentTaskID

exec GetStudentTaskDetailsByID @StudentTaskID=1
EXEC dbo.GetStudentTaskDetails 1

*/
IF EXISTS(SELECT 1 FROM sys.procedures WHERE OBJECT_SCHEMA_NAME([object_id]) = 'dbo' and name = 'GetStudentsTasks')
	DROP PROCEDURE dbo.GetStudentsTasks
GO

CREATE PROCEDURE GetStudentsTasks
    @StudentTaskID INT = NULL,
    @StudentID INT = NULL,
    @SubTaskID INT = NULL,
    @TaskID INT = NULL,
    @CompletionStatus NVARCHAR(20) = NULL, 
	@SortColumn NVARCHAR(50) = NULL, -- ����� ���� ��� ����������
    @SortDirection NVARCHAR(4) = 'ASC', -- ����� ���������� (�� ��������� ASC �� �����������) DESC -�� ��������
	@Description  NVARCHAR(MAX)
AS
BEGIN
	/*���������� ����� � ��������� SSMS
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
		(SELECT COUNT(*) FROM StudentTasks) AS TotalSubTasks, --���������� ����� ��������
		(SELECT COUNT(*) FROM StudentTasks where CompletionStatus='���������') AS CompletedSubTasks, --���������� ������� ����� ��������
		COUNT(*) OVER() AS TotalCount --  ��������� ����� ���������� ���� ��������� �������
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

EXEC GetStudentsTasks; ����� ���� ����� ���� ���������
EXEC GetStudentsTasks @StudentID = 2; ����� ���� ����� �������� � id=2
EXEC GetStudentsTasks @TaskID = 2; �� ��������� �������
EXEC GetStudentsTasks @SubTaskID = 2, @CompletionStatus = N'�� ���������';
EXEC GetStudentsTasks @CompletionStatus = N'���������'; �� ������� ����������
EXEC GetStudentsTasks @StudentTaskID = 2; ���������� ������
EXEC GetStudentsTasks @Description = N'���� 2025'; ���������� ������

� ����������� 
EXEC GetStudentTaskDetailsByID @SortColumn = 'StudentTaskID', @SortDirection = 'ASC';
EXEC GetStudentTaskDetailsByID @SortColumn = 'StudentTaskID', @SortDirection = 'DESC';
EXEC GetStudentTaskDetailsByID @SortColumn = 'TaskID', @SortDirection = 'ASC';
EXEC GetStudentTaskDetailsByID @SortColumn = 'TaskID', @SortDirection = 'DESC';

EXEC GetStudentTaskDetailsByID @SortColumn = 'CompletionDate', @SortDirection = 'ASC'; ���������� �� ���� �� ��������:
EXEC GetStudentTaskDetailsByID @SortColumn = 'CompletionDate', @SortDirection = 'DESC'; ���������� �� ���� �� ��������:

���������� �� ������������
EXEC GetStudentTaskDetailsByID @SortColumn = 'StudentID', @SortDirection = 'ASC';
EXEC GetStudentTaskDetailsByID @SortColumn = 'StudentID', @SortDirection = 'DESC';
EXEC GetStudentTaskDetailsByID @SortColumn = 'Login', @SortDirection = 'ASC';
EXEC GetStudentTaskDetailsByID @SortColumn = 'Login', @SortDirection = 'DESC';


EXEC GetStudentTaskDetailsByID @StudentID = 1, @SortColumn = 'StudentTaskID', @SortDirection = 'ASC';
*/ 

/*
select* from Tasks
select* from SubTasks
select* from StudentTasks
select ID, Login from Students
select distinct Description from SubTasks
SELECT TaskTitle FROM Tasks
*/

