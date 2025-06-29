
IF EXISTS(SELECT 1 FROM sys.procedures WHERE OBJECT_SCHEMA_NAME([object_id]) = 'dbo' and name = 'Create_Table_Variants')
	DROP PROCEDURE dbo.Create_Table_Variants
GO

CREATE PROCEDURE dbo.Create_Table_Variants
AS
BEGIN
	IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Variants')
	BEGIN
		CREATE TABLE Variants (
			VariantID INT PRIMARY KEY IDENTITY(1,1),
			VariantName NVARCHAR(255),           -- Человеко-понятное название (например, "Контрольная работа")
			Type NVARCHAR(100),           -- Тип (например, "Вариант", "Контрольная", "Олимпиада", "Практика")
			Year NVARCHAR(100),
			Number INT NULL,              -- Номер, если применимо (1, 2, 3 и т.д.)
			DifficultyLevel int,  -- Уровень сложности (например, )
			Comment NVARCHAR(100)
		);
	END
END;


/*
exec dbo.Create_Table_Variants
INSERT INTO SubTasks (TaskID, SubTaskNumber, Description) VALUES (1,'1.1','1 ������');
select * from Variants
DROP PROCEDURE dbo.Create_Table_Variants
drop table Variants

ALTER TABLE Variants ADD Comment INT;

*/

/*
select * FROM SubTasks S
JOIN Variants V ON S.Description = V.Name;


переносим данные в новую таблицу
INSERT INTO Variants (Name)
SELECT DISTINCT Description
FROM SubTasks
WHERE Description IS NOT NULL;
*/


/*
UPDATE S
SET S.VariantID = V.VariantID
FROM SubTasks S
JOIN Variants V ON S.Description = V.Name;
*/

SELECT * FROM SubTasks s
                            LEFT JOIN Variants v on s.VariantID = v.VariantID where TaskID=1

							EXEC sp_rename 'Variants.Name', 'VariantName', 'COLUMN';
