from config_test import BASE_URL, login_admin, pass_admin, login_user, pass_user, token_admin, token, STUDENT_ID #, client

import pytest
import requests
import httpx
from uuid import uuid4

STUDENT_ID = 2
STUDENT_TASK_ID = 43
SUBTASK_ID = 10
TASK_ID = 8
SUBJECT_ID = 10
VARIANT_ID = 5
COMPLETION_STATUS = 'Не приступал'
SEARCH = 'Крылов'
SORT_COLUMN1= 'DeadlineDate'
SORT_DIRECTION1= 'DESC'
SORT_COLUMN2 = 'Attempts'
SORT_DIRECTION2 = 'ASC'
LIMIT = 5000
OFFSET = 10


@pytest.mark.asyncio
async def test_add_new_student_success():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        headers = {"Authorization": f"Bearer {token_admin}"}
        unique_login = f"test_student_{uuid4().hex[:8]}"
        payload = {
            "Login": unique_login,
            "Email": f"{unique_login}@example.com",
            "Password": "Secret123!",
            "Last_Name": "Иванов",
            "First_Name": "Иван",
            "Middle_Name": "Иванович",
            "Sex": "М",
            "BirthDate": "2000-01-01",
            "Comment": "Тестовый пользователь",
            "RoleID": 3,  # Укажи актуальный ID роли
            "IsActive": True
        }

        response = await client.post("/api/students/new_student", headers=headers, json=payload)

        assert response.status_code == 200, f"❌ Ошибка при добавлении студента: {response.text}"
        assert response.json()["message"] == "Студент успешно добавлен"
        print("✅ Новый студент успешно добавлен")



'''Проверка роута без фильтров'''
def test_get_all_students_tasks_ok():
    url = f"{BASE_URL}/api/students_subtasks"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)

    assert response.status_code == 200, "❌ Ожидался статус 200"
    data = response.json()
    assert isinstance(data, list), "❌ Ответ должен быть списком задач"
    print(f"✅ Успешный ответ. Получено задач: {len(data)}")


'''Проверка роута без фильтров, но с path параметром student_id'''
@pytest.mark.parametrize("student_id, expected_status, description", [
    (STUDENT_ID, 200, "Существующий студент получает задачи"),
    (999999, 200, "Несуществующий студент — пустой список (или обработка)"),
    ("abc", 422, "Невалидный ID студента"),
])
def test_get_tasks_by_student(student_id, expected_status, description):
    url = f"{BASE_URL}/api/students_subtasks/{student_id}"
    headers = {"Authorization": f"Bearer {token_admin}"}

    response = requests.get(url, headers=headers)
    assert response.status_code == expected_status, f"❌ {description}"

    if expected_status == 200:
        data = response.json()
        assert isinstance(data, list), "Ожидался список задач"
        print(f"✅ {description}: получено {len(data)} задач")
    else:
        print(f"⚠️ {description}: статус {response.status_code}")

'''Проверка фильтров'''
def run_student_tasks_query_test(student_id, query_params, expected_status, description):
    url = f"{BASE_URL}/api/students_subtasks/{student_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers, params=query_params)
    print("👉 DEBUG PARAMS:", query_params)
    assert response.status_code == expected_status, f"❌ {description}"

    if expected_status == 200:
        data = response.json()
        assert isinstance(data, list), "❌ Ожидался список задач"
        assert len(data) > 0, f"❌ {description}: получен пустой список"
        print(f"✅ {description}: получено задач — {len(data)}")
    else:
        print(f"⚠️ {description}: статус {response.status_code}")

@pytest.mark.parametrize("query_params, expected_status, description", [
    ({"student_task_id": STUDENT_TASK_ID}, 200, "Фильтрация по StudentTaskID"),
    ({"sub_task_id": SUBTASK_ID}, 200, "Фильтрация по SubTaskID"),
    ({"task_id": TASK_ID}, 200, "Фильтрация по TaskID"),
    ({"subject_id": SUBJECT_ID}, 200, "Фильтрация по SubjectID"),
    ({"variant_id": VARIANT_ID}, 200, "Фильтрация по VariantID"),
    ({"completion_status": COMPLETION_STATUS}, 200, "Фильтрация по CompletionStatus"),
    ({"search": SEARCH}, 200, "Поиск по ключевому слову"),
    ({"sort_column1": SORT_COLUMN1}, 200, "Сортировка по первому столбцу"),
    ({"sort_column2": SORT_COLUMN2}, 200, "Сортировка по второму столбцу"),
    ({"sort_direction1": SORT_DIRECTION1}, 200, "Сортировка по убыванию (1 уровень)"),
    ({"sort_direction2": SORT_DIRECTION2}, 200, "Сортировка по возрастанию (2 уровень)"),
    ({"limit": 5000}, 200, "Ограничение количества строк"),
    ({"offset": OFFSET}, 200, "Пропуск N строк"),
])
def test_query_params_on_student_tasks(query_params, expected_status, description):
    run_student_tasks_query_test(STUDENT_ID, query_params, expected_status, description)


@pytest.mark.parametrize("student_task_id, expected_status, description", [
    (STUDENT_TASK_ID, 200, "Существующая задача возвращается успешно"),
    (999999, 200, "Несуществующая задача — вернётся пустой список"),
    ("abc", 422, "Невалидный StudentTaskID — ошибка валидации"),
])
def test_get_student_task_by_id(student_task_id, expected_status, description):
    url = f"{BASE_URL}/api/students_subtasks/2/StudentTask/{student_task_id}"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)
    assert response.status_code == expected_status, f"❌ {description}"

    if expected_status == 200:
        data = response.json()
        assert isinstance(data, list), "❌ Ожидался список задач"
        print(f"✅ {description}: получено задач — {len(data)}")
    else:
        print(f"⚠️ {description}: статус {response.status_code}")