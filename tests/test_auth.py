import requests

#BASE_URL = "https://info-run.ru/"
BASE_URL = "http://{BASE_URL}/"

'''Аутентификация'''
def test_successful_login():
    data = {"Login": "ivan", "Password": "standart"}
    response = requests.post(f"{BASE_URL}/auth/login", json=data)
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_wrong_password():
    data = {"Login": "ivan", "Password": "wrong"}
    response = requests.post(f"{BASE_URL}/auth/login", json=data)
    assert response.status_code == 400
    assert response.json()["detail"]["error"] == "PasswordFailed"

def test_wrong_username():
    data = {"Login": "ivann", "Password": "standart"}
    response = requests.post(f"{BASE_URL}/auth/login", json=data)
    assert response.status_code == 400
    assert response.json()["detail"]["error"] == "LoginNotFound"

def test_inactive_student():
    data = {"Login": "rustam", "Password": "standart"}
    response = requests.post(f"{BASE_URL}/auth/login", json=data)
    assert response.status_code == 400
    assert response.json()["detail"]["error"] == "StudentNoActive"