--������� ��������, ������� ������� ���� ������ BASE--
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'BASE')
BEGIN
    CREATE DATABASE BASE;
END
GO  -- ��������� �����

USE BASE
GO  -- ��������� ������������� ����


