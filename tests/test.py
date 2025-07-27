from config_test import BASE_URL, login_admin, pass_admin, login_user, pass_user, token_admin, token
import requests
import pytest






# В test_get_logs надо менять id пользователй




@pytest.mark.parametrize("token, expected_status, description", [
    (token_admin, 200, "Админ получает все логи"),
    (token, 403, "Обычный пользователь не имеет доступа")
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
    (token_admin, 1, 200),          # админ может смотреть логи любого пользователя
    (token, 6, 200),           # пользователь смотрит свои логи — ок
    (token, 3, 403),           # пользователь смотрит чужие логи — доступ запрещён
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