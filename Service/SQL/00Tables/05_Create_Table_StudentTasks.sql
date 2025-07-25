IF EXISTS(SELECT 1 FROM sys.procedures WHERE OBJECT_SCHEMA_NAME([object_id]) = 'dbo' and name = 'Create_Table_StudentTasks')
	DROP PROCEDURE dbo.Create_Table_StudentTasks
GO

--Создаем Хранимку, которая создает таблицу с задачами--
CREATE PROCEDURE Create_Table_StudentTasks
AS
BEGIN
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'StudentTasks')
	BEGIN
		CREATE TABLE StudentTasks (
		StudentTaskID INT IDENTITY(1,1) PRIMARY KEY,			-- id задачи студента
		StudentID bigint NOT NULL,								-- id студента
		SubTaskID INT NOT NULL,									-- id задачи
		StudentAnswer NVARCHAR(32),								-- Ответ студента
		CompletionStatus NVARCHAR(20) CHECK (CompletionStatus IN ('Не приступал', 'В процессе', 'Выполнено')),	-- Статус выполнения
		Score DECIMAL(5,2) NULL,								-- Баллы за подзадачу
		SolutionStudentPath NVARCHAR(255),						-- Решение задачи Студента
		StartDate DATETIME NULL,								-- Дата начала выполнения задания
		ModifiedDate DATETIME NULL,								-- Дата изменения 
		CompletionDate DATETIME NULL,							-- Дата когда был получен правильный ответ
		DeadlineDate DATETIME NULL,								-- Срок выполнения
		Attempts INT DEFAULT 0,									-- количество попыток
		FOREIGN KEY (StudentID) REFERENCES Students(ID),		-- внешний ключ на id студента
		FOREIGN KEY (SubTaskID) REFERENCES SubTasks(SubTaskID)	-- внешний ключ на id задачи
		);
	END
END

/*
exec dbo.Create_Table_StudentTasks

update StudentTasks set Attempts=0
select * from StudentTasks


drop table StudentTasks
*/

/*
Добавление столбцов в таблицу
Alter TABLE StudentTasks 
ADD
		StudentAnswer NVARCHAR(32) --Ответ ученика
GO
*/

/*
Ошибка:
Конфликт инструкции UPDATE с ограничением CHECK "CK__StudentTa__Compl__7DCDAAA2". Конфликт произошел в базе данных "BASE", таблица "dbo.StudentTasks", column 'CompletionStatus'.
Для обновления данных, которое не разрешено по ограничению 
SELECT name 
FROM sys.check_constraints 
WHERE parent_object_id = OBJECT_ID('dbo.StudentTasks');

снимаем ограничение
ALTER TABLE StudentTasks
DROP CONSTRAINT CK_StudentTasks_CompletionStatus;

обновляем данные

update StudentTasks set CompletionStatus='Выполнено' where StudentTaskID=1

ставим новое ограничение
ALTER TABLE StudentTasks
ADD CONSTRAINT CK_StudentTasks_CompletionStatus
CHECK (CompletionStatus IN ('Не приступал', 'В процессе', 'Выполнено'));


ALTER TABLE StudentTasks ADD DeadlineDate DATE NULL

*/
update StudentTasks set DeadlineDate=CAST(GETDATE() AS DATE)  where StudentTaskID=2