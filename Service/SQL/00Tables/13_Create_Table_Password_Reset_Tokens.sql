IF EXISTS(SELECT 1 FROM sys.procedures WHERE OBJECT_SCHEMA_NAME([object_id]) = 'dbo' and name = 'Create_Table_Password_Reset_Tokens')
	DROP PROCEDURE dbo.Create_Table_Password_Reset_Tokens
GO

--—оздаем ’ранимку, котора€ создает таблицу Students--
/*¬ данной таблице хран€тс€ токены дл€ сброса парол€ пользовател€*/
CREATE PROCEDURE Create_Table_Password_Reset_Tokens
AS
BEGIN
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'PasswordResetTokens')
	BEGIN
		CREATE TABLE PasswordResetTokens (
			ID INT IDENTITY(1,1) PRIMARY KEY,					-- id токена
			StudentID BIGINT NOT NULL,								-- id студента
			Token NVARCHAR(255) NOT NULL UNIQUE,				-- сам токен
			ExpiresAt DATETIME2 NOT NULL,						-- срок действи€ токена (1 час).
			Used BIT NOT NULL DEFAULT 0,						-- логическое поле, которое показывает, использован ли токен.
			CreatedAt DATETIME2 NOT NULL DEFAULT GETDATE(),	-- ƒата дл€ логов

			CONSTRAINT FK_PasswordResetTokens_Students FOREIGN KEY (StudentID)
				REFERENCES Students(ID)
				ON DELETE CASCADE
		);
	END
END;

--exec Create_Table_Password_Reset_Tokens