from auth import _login
import requests
import pytest
BASE_URL = "https://info-run.ru/"
#BASE_URL = "http://localhost:9000/"

# актуальный пользователь
login_user = 'test'
pass_user = 'standart'
token = _login()


"""Категории"""
def run_task_test(subjectID, expected_status):
    token = _login()
    assert token, "❌ Невозможно получить токен, тест остановлен."
    headers = {"Authorization": f"Bearer {token}"}
    params = {"subjectID": subjectID}
    response = requests.get(f"{BASE_URL}/api/tasks", headers=headers, params=params)
    assert response.status_code == expected_status, \
        f"Ошибка: ожидался статус {expected_status}, получен {response.status_code}. Ответ: {response.text}"

# 4 теста
@pytest.mark.parametrize("subjectID, expected_status, description", [
    (10, 200, "Получили категории с предметами"),
    (2, 200, "Получили пустой список с категориями"),
    (None, 200, "Получили категории по всем предметам"),
    ("aasd", 422, "Неправильный тип параметра")
])
def test_tasks(subjectID, expected_status, description):
    run_task_test(subjectID, expected_status)
    print(f"Тест с subjectID={subjectID} пройден: {description}")



"""Предметы"""
def run_subjects_test(expected_status):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/subjects", headers=headers)
    assert response.status_code == expected_status, \
        f"Ошибка: ожидался статус {expected_status}, получен {response.status_code}. Ответ: {response.text}"
    return response

# 1 тест
@pytest.mark.parametrize("expected_status, description", [
    (200, "Получили список всех предметов"),
])
def test_get_subjects(expected_status, description):
    response = run_subjects_test(expected_status)
    print(f"✅ Тест GET /api/subjects пройден: {description}")
    print("Ответ:", response.text)



"""Предмет по id"""
def run_subject_by_id_test(subject_id, expected_status):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/subjects/{subject_id}", headers=headers)
    assert response.status_code == expected_status, \
        f"Ошибка: ожидался статус {expected_status}, получен {response.status_code}. Ответ: {response.text}"
    return response

# 3 теста
@pytest.mark.parametrize("subject_id, expected_status, description", [
    (1, 200, "Существующий предмет найден"),
    (9999, 404, "Несуществующий предмет вызывает ошибку 404"),
    ("abc", 422, "Невалидный subjectID — строка вместо числа"),
])
def test_get_subject_by_id(subject_id, expected_status, description):
    response = run_subject_by_id_test(subject_id,expected_status)
    print(f"✅ Тест GET /api/subjects/{subject_id} пройден: {description}")
    print("Ответ:", response.text)