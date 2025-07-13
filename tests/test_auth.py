import requests
#from fastapi.testclient import TestClient
#from Service.main import app
#BASE_URL = "https://info-run.ru/"
BASE_URL = "http://localhost:9000/"

# актуальный пользователь
login_user = 'ivan'
pass_user = 'standart'

'''Аутентификация'''
def test_successful_login():
    data = {"Login": login_user, "Password": pass_user}
    response = requests.post(f"{BASE_URL}/auth/login", json=data)
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_wrong_password():
    data = {"Login": login_user, "Password": "wrong"}
    response = requests.post(f"{BASE_URL}/auth/login", json=data)
    assert response.status_code == 401
    assert response.json()["detail"]["error"] == "PasswordFailed"

def test_wrong_username():
    data = {"Login": "ivann", "Password": pass_user}
    response = requests.post(f"{BASE_URL}/auth/login", json=data)
    assert response.status_code == 401
    assert response.json()["detail"]["error"] == "LoginNotFound"

def test_inactive_student():
    data = {"Login": "rustam", "Password": "standart"}
    response = requests.post(f"{BASE_URL}/auth/login", json=data)
    assert response.status_code == 403
    assert response.json()["detail"]["error"] == "StudentNoActive"


'''Выход'''
def test_logout():
    res = requests.post(f"{BASE_URL}/auth/login", json={"Login": login_user, "Password": pass_user})
    token = res.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(f"{BASE_URL}/auth/logout", headers=headers)

    assert res.status_code == 200
    assert res.json() == {"detail": "LOGOUT"}