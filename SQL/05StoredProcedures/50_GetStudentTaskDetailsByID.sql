/*
С помощью данного скрипта находм все данные задачи выбранного студента по StudentTaskID

exec GetStudentTaskDetailsByID @StudentTaskID=1
EXEC dbo.GetStudentTaskDetails 1

*/
IF EXISTS(SELECT 1 FROM sys.procedures WHERE OBJECT_SCHEMA_NAME([object_id]) = 'dbo' and name = 'GetStudentTaskDetailsByID')
	DROP PROCEDURE dbo.GetStudentTaskDetailsByID
GO

CREATE PROCEDURE GetStudentTaskDetailsByID
    @StudentTaskID INT
AS
BEGIN
    SELECT 
        st.StudentTaskID, 
        st.StudentID,
        st.SubTaskID,
        st.StudentAnswer,
        st.CompletionStatus, 
        st.Score,
        st.CompletionDate,
		st.SolutionStudentPath,
        sd.Login,
        sd.Role,
        s.TaskID,
		t.TaskTitle,
        s.SubTaskNumber,
        s.ImagePath,
        s.Description,
        s.Answer,
        s.SolutionPath
    FROM StudentTasks st
        JOIN Students sd ON sd.ID = st.StudentID 
        JOIN SubTasks s ON s.SubTaskID = st.SubTaskID
		JOIN Tasks t on t.TaskID = s.TaskID
    WHERE st.StudentTaskID = @StudentTaskID;
END
GO