import requests

#BASE_URL = "https://info-run.ru/"
BASE_URL = "http://localhost:9000/"


def login_success():
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "Login": "ivan",
        "Password": "standart"
    })
    print("✅ Успешный вход:", response.status_code, response.json())


def login_wrong_password():
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "Login": "ivan",
        "Password": "wrongpass"
    })
    print("❌ Неверный пароль:", response.status_code, response.json())


def login_wrong_username():
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "Login": "nosuchuser",
        "Password": "standart"
    })
    print("❌ Неверный логин:", response.status_code, response.json())


def login_inactive_user():
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "Login": "rustam",
        "Password": "standart"
    })
    print("⛔ Неактивный пользователь:", response.status_code, response.json())

if __name__ == "__main__":
    login_success()
    login_wrong_password()
    login_wrong_username()
    login_inactive_user()