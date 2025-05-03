from sqlalchemy.orm import Session
from sqlalchemy import text
from Schemas.tasks import SubTaskCreate

''' функция-SQL запрос к БД для вывода всех задач'''
def get_all_tasks(db: Session):
    query = text("SELECT TaskID, TaskNumber, TaskTitle FROM Tasks ORDER BY TaskNumber")
    result = db.execute(query).fetchall()
    #print(result) # выводит результат запроса в консоль
    return [{"TaskID": row.TaskID, "TaskNumber": row.TaskNumber, "TaskTitle": row.TaskTitle} for row in result]

''' функция-SQL запрос к БД для вывода задачи по id'''
def get_task_id(db: Session, task_id: int):
    query = text(f"SELECT TaskID, TaskNumber, TaskTitle FROM Tasks where TaskID={task_id}")
    result = db.execute(query).fetchall()
    return result

''' Вывод всех заголовков столбцов таблицы SubTasks'''
def get_columns_of_table(db: Session, table_name: str = 'SubTasks'):
    query = text(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = :table_name")
    result = db.execute(query, {"table_name": table_name}).fetchall()
    return [row.COLUMN_NAME for row in result]

''' функция-SQL запрос к БД для вывода всех подзадач'''
def get_all_subtasks(db: Session):
    query = text("SELECT SubTaskID, TaskID, SubTaskNumber, ImagePath, Description, Answer, SolutionPath FROM SubTasks ORDER BY SubTaskNumber")
    result = db.execute(query).fetchall()
    subtasks = [
        {"SubTaskID": row.SubTaskID,
        "TaskID": row.TaskID,
         "SubTaskNumber": row.SubTaskNumber,
         "ImagePath": row.ImagePath,
         "Description": row.Description,
         "Answer": row.Answer,
         "SolutionPath": row.SolutionPath}
        for row in result]
    return subtasks

''' функция-SQL для вывода подзадачи по id'''
def get_subtasks_id(db: Session, task_id: int):
    query = text(f"SELECT * FROM SubTasks where SubTaskID={task_id}")
    result = db.execute(query).fetchall()
    subtasks = [
        {"SubTaskID": row.SubTaskID,
        "TaskID": row.TaskID,
         "SubTaskNumber": row.SubTaskNumber,
         "ImagePath": row.ImagePath,
         "Description": row.Description,
         "Answer": row.Answer,
         "SolutionPath": row.SolutionPath}
        for row in result]
    return subtasks

''' функция-SQL для вывода подзадач по типу номеру ЕГЭ'''
def get_subtasks_TaskID(db: Session, task_id: int):
    query = text(f"SELECT * FROM SubTasks where TaskID={task_id} ORDER BY SubTaskNumber")
    result = db.execute(query).fetchall()
    subtasks = [
        {"SubTaskID": row.SubTaskID,
        "TaskID": row.TaskID,
         "SubTaskNumber": row.SubTaskNumber,
         "ImagePath": row.ImagePath,
         "Description": row.Description,
         "Answer": row.Answer,
         "SolutionPath": row.SolutionPath}
        for row in result]
    return subtasks

''' Добавление новой подзадачи '''
def create_subtask(db: Session, subtask_data: SubTaskCreate):
    query = text("""
        INSERT INTO SubTasks (TaskID, SubTaskNumber, ImagePath, Description, Answer, SolutionPath)
        OUTPUT INSERTED.SubTaskID
        VALUES (:TaskID, :SubTaskNumber, :ImagePath, :Description, :Answer, :SolutionPath)
    """)
    result = db.execute(query, {
        "TaskID": subtask_data.TaskID,
        "SubTaskNumber": subtask_data.SubTaskNumber,
        "ImagePath": subtask_data.ImagePath,
        "Description": subtask_data.Description,
        "Answer": subtask_data.Answer,
        "SolutionPath": subtask_data.SolutionPath,
    })

    new_id = result.scalar() # возвращаем id добавленной задачи
    return {"SubTaskID": new_id}


'''def get_all_tasks(db: Session):
    return db.query(Task).order_by(Task.TaskNumber).all()'''