from auth import _login
import requests
import pytest
BASE_URL = "https://info-run.ru/"
#BASE_URL = "http://localhost:9000/"

# актуальный пользователь
login_user = 'test'
pass_user = 'standart'
token = _login()

def run_task_test(subjectID, expected_status):
    token = _login()
    assert token, "❌ Невозможно получить токен, тест остановлен."

    headers = {"Authorization": f"Bearer {token}"}
    params = {"subjectID": subjectID}

    response = requests.get(f"{BASE_URL}/api/tasks", headers=headers, params=params)
    assert response.status_code == expected_status, \
        f"Ошибка: ожидался статус {expected_status}, получен {response.status_code}. Ответ: {response.text}"

@pytest.mark.parametrize("subjectID, expected_status, description", [
    (10, 200, "Получили категории с предметами"),
    (2, 200, "Получили пустой список с категориями"),
    (None, 200, "Получили категории по всем предметам"),
    ("aasd", 422, "Неправильный тип параметра")
])
def test_tasks(subjectID, expected_status, description):
    run_task_test(subjectID, expected_status)
    print(f"Тест с subjectID={subjectID} пройден: {description}")