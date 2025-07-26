from config import BASE_URL, login_admin, pass_admin, login_user, pass_user, token_admin, token #, client
from config import STUDENT_ID, STUDENT_TASK_ID
import pytest
import requests



def test_get_all_students_tasks_ok():
    url = f"{BASE_URL}/api/students_subtasks"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)

    assert response.status_code == 200, "❌ Ожидался статус 200"
    data = response.json()
    assert isinstance(data, list), "❌ Ответ должен быть списком задач"
    print(f"✅ Успешный ответ. Получено задач: {len(data)}")



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


@pytest.mark.parametrize("student_task_id, expected_status, description", [
    (STUDENT_TASK_ID, 200, "Существующая задача возвращается успешно"),
    (999999, 200, "Несуществующая задача — вернётся пустой список"),
    ("abc", 422, "Невалидный StudentTaskID — ошибка валидации"),
])
def test_get_student_task_by_id(student_task_id, expected_status, description):
    url = f"{BASE_URL}/api/students_subtasks/0/StudentTask/{student_task_id}"
    headers = {"Authorization": f"Bearer {token_admin}"}

    response = requests.get(url, headers=headers)
    assert response.status_code == expected_status, f"❌ {description}"

    if expected_status == 200:
        data = response.json()
        assert isinstance(data, list), "❌ Ожидался список задач"
        print(f"✅ {description}: получено задач — {len(data)}")
    else:
        print(f"⚠️ {description}: статус {response.status_code}")