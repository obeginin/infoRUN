--������� ��������, ������� ������� ���� ������ BASE--
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'infoRUN')
BEGIN
    CREATE DATABASE infoRUN;
END
GO  -- ��������� �����

USE infoRUN
GO  -- ��������� ������������� ����


