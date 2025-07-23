from auth import _login
import requests
import pytest
#from fastapi.testclient import TestClient
#from Service.main import app
BASE_URL = "https://info-run.ru/"
#BASE_URL = "http://localhost:9000/"

# админ пользователь
login_admin = 'test'
pass_admin = 'standart'

login_user = 'ivan'
pass_user = 'standart'
# В test_get_logs надо менять id пользователй


# Заготовка токенов для теста (админ и обычный пользователь)
ADMIN_TOKEN =  _login() # замените на настоящий тестовый токен с правами admin_panel
USER_TOKEN = _login(login_user,pass_user)  # токен без прав admin_panel, например, для студента ID=2

#print("admin",ADMIN_TOKEN)
#print("user",USER_TOKEN)

@pytest.mark.parametrize("token, expected_status, description", [
    (ADMIN_TOKEN, 200, "Админ получает все логи"),
    (USER_TOKEN, 403, "Обычный пользователь не имеет доступа")
])
def test_get_all_logs(token, expected_status, description):
    url = f"{BASE_URL}/api/admin/students/logs"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)

    assert response.status_code == expected_status, f"Unexpected status: {description}"

    if expected_status == 200:
        data = response.json()
        assert isinstance(data, list), "Expected response to be a list of logs"
        # можно дополнительно проверить лимит по умолчанию:
        assert len(data) <= 50, "Default limit exceeded"

@pytest.mark.parametrize("requester_token, requested_student_id, expected_status", [
    (ADMIN_TOKEN, 1, 200),          # админ может смотреть логи любого пользователя
    (USER_TOKEN, 6, 200),           # пользователь смотрит свои логи — ок
    (USER_TOKEN, 3, 403),           # пользователь смотрит чужие логи — доступ запрещён
])
def test_get_logs(requester_token, requested_student_id, expected_status):
    url = f"{BASE_URL}/api/admin/students/{requested_student_id}/logs"
    headers = {"Authorization": f"Bearer {requester_token}"}
    response = requests.get(url, headers=headers)

    assert response.status_code == expected_status, f"Unexpected status for user token with studentID {requested_student_id}"
    if expected_status == 200:
        # Проверяем, что в ответе есть список (массив) логов
        data = response.json()
        assert isinstance(data, list), "Expected list of logs"