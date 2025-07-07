
-- таблица с ролями ()
CREATE TABLE Roles (
    RoleID INT PRIMARY KEY IDENTITY(1,1),
    Name NVARCHAR(50) NOT NULL UNIQUE,
);
--insert into Roles (Name) Values ('Админ'), ('Учитель'), ('Ученик')

CREATE TABLE Permissions (
    PermissionID INT PRIMARY KEY IDENTITY(1,1),
    Name NVARCHAR(50) NOT NULL UNIQUE,
    Description NVARCHAR(255)
);
--insert into Permissions (Name, Description) Values ('view_tasks','Просмотр задач'),('creat_tasks','Создание задач'),('edit_tasks','Редактирование  задач'),('admin_panel','Административная панель')


CREATE TABLE RolePermissions (
    RoleID INT NOT NULL,
    PermissionID INT NOT NULL,
    PRIMARY KEY (RoleID, PermissionID),								-- первичный ключ сразу на два поля
    FOREIGN KEY (RoleID) REFERENCES Roles(RoleID),					-- внешний ключ (ссылаемся на id роли)
    FOREIGN KEY (PermissionID) REFERENCES Permissions(PermissionID) -- внешний ключ (ссылаемся на id разрешения)
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
ORDER BY r.RoleID


/*
интересный запрос с группировкой по полям
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