--������� ��������, ������� ������� ���� ������ BASE--
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'infoRUN')
BEGIN
    CREATE DATABASE infoRUN;
	CREATE DATABASE LogDB;
END
GO  -- ��������� �����

USE infoRUN
GO  -- ��������� ������������� ����


