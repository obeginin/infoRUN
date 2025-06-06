/*
Статистика студента

exec GetStudentsTasks @StudentTaskID=1
EXEC dbo.GetStudentTaskDetails 1

*/
IF EXISTS(SELECT 1 FROM sys.procedures WHERE OBJECT_SCHEMA_NAME([object_id]) = 'dbo' and name = 'GetStatisticStudent')
	DROP PROCEDURE dbo.GetStatisticStudent
GO
CREATE PROCEDURE dbo.GetStatisticStudent