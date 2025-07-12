import requests
from time import time, sleep
from dotenv import load_dotenv
import jwt
from datetime import datetime, timedelta, timezone
import os
load_dotenv()

BASE_URL = "https://info-run.ru/"
#BASE_URL = "http://localhost:9000/"




def login_wrong_password():
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "Login": "ivan",
        "Password": "wrongpass"
    })
    try:
        data = response.json()
        print(data)
    except Exception as e:
        print("❌ Ошибка при разборе JSON-ответа:", e)
        print("Ответ:", response.text)
        return
    data.get("detail", {}).get("error")
    if response.status_code == 401 and data.get("detail", {}).get("error") == "PasswordFailed":
        print("Тест №1 пройден. ✅ ❌ Неверный пароль:", response.status_code, data)
    else:
        print("❌ Тест №1 не пройден. Ожидался отказ из-за неверного пароля:", response.status_code, data)


def login_wrong_username():
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "Login": "nosuchuser",
        "Password": "standart"
    })

    try:
        data = response.json()
    except Exception as e:
        print("❌ Ошибка при разборе JSON-ответа:", e)
        print("Ответ:", response.text)
        return

    if response.status_code == 401 and data.get("detail", {}).get("error") == "LoginNotFound":
        print("Тест №2 пройден. ✅ ❌ Неверный логин:", response.status_code, data)
    else:
        print("❌ Тест №2 не пройден. Ожидался отказ из-за неверного логина:", response.status_code, data)


def login_inactive_user():
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "Login": "rustam",
        "Password": "standart"
    })
    try:
        data = response.json()
    except Exception as e:
        print("❌ Ошибка при разборе JSON-ответа:", e)
        print("Ответ:", response.text)
        return

    if response.status_code == 403 and data.get("detail", {}).get("error") == "StudentNoActive":
        print("Тест №3 пройден. ✅ ⛔ Неактивный пользователь:", response.status_code, data)
    else:
        print("❌ Тест №3 не пройден. Ожидался отказ из-за неактивности:", response.status_code, data)

def login_success():
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "Login": "ivan",
        "Password": "standart"
    })
    try:
        data = response.json()
    except Exception as e:
        print("❌ Ошибка при разборе JSON-ответа:", e)
        print("Ответ:", response.text)
        return None

    if response.status_code == 200 and "access_token" in data:
        print("Тест №4 пройден. ✅ ✅ Успешный вход:", data)
        return data["access_token"]
    else:
        print(f"❌ Тест №4 не пройден. Код: {response.status_code}, Ответ:", data)
        return None

'''Проверка Токена'''
def check_token():
    token = login_success()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(f"{BASE_URL}/auth/check-token", headers=headers)
    try:
        data = response.json()
    except Exception as e:
        print("❌ Ошибка при разборе JSON-ответа:", e)
        print("Ответ:", response.text)
        return

    if response.status_code == 200:
        print("Тест №5 пройден. ✅ ✅ Получили студента по токену:", response.status_code, data)
    else:
        print("Тест №5 Ошибка!!!. ❌  Код: {response.status_code}, Ответ:", data)

'''Проверка Токена'''
def invalid_token():
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUretzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJpdmFuIiwiZXhwIjoxNzUyNTU0NjEzfQ._bkf8eUrMYAkPcYFsvOt3WjXVsjq22jwKHnmlVM9nUM"
    }
    response = requests.get(f"{BASE_URL}/auth/check-token", headers=headers)
    try:
        data = response.json()
        if response.status_code == 401 and data["detail"]["error"] == "TokenInvalid":
            print("Тест №6 Пройден. ✅ ❌ Недействительный Токен:", response.status_code, response.json())
        else:
            print("Тест №6 Ошибка!!!. ❌  Недействительный Токен:", response.status_code)
    except Exception as e:
        print("❌ Тест №6. Не удалось обработать ответ:", e)
        print("🔁 Ответ сервера:", response.text)

def invalid_schema_token():
    token = login_success()
    headers = {
        "Authorization": f"Token {token}"
    }
    response = requests.get(f"{BASE_URL}/auth/check-token", headers=headers)
    try:
        data = response.json()
        if response.status_code == 401 and data["detail"]["error"] == "TokenMalformed":
            print("Тест №7 Пройден. ✅ ❌ Неправильная схема Токена:", response.status_code, response.json())
        else:
            print("Тест №7 Ошибка!!!. ❌  Неправильная схема Токена:", response.status_code)
    except Exception as e:
        print("❌ Тест №7. Не удалось обработать ответ:", e)
        print("🔁 Ответ сервера:", response.text)


# функция создания левого токена
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
def create_error_token(login: str):
    payload = {
        "sub": login,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=10)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def student_not_found():
    # Токен с корректным payload, но с несуществующим логином "nosuchuser"
    fake_token = create_error_token("nosuchuser")
    #print(fake_token)

    headers = {
        "Authorization": f"Bearer {fake_token}"
    }
    response = requests.get(f"{BASE_URL}/auth/check-token", headers=headers)

    try:
        data = response.json()
        if response.status_code == 401 and data.get("detail", {}).get("error") == "StudentNotFound":
            print("Тест №8 Пройден. ✅ ❌: Извлеченный из токена логин не найден в бд", response.status_code, data)
        else:
            print("Тест №8 Ошибка!!! ❌: Извлеченный из токена логин не найден в бд", response.status_code, data)
    except Exception as e:
        print("Ошибка при разборе ответа:", e)
        print("Ответ сервера:", response.text)


def token_without_sub():
    # Генерируем токен без поля "sub"
    payload = {
        "exp": int(time()) + 60,  # срок действия токена 1 минута
        # "sub" отсутствует специально
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(f"{BASE_URL}/auth/check-token", headers=headers)

    try:
        data = response.json()
        if response.status_code == 401 and data.get("detail", {}).get("error") == "TokenInvalidPayload":
            print("Тест №9 Пройден. ✅ ❌: Токен без 'sub'", response.status_code, data)
        else:
            print("Тест №9. Ошибка!!!❌: Токен без 'sub' ", response.status_code, data)
    except Exception as e:
        print("Ошибка при обработке ответа:", e)
        print("Ответ сервера:", response.text)

# функция для генерации JWT-токен с временем жизни 5 секунд
def generate_short_lived_token(login: str) -> str:
    payload = {
        "sub": login,
        "exp": datetime.now(timezone.utc) + timedelta(seconds=5)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def expired_Token():
    token = generate_short_lived_token("ivan")
    print("Ждем 6 секунд, чтобы токен истек")
    headers = {
        "Authorization": f"Bearer {token}"
    }
    sleep(6)
    response = requests.get(f"{BASE_URL}/auth/check-token", headers=headers)
    try:
        data = response.json()
        if response.status_code == 401 and data.get("detail", {}).get("error") == "TokenExpired":
            print("Тест №10 Пройден. ✅ ❌ Срок действия токена истёк ", response.status_code, data)
        else:
            print("Тест №10. Ошибка!!! ❌ Срок действия токена истёк.  Ответ сервера:", response.status_code, data)
    except Exception as e:
        print("Ошибка при разборе ответа:", e)
        print("Ответ сервера:", response.text)

if __name__ == "__main__":
    strat_time = time()
    login_wrong_password()
    login_wrong_username()
    login_inactive_user()
    check_token()
    invalid_token()
    invalid_schema_token()
    student_not_found()
    token_without_sub()
    expired_Token()
    end_time = time()
    print(f"Время выполнения запросов: {end_time-strat_time}")