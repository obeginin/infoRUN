from config_test import BASE_URL, login_admin, pass_admin, login_user, pass_user, token_admin, token
import requests
import pytest





'''Аутентификация'''
def test_successful_login():
    data = {"Login": login_user, "Password": pass_user}
    response = requests.post(f"{BASE_URL}/api/auth/login", json=data)
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_wrong_password():
    data = {"Login": login_user, "Password": "wrong"}
    response = requests.post(f"{BASE_URL}/api/auth/login", json=data)
    assert response.status_code == 401
    assert response.json()["detail"]["error"] == "PasswordFailed"

def test_wrong_username():
    data = {"Login": "ivann", "Password": pass_user}
    response = requests.post(f"{BASE_URL}/api/auth/login", json=data)
    assert response.status_code == 401
    assert response.json()["detail"]["error"] == "LoginNotFound"

def test_inactive_student():
    data = {"Login": "rustam", "Password": "standart"}
    response = requests.post(f"{BASE_URL}/api/auth/login", json=data)
    assert response.status_code == 403
    assert response.json()["detail"]["error"] == "StudentNoActive"


'''Выход'''
def test_logout():
    res = requests.post(f"{BASE_URL}/api/auth/login", json={"Login": login_user, "Password": pass_user})
    token = res.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(f"{BASE_URL}/api/auth/logout", headers=headers)

    assert res.status_code == 200
    assert res.json() == {"detail": "LOGOUT"}


'''роли'''
@pytest.mark.parametrize("expected_status, description", [
    (200, "Успешное получение списка всех ролей"),
])
def test_read_all_roles(expected_status, description):
    url = f"{BASE_URL}/api/admin/roles"
    response = requests.get(url, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == expected_status, f"Failed: {description}"
    data = response.json()
    assert isinstance(data, list), "Ответ должен быть списком"
    assert len(data) > 0, "Список ролей не должен быть пустым"
    first = data[0]
    assert "RoleID" in first and "Name" in first, "Роль должна содержать поля RoleID и Name"
    #print(f"✅ {description} - всего ролей: {len(data)}")


'''разрешения роли'''
@pytest.mark.parametrize("role_id, expected_status, description", [
    (2, 200, "Существующая роль"),
    (9999, 404, "Несуществующая роль"),
    ("abc", 422, "Невалидный role_id"),
])
def test_read_permissions_role(role_id, expected_status, description):
    url = f"{BASE_URL}/api/admin/roles/{role_id}"
    response = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == expected_status, f"Failed: {description}"
    if expected_status == 200:
        data = response.json()
        assert "permissions" in data, "Нет поля permissions в ответе"
        assert isinstance(data["permissions"], list), "permissions должно быть списком"
        assert len(data["permissions"]) > 0, "permissions не должен быть пустым"
        #print(f"✅ {description} - статус {response.status_code}, разрешения: {data['permissions']}")
    else:
        print(f"✅ {description} - статус {response.status_code}")


'''разрешения'''
@pytest.mark.parametrize("expected_status, description", [
    (200, "Успешное получение списка всех разрешения"),
])
def test_read_all_permissions(expected_status, description):
    url = f"{BASE_URL}/api/admin/permission"
    response = requests.get(url, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == expected_status, f"Failed: {description}"
    data = response.json()
    assert isinstance(data, list), "Ответ должен быть списком"
    assert len(data) > 0, "Список разрешений не должен быть пустым"
    first = data[0]
    assert "PermissionID" in first and "Name" in first, "Разрешение должно содержать поля PermissionID и Name"
    #print(f"✅ {description} - всего разрешений: {len(data)}")


@pytest.mark.parametrize("student_id, role_id, expected_status, description", [
    (4, 1, 200, "Успешное назначение роли студенту"),
    (9999, 2, 404, "Несуществующий студент"),
    (4, 9999, 404, "Несуществующая роль"),
    ("abc", 2, 422, "Некорректный studentID (строка вместо числа)"),
])
def test_assign_role_to_student(student_id, role_id, expected_status, description):
    url = f"{BASE_URL}/api/admin/students/{student_id}/assign-role?RoleID={role_id}"
    response = requests.post(url, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == expected_status, f"❌ Failed: {description}"
    print(f"✅ {description} — статус {response.status_code}")

    if expected_status == 200:
        data = response.json()
        assert "message" in data
        assert "успешно назначена роль" in data["message"]

'''список студентов'''
def test_read_all_students():
    url = f"{BASE_URL}/api/admin/students"
    response = requests.get(url, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200, "Не удалось получить список студентов"
    data = response.json()

    # Проверка, что получен список
    assert isinstance(data, list), "Ответ должен быть списком студентов"
    assert len(data) > 0, "Список студентов не должен быть пустым"

    # Проверка структуры первой записи
    student = data[0]
    expected_fields = ["ID", "Login", "First_Name", "Last_Name", "Email", "RoleName", "permissions"]
    for field in expected_fields:
        assert field in student, f"Поле {field} отсутствует в объекте студента"

    print(f"✅ Успешно получен список студентов. Всего студентов: {len(data)}")


@pytest.mark.parametrize("role_id, permission_ids, expected_status, description", [
    (3, [1, 2], 200, "Назначение новых разрешений существующей роли"),
    (3, [], 200, "Очистка всех разрешений у существующей роли"),
    (9999, [1], 404, "Роль не найдена"),
    (3, [9999], 500, "Ошибка при назначении несуществующего разрешения"),
])
def test_assign_permissions_to_role(role_id, permission_ids, expected_status, description):
    url = f"{BASE_URL}/api/admin/roles/{role_id}/assign-permission"
    payload = {"permission_ids": permission_ids}
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.post(url, json=payload, headers=headers)

    assert response.status_code == expected_status, f"❌ {description} (ожидали {expected_status}, получили {response.status_code})"

    if expected_status == 200:
        json = response.json()
        assert "message" in json
        assert isinstance(json.get("added", []), list)
        assert isinstance(json.get("removed", []), list)

    #print(f"✅ {description} — статус {response.status_code}")