IF EXISTS(SELECT 1 FROM sys.procedures WHERE OBJECT_SCHEMA_NAME([object_id]) = 'dbo' and name = 'Create_Table_Password_Reset_Tokens')
	DROP PROCEDURE dbo.Create_Table_Password_Reset_Tokens
GO

--������� ��������, ������� ������� ������� Students--
/*� ������ ������� �������� ������ ��� ������ ������ ������������*/
CREATE PROCEDURE Create_Table_Password_Reset_Tokens
AS
BEGIN
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'PasswordResetTokens')
	BEGIN
		CREATE TABLE PasswordResetTokens (
			ID INT IDENTITY(1,1) PRIMARY KEY,					-- id ������
			StudentID BIGINT NOT NULL,								-- id ��������
			Token NVARCHAR(255) NOT NULL UNIQUE,				-- ��� �����
			ExpiresAt DATETIME2 NOT NULL,						-- ���� �������� ������ (1 ���).
			Used BIT NOT NULL DEFAULT 0,						-- ���������� ����, ������� ����������, ����������� �� �����.
			CreatedAt DATETIME2 NOT NULL DEFAULT GETDATE(),	-- ���� ��� �����

			CONSTRAINT FK_PasswordResetTokens_Students FOREIGN KEY (StudentID)
				REFERENCES Students(ID)
				ON DELETE CASCADE
		);
	END
END;

--exec Create_Table_Password_Reset_Tokens