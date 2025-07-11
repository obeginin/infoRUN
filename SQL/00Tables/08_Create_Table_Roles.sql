
-- ������� � ������ 
CREATE TABLE Roles (
    RoleID INT PRIMARY KEY IDENTITY(1,1),
    Name NVARCHAR(50) NOT NULL UNIQUE,
);
--insert into Roles (Name) Values ('�����'), ('�������'), ('������')

-- ������� � ������������
CREATE TABLE Permissions (
    PermissionID INT PRIMARY KEY IDENTITY(1,1),
    Name NVARCHAR(50) NOT NULL UNIQUE,
    Description NVARCHAR(255)
);
--insert into Permissions (Name, Description) Values ('view_tasks','�������� �����'),('create_tasks','�������� �����'),('edit_tasks','��������������  �����'),('edit_students','���������� ����������'),('admin_panel','���������������� ������')

-- ������� ����� ����� � ����������
update Permissions set Name='create_tasks' where PermissionID=2
CREATE TABLE RolePermissions (
    RoleID INT NOT NULL,
    PermissionID INT NOT NULL,
    PRIMARY KEY (RoleID, PermissionID),								-- ��������� ���� ����� �� ��� ����
    FOREIGN KEY (RoleID) REFERENCES Roles(RoleID),					-- ������� ���� (��������� �� id ����)
    FOREIGN KEY (PermissionID) REFERENCES Permissions(PermissionID) -- ������� ���� (��������� �� id ����������)
);

insert into RolePermissions (RoleID, PermissionID) Values ()
select * from Students
select * from Roles
select * from Permissions
select * from RolePermissions


select * from Students s
left join Roles r on s.RoleID = r.RoleID


SELECT
    r.RoleID,
    r.Name as RoleName,
    p.PermissionID,
    p.Name as PermissionName
FROM RolePermissions rp
JOIN Roles r ON rp.RoleID = r.RoleID
JOIN Permissions p ON rp.PermissionID = p.PermissionID
WHERE r.RoleID = 1
ORDER BY r.RoleID


/*
���������� ������ � ������������ �� �����
SELECT
    r.RoleID,
    r.Name AS RoleName,
    STRING_AGG(p.PermissionID, ',') AS PermissionIDs,
    STRING_AGG(p.Name, ',') AS PermissionNames
FROM RolePermissions rp
JOIN Roles r ON rp.RoleID = r.RoleID
JOIN Permissions p ON rp.PermissionID = p.PermissionID
GROUP BY r.RoleID, r.Name
*/
select s.id, s.Login, s.Password, s.Role, r.RoleID, r.Name as RoleName from Students s 
left join Roles r on s.RoleID = r.RoleID

select s.id, s.Login,  s.Role, r.RoleID, r.Name as RoleName 
                                    from Students s 
                                    left join Roles r on s.RoleID = r.RoleID
                                    where s.Login = 'obeginin'