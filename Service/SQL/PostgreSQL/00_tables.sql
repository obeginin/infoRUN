-- Создание баз данных
CREATE DATABASE inforun;
--CREATE DATABASE logdb;


-- Таблица с ролями
CREATE TABLE Roles (
    RoleID SERIAL PRIMARY KEY,       -- автоинкремент
    Name VARCHAR(50) NOT NULL UNIQUE
);

INSERT INTO Roles (Name) VALUES ('SuperAdmin'),('Администратор'), ('Учитель'), ('Ученик'), ('Родитель');


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
    ('view_solutions', 'Просмотр решений'),
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
VALUES ('obeginin', 'Бегинин', 'Олег', 'Вячеславович','lezhik.from@gmail.com', 'М',NULL,'Комментарий', '$pbkdf2-sha256$29000$3zunFMK4955zjpEyxngPYQ$nECQLRTK9OFP8I6QErp5iVHRy6D4j4/mC7IgkxDGTEY', 1,TRUE,NULL,TRUE),
('test1', 'Тестовый1', 'Тест1', 'Тестович1','test1@gmail.com', 'М',NULL,'тестовый админ', '$pbkdf2-sha256$29000$3zunFMK4955zjpEyxngPYQ$nECQLRTK9OFP8I6QErp5iVHRy6D4j4/mC7IgkxDGTEY', 1,TRUE,NULL,TRUE),
('test2', 'Тестовый2', 'Тест2', 'Тестович2','test2@gmail.com', 'М',NULL,'тестовый учитель', '$pbkdf2-sha256$29000$3zunFMK4955zjpEyxngPYQ$nECQLRTK9OFP8I6QErp5iVHRy6D4j4/mC7IgkxDGTEY', 2,TRUE,NULL,TRUE),
('test3', 'Тестовый3', 'Тест3', 'Тестович3','test3@gmail.com', 'М',NULL,'тестовый ученик', '$pbkdf2-sha256$29000$3zunFMK4955zjpEyxngPYQ$nECQLRTK9OFP8I6QErp5iVHRy6D4j4/mC7IgkxDGTEY', 3,TRUE,NULL,TRUE),
('test4', 'Тестовый4', 'Тест4', 'Тестович4','test4@gmail.com', 'М',NULL,'тестовый родитель', '$pbkdf2-sha256$29000$3zunFMK4955zjpEyxngPYQ$nECQLRTK9OFP8I6QErp5iVHRy6D4j4/mC7IgkxDGTEY', 4,TRUE,NULL,TRUE);
;

-- В данной таблице хранятся токены для сброса пароля пользователя
CREATE TABLE PasswordResetTokens (
    ID SERIAL PRIMARY KEY,                          -- автоинкрементный id токена
    StudentID BIGINT NOT NULL,                      -- id студента
    Token VARCHAR(255) NOT NULL UNIQUE,            -- сам токен
    ExpiresAt TIMESTAMP NOT NULL,                  -- срок действия токена
    Used BOOLEAN NOT NULL DEFAULT FALSE,           -- логическое поле: использован ли токен
    CreatedAt TIMESTAMP NOT NULL DEFAULT NOW(),    -- дата создания

    CONSTRAINT FK_PasswordResetTokens_Students FOREIGN KEY (StudentID)
        REFERENCES Students(ID)
        ON DELETE CASCADE
);

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
    TaskID SERIAL PRIMARY KEY,         -- автоинкрементный id категории
    SubjectID INT NOT NULL,            -- id предмета
    TaskNumber INT,    				   -- номер категории (надо переделать на подкатегорию или что то,
    TaskTitle VARCHAR(255),   		   -- описание категории
    CONSTRAINT fk_subject FOREIGN KEY (SubjectID) REFERENCES Subjects(ID) ON DELETE CASCADE
);

INSERT INTO Tasks (SubjectID, TaskTitle)
VALUES 
    ('ЕГЭ №1',10),('ЕГЭ №2',10),('ЕГЭ №3',10),('ЕГЭ №4',10),('ЕГЭ №5',10),('ЕГЭ №6',10),('ЕГЭ №7',10),('ЕГЭ №8',10),('ЕГЭ №9',10),('ЕГЭ №10',10),('ЕГЭ №11',10),('ЕГЭ №12',10),
    ('ЕГЭ №13',10),('ЕГЭ №14',10),('ЕГЭ №15',10),('ЕГЭ №16',10),('ЕГЭ №17',10),('ЕГЭ №18',10),('ЕГЭ №19',10),('ЕГЭ №20',10),('ЕГЭ №21',10),('ЕГЭ №22',10),('ЕГЭ №23',10),('ЕГЭ №24',10),
    ('ЕГЭ №25',10),('ЕГЭ №26',10),('ЕГЭ №27',10),
    ('ОГЭ №1',10),('ОГЭ №2',10),('ОГЭ №3',10),('ОГЭ №4',10),('ОГЭ №5',10),('ОГЭ №6',10),('ОГЭ №7',10),('ОГЭ №8',10),('ОГЭ №9',10),('ОГЭ №10',10),('ОГЭ №11',10),('ОГЭ №12',10),
    ('ОГЭ №13',10),('ОГЭ №14',10),('ОГЭ №15',10),('ОГЭ №16',10),
    ('Программирование',10)

-- Таблица с тегами (ЕГЭ, ОГЭ, СР, КР и т.д)
CREATE TABLE Tags (
    TagID SERIAL PRIMARY KEY,
    TagName VARCHAR(100) UNIQUE NOT NULL, -- например: ЕГЭ, ОГЭ, Самостоялка
    ShortName VARCHAR(7) UNIQUE NOT NULL,   -- краткое название (до 7 символов, для компактного отображения ЕГЭ, ОГЭ, СР, КР)
    TagType VARCHAR(50) NULL              -- необязательно: можно хранить тип (для заданий, для вариантов, универсальный)
);

INSERT INTO Tags (TagName, ShortName, TagType) VALUES
	('ЕГЭ', 'ЕГЭ', 'universal'),
	('ОГЭ', 'ОГЭ', 'universal'),
	('Самостоятельная работа', 'СР', 'universal'),
	('Контрольная работа', 'КР', 'universal'),
	('Короткий тест на тему', 'Тест', 'universal'),
	('Практические упражнения', 'Практика', 'universal');

-- Таблица с вариантами
CREATE TABLE Variants (
    VariantID SERIAL PRIMARY KEY,           -- автоинкрементный id
    VariantName VARCHAR(255),               -- человеко-понятное название
    SubjectID INT NOT NULL,            		-- id предмета
    TagID INT NULL,							-- id тега предмета
    Type VARCHAR(100),                      -- тип варианта (например, "Вариант", "Контрольная")
    Year VARCHAR(100),                      -- год варианта
    Number INT NULL,                        -- номер варианта, если применимо
    DifficultyLevel INT,                    -- уровень сложности
    Comment VARCHAR(100)                    -- комментарий
    CONSTRAINT fk_variants_subject FOREIGN KEY (SubjectID) REFERENCES Subjects(ID) ON DELETE CASCADE,
    CONSTRAINT fk_variants_tag FOREIGN KEY (TagID) REFERENCES Tags(TagID) ON DELETE SET NULL
);

INSERT INTO Variants (VariantName,SubjectID, TagID)
VALUES 
    ('Крылов Вариант №1',10,1),('Крылов Вариант №2',10,1),('Крылов Вариант №3',10,1),('Крылов Вариант №4',10,1),('Крылов Вариант №5',10,1),('Крылов Вариант №6',10,1),('Крылов Вариант №7',10,1),('Крылов Вариант №8',10,1),
    ('Крылов Вариант №9',10,1),('Крылов Вариант №10,1',10,1),('Крылов Вариант №11',10,1),('Крылов Вариант №12',10,1),('Крылов Вариант №13',10,1),('Крылов Вариант №14',10,1),('Крылов Вариант №5',10,1),('Крылов Вариант №16',10,1),
	('Крылов Вариант №17',10,1),('Крылов Вариант №18',10,1),('Крылов Вариант №19',10,1),('Крылов Вариант №20',10,1),
	('PRO100EGE Вариант №1',10,1),('PRO100EGE Вариант №2',10,1),('PRO100EGE Вариант №3',10,1),('PRO100EGE Вариант №4',10,1),('PRO100EGE Вариант №5',10,1),('PRO100EGE Вариант №6',10,1),('PRO100EGE Вариант №7',10,1),('PRO100EGE Вариант №8',10),
	('Апробация 14.05.2025',10,1),('Основной 2024 1 волна',10,1),('Основной 2024 2 волна',10,1),('Основной 2024 3 волна',10,1),('Основной 2024 4 волна',10,1),
	('Основной 2025 1 волна',10,1),('Основной 2025 2 волна',10,1),('Основной 2025 3 волна',10,1),('Основной 2025 4 волна',10,1),
	('Демоверсия 2025',10,1),('Демоверсия 2024',10,1),('Демоверсия 2023',10,1),
	('Кабанов',10,1,1),('Поляков',10,1),('РешуЕГЭ',10,1),('Статград 2025.05.12 №6 (База) Вар1',10,1), ('Статград 2025.05.12 №6 (База) Вар1',10,1),
	('Демоверсия 2025',10,2),('Демоверсия 2024',10,2),('Демоверсия 2023',10,2),;

-- Таблица подзадач
CREATE TABLE SubTasks (
    SubTaskID SERIAL PRIMARY KEY,                    -- автоинкрементный id
    TaskID INT NOT NULL,                             -- id категории
    SubTaskNumber INT,		                         -- номер подзадачи
    VariantID INT,                                   -- id варианта
    ImagePath VARCHAR(255),                          -- путь к изображению
    Description TEXT,                                -- описание задачи
    DifficultyLevel VARCHAR(10) CHECK (DifficultyLevel IN ('легко', 'норма', 'сложно', 'гроб')), -- уровень сложности
    SolutionPath VARCHAR(255),                       -- путь к решению
    CONSTRAINT fk_task FOREIGN KEY (TaskID) REFERENCES Tasks(TaskID) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_variant FOREIGN KEY (VariantID) REFERENCES Variants(VariantID) ON UPDATE CASCADE ON DELETE SET NULL
);

-- Таблица для связи многие ко многим тэгов с задачами
CREATE TABLE SubTaskTags (
    SubTaskID INT NOT NULL,
    TagID INT NOT NULL,
    PRIMARY KEY (SubTaskID, TagID),
    FOREIGN KEY (SubTaskID) REFERENCES SubTasks(SubTaskID) ON DELETE CASCADE,
    FOREIGN KEY (TagID) REFERENCES Tags(TagID) ON DELETE CASCADE
);

-- Таблица с ответами на задачи
CREATE TABLE SubTaskAnswers (
    AnswerID SERIAL PRIMARY KEY,
    SubTaskID INT NOT NULL,                  -- id задачи
    AnswerText TEXT NOT NULL,                -- правильный ответ (текст, число, вариант и т.д.)
    AnswerOrder INT DEFAULT 0,               -- порядок (для тестов с несколькими вариантами)
    AnswerType VARCHAR(20) DEFAULT 'text',   -- тип ответа: text, number, choice
    Score DECIMAL(5,2) DEFAULT 1.0,         -- баллы за этот ответ
    CONSTRAINT fk_subtask FOREIGN KEY (SubTaskID)
        REFERENCES SubTasks(SubTaskID)
        ON DELETE CASCADE
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




