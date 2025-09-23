import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Pydantic v2 config
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).parent.parent / ".env"),
        case_sensitive=False,
        extra="ignore",
    )

    # -----------------------
    # Application
    # -----------------------
    APP_NAME: str = "infoRUN project"
    ENVIRONMENT: str = "production"
    DEBUG: bool = False
    SECRET_KEY: str = Field(..., min_length=16)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 300

    # -----------------------
    # Database
    # -----------------------
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    @property
    def DB_URL(self) -> str:
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 1800

    # -----------------------
    # Logging & Files
    # -----------------------
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "app.log"

    PROJECT_ROOT: Path = Field(default_factory=lambda: Path(__file__).resolve().parent.parent)
    UPLOADS_DIR: Path = Field(default_factory=lambda: Path(__file__).resolve().parent.parent / "Uploads")
    LOG_DIR: Path = Field(default_factory=lambda: Path(__file__).resolve().parent.parent / "logs")
    ARCHIVE_LOG_DIR: Path = Field(
        default_factory=lambda: Path(
            os.getenv("ARCHIVE_LOG_DIR") or Path(__file__).resolve().parent.parent / "logs/archive")
    )
    UPLOAD_IMAGE_DIR: Path
    UPLOAD_SOLUTION_DIR: Path
    UPLOAD_FILES_DIR: Path
    UPLOAD_STUDENTS_IMAGE_DIR: Path
    TEMPLATES_DIR: Path
    # Uploads
    def __init__(self, **values):
        super().__init__(**values)

        # Берем имена папок из env или используем дефолт
        self.LOG_DIR = self.PROJECT_ROOT / "logs"
        self.ARCHIVE_LOG_DIR = Path(os.getenv("ARCHIVE_LOG_DIR") or self.LOG_DIR / "archive")
        self.UPLOADS_DIR = self.PROJECT_ROOT / "Uploads"
        self.UPLOAD_IMAGE_DIR = self.UPLOADS_DIR / os.getenv("UPLOAD_IMAGE_DIR", "images")
        self.UPLOAD_SOLUTION_DIR = self.UPLOADS_DIR / os.getenv("UPLOAD_SOLUTION_DIR", "solutions")
        self.UPLOAD_FILES_DIR = self.UPLOADS_DIR / os.getenv("UPLOAD_FILES_DIR", "files")
        self.UPLOAD_STUDENTS_IMAGE_DIR = self.UPLOADS_DIR / os.getenv("UPLOAD_STUDENTS_IMAGE_DIR", "StudentSolutions")
        self.TEMPLATES_DIR = self.UPLOADS_DIR / os.getenv("TEMPLATES_DIR", "templates")


        # Создаем папки
        for folder in [ self.UPLOADS_DIR,
            self.UPLOAD_IMAGE_DIR,
            self.UPLOAD_SOLUTION_DIR,
            self.UPLOAD_FILES_DIR,
            self.UPLOAD_STUDENTS_IMAGE_DIR,
            self.TEMPLATES_DIR,
            self.LOG_DIR,
            self.ARCHIVE_LOG_DIR]:
            folder.mkdir(parents=True, exist_ok=True)


    # -----------------------
    # API & Timezone
    # -----------------------
    API_PREFIX: str = "/api/v1"
    TIMEZONE: str = "Europe/Moscow"

    # -----------------------
    # Метод для всех путей
    # -----------------------
    def full_paths(self) -> dict[str, Path]:
        return {
            "PROJECT_ROOT": self.PROJECT_ROOT,
            "LOG_DIR": self.LOG_DIR,
            "ARCHIVE_LOG_DIR": self.ARCHIVE_LOG_DIR,
            "UPLOADS_DIR": self.UPLOADS_DIR,
            "UPLOAD_IMAGE_DIR": self.UPLOAD_IMAGE_DIR,
            "UPLOAD_SOLUTION_DIR": self.UPLOAD_SOLUTION_DIR,
            "UPLOAD_FILES_DIR": self.UPLOAD_FILES_DIR,
            "UPLOAD_STUDENTS_IMAGE_DIR": self.UPLOAD_STUDENTS_IMAGE_DIR,
            "TEMPLATES_DIR": self.TEMPLATES_DIR,
        }

    # -----------------------
    # Создание директорий после инициализации
    # -----------------------
    def create_dirs(self):
        for folder in self.full_paths().values():
            folder.mkdir(parents=True, exist_ok=True)

# -----------------------
# Глобальный экземпляр
# -----------------------
settings = Settings()
# создаем все папки при старте
settings.create_dirs()