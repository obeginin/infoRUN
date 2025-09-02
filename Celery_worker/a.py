#from Celery_worker.files import save_subtask_files_task
from utils.config import settings

#save_subtask_files_task.delay(1)
print(settings.UPLOADS_DIR)
print(settings.UPLOAD_IMAGE_DIR)  # путь к Uploads/images
print(settings.LOG_DIR)