-- Создание баз данных
CREATE DATABASE inforun;
CREATE DATABASE logdb;


-- Таблица с ролями
CREATE TABLE Roles (
    RoleID SERIAL PRIMARY KEY,       -- автоинкремент
    Name VARCHAR(50) NOT NULL UNIQUE
);

INSERT INTO Roles (Name) VALUES ('Админ'), ('Учитель'), ('Ученик');


-- Таблица с разрешениями
CREATE TABLE Permissions (
    PermissionID SERIAL PRIMARY KEY, -- автоинкремент
    Name VARCHAR(50) NOT NULL UNIQUE,
    Description VARCHAR(255)
);

-- Пример вставки разрешений
INSERT INTO Permissions (Name, Description) VALUES 
    ('view_tasks', 'Просмотр задач'),
    ('create_tasks', 'Создание задач'),
    ('edit_tasks', 'Редактирование задач'),
    ('edit_students', 'Управление студентами'),
    ('admin_panel', 'Административная панель');

-- таблица связи ролей и разрешений
CREATE TABLE RolePermissions (
    RoleID INT NOT NULL,
    PermissionID INT NOT NULL,
    PRIMARY KEY (RoleID, PermissionID),                                -- составной первичный ключ
    CONSTRAINT fk_role FOREIGN KEY (RoleID) REFERENCES Roles(RoleID) ON DELETE CASCADE,
    CONSTRAINT fk_permission FOREIGN KEY (PermissionID) REFERENCES Permissions(PermissionID) ON DELETE CASCADE
);

-- Таблица со студентами (пользователями)
CREATE TABLE Students (
    ID BIGSERIAL PRIMARY KEY,                       		-- автоинкрементный id
    Login VARCHAR(50) UNIQUE,                        		-- логин пользователя
    Last_Name VARCHAR(50),
    First_Name VARCHAR(50),
    Middle_Name VARCHAR(50),
    Email VARCHAR(50) UNIQUE,
    Phone VARCHAR(25) UNIQUE,
    Sex CHAR(1) CHECK (Sex IN ('М', 'Ж') OR Sex IS NULL),   -- один символ, проверка
    BirthDate TIMESTAMP,
    Comment TEXT,
    Password VARCHAR(255) NOT NULL,                 		-- хеш пароля
    RoleID INT NOT NULL DEFAULT 3,                  		-- id роли (по умолчанию: "Ученик")
    IsActive BOOLEAN NOT NULL DEFAULT TRUE,         		-- булевый тип (по умолчанию: включен)
    IsDeleted TIMESTAMP NULL,                       		-- дата удаления
    IsConfirmed BOOLEAN NOT NULL DEFAULT FALSE,    			-- подтверждение email
    CONSTRAINT fk_role FOREIGN KEY (RoleID) REFERENCES Roles(RoleID)
);

-- вставить значения
INSERT INTO Students 
    (Login, Last_Name, First_Name, Middle_Name, Email, Sex, BirthDate, Comment, Password, RoleID, IsActive, IsDeleted, IsConfirmed)
VALUES ('obeginin', 'Бегинин', 'Олег', 'Вячеславович','lezhik.from@gmail.com', 'М',NULL,'Комментарий', '$pbkdf2-sha256$29000$3zunFMK4955zjpEyxngPYQ$nECQLRTK9OFP8I6QErp5iVHRy6D4j4/mC7IgkxDGTEY', 1,TRUE,NULL,TRUE);


-- Таблица с предметами
CREATE TABLE Subjects (
    ID SERIAL PRIMARY KEY,             -- автоинкрементный id
    Name VARCHAR(100) NOT NULL UNIQUE, -- название предмета
    Description TEXT NULL              -- описание предмета
);

INSERT INTO Subjects (Name, Description) VALUES
  ('Математика', 'Подготовка к ЕГЭ по математике'),
  ('Русский язык', 'Подготовка к ЕГЭ по русскому языку'),
  ('Физика', 'Подготовка к ЕГЭ по физике'),
  ('Химия', 'Подготовка к ЕГЭ по химии'),
  ('Биология', 'Подготовка к ЕГЭ по биологии'),
  ('История', 'Подготовка к ЕГЭ по истории'),
  ('Обществознание', 'Подготовка к ЕГЭ по обществознанию'),
  ('Литература', 'Подготовка к ЕГЭ по литературе'),
  ('Английский язык', 'Подготовка к ЕГЭ по английскому языку'),
  ('Информатика', 'Подготовка к ЕГЭ по информатике');

-- Таблица с категориями
CREATE TABLE Tasks (
    TaskID SERIAL PRIMARY KEY,         -- автоинкрементный id задачи
    SubjectID INT NOT NULL,            -- id предмета
    TaskNumber INT NOT NULL UNIQUE,    -- номер задачи, уникальный и не NULL
    TaskTitle VARCHAR(255) NOT NULL,   -- название задачи
    CONSTRAINT fk_subject FOREIGN KEY (SubjectID) REFERENCES Subjects(ID) ON DELETE CASCADE
);

-- Таблица с вариантами
CREATE TABLE Variants (
    VariantID SERIAL PRIMARY KEY,           -- автоинкрементный id
    VariantName VARCHAR(255),               -- человеко-понятное название
    Type VARCHAR(100),                      -- тип варианта (например, "Вариант", "Контрольная")
    Year VARCHAR(100),                      -- год варианта
    Number INT NULL,                        -- номер варианта, если применимо
    DifficultyLevel INT,                     -- уровень сложности
    Comment VARCHAR(100)                     -- комментарий
);

-- Таблица подзадач
CREATE TABLE SubTasks (
    SubTaskID SERIAL PRIMARY KEY,                    -- автоинкрементный id
    TaskID INT NOT NULL,                             -- id категории
    SubTaskNumber INT NOT NULL,                      -- номер подзадачи
    VariantID INT,                                   -- id варианта
    ImagePath VARCHAR(255),                          -- путь к изображению
    Description TEXT,                                -- описание задачи
    Answer VARCHAR(32),                              -- ответ (можно перенести в отдельную таблицу)
    SolutionPath VARCHAR(255),                       -- путь к решению
    CONSTRAINT fk_task FOREIGN KEY (TaskID) REFERENCES Tasks(TaskID) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_variant FOREIGN KEY (VariantID) REFERENCES Variants(VariantID) ON UPDATE CASCADE ON DELETE SET NULL
);

-- Таблица изображений подзадач
CREATE TABLE SubTasksImages (
    ID SERIAL PRIMARY KEY,
    SubTaskID INT NOT NULL REFERENCES SubTasks(SubTaskID) ON DELETE CASCADE,
    FileName VARCHAR(255) NOT NULL,
    FilePath VARCHAR(500) NOT NULL,
    UploadDate TIMESTAMP DEFAULT NOW()
);

-- Таблица дополнительных файлов подзадач
CREATE TABLE SubTaskFiles (
    ID SERIAL PRIMARY KEY,
    SubTaskID INT NOT NULL REFERENCES SubTasks(SubTaskID) ON DELETE CASCADE,
    FileName VARCHAR(255),
    FilePath VARCHAR(500),
    UploadDate TIMESTAMP DEFAULT NOW()
);

-- Таблица решений подзадач
CREATE TABLE SubTaskSolutions (
    ID SERIAL PRIMARY KEY,
    SubTaskID INT NOT NULL REFERENCES SubTasks(SubTaskID) ON DELETE CASCADE,
    FileName VARCHAR(255) NOT NULL,
    FilePath VARCHAR(500) NOT NULL,
    UploadDate TIMESTAMP DEFAULT NOW()
);

-- Таблица временных файлов подзадач
CREATE TABLE SubTaskTemp (
    ID SERIAL PRIMARY KEY,
    SubTaskID INT NOT NULL REFERENCES SubTasks(SubTaskID) ON DELETE CASCADE,
    StudentID INT NOT NULL,
    SolutionTempPath TEXT NULL,     -- путь к временным решениям
    FilesTempPaths TEXT NULL,       -- дополнительные файлы
    CreatedAt TIMESTAMP DEFAULT NOW()
);

-- таблица задач студентов
CREATE TABLE StudentTasks (
    StudentTaskID SERIAL PRIMARY KEY,                  -- автоинкрементный id
    StudentID BIGINT NOT NULL,                         -- id студента
    SubTaskID INT NOT NULL,                            -- id подзадачи
    StudentAnswer VARCHAR(32),                         -- ответ студента
    CompletionStatus VARCHAR(20) CHECK (CompletionStatus IN ('Не приступал', 'В процессе', 'Выполнено')), -- статус выполнения
    Score DECIMAL(5,2) NULL,                           -- баллы за подзадачу
    SolutionStudentPath VARCHAR(255),                  -- путь к решению студента
    StartDate TIMESTAMP NULL,                           -- дата начала выполнения
    ModifiedDate TIMESTAMP NULL,                        -- дата изменения
    CompletionDate TIMESTAMP NULL,                      -- дата получения правильного ответа
    DeadlineDate TIMESTAMP NULL,                        -- срок выполнения
    Attempts INT DEFAULT 0,                             -- количество попыток
    CONSTRAINT fk_student FOREIGN KEY (StudentID) REFERENCES Students(ID) ON DELETE CASCADE,
    CONSTRAINT fk_subtask FOREIGN KEY (SubTaskID) REFERENCES SubTasks(SubTaskID) ON DELETE CASCADE
);

-- таблица с логами(действий) студентов 
CREATE TABLE StudentActionLogs (
    LogID SERIAL PRIMARY KEY,                           -- автоинкрементный id
    StudentID INT,                                      -- id студента
    StudentLogin VARCHAR(50) NOT NULL,                 -- логин студента
    EventType VARCHAR(50) NOT NULL,                    -- тип действия: login_success, task_viewed, profile_updated
    Reason VARCHAR(100),                                -- причина
    DescriptionEvent VARCHAR(100),                     -- описание действия
    EventTime TIMESTAMP DEFAULT NOW(),                 -- время события
    IPAddress VARCHAR(45),                              -- IP адрес
    UserAgent TEXT,                                     -- User-Agent
    Metadata JSONB                                      -- специфичные поля в формате JSON
);
