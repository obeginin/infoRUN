import requests
from time import time, sleep
from dotenv import load_dotenv
import jwt
from datetime import datetime, timedelta, timezone
import os
load_dotenv()

BASE_URL = "https://info-run.ru/"
#BASE_URL = "http://localhost:9000/"

# актуальный пользователь
login_user = 'test'
pass_user = 'standart'
new_pass_user = 'standart_password'

def _login():
    response = requests.post(f"{BASE_URL}/api/auth/login", json={
        "Login": login_user,
        "Password": pass_user
    })
    try:
        data = response.json()
    except Exception as e:
        print("Ошибка при декодировании JSON:", e)
        print("Тело ответа:", response.text)
        raise
    #print("Ответ сервера:", data)
    if 'access_token' not in data:
        print(f"[Ошибка] Логин не удался. Статус: {response.status_code}")
        #print("Ответ:", data)
        raise KeyError("'access_token' отсутствует в ответе")

    return data["access_token"]

def login_wrong_password():
    response = requests.post(f"{BASE_URL}/api/auth/login", json={
        "Login": login_user,
        "Password": "wrongpass"
    })
    try:
        data = response.json()
        #print(data)
    except Exception as e:
        print("❌ Ошибка при разборе JSON-ответа:", e)
        print("Ответ:", response.text)
        return
    data.get("detail", {}).get("error")
    if response.status_code == 401 and data.get("detail", {}).get("error") == "PasswordFailed":
        print("Тест №1 пройден. ✅ ⛔ Неверный пароль:", response.status_code, data)
    else:
        print("❌ Тест №1 не пройден. Ожидался отказ из-за неверного пароля:", response.status_code, data)


def login_wrong_username():
    response = requests.post(f"{BASE_URL}/api/auth/login", json={
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
        print("Тест №2 пройден. ✅ ⛔ Неверный логин:", response.status_code, data)
    else:
        print("❌ Тест №2 не пройден. Ожидался отказ из-за неверного логина:", response.status_code, data)


def login_inactive_user():
    response = requests.post(f"{BASE_URL}/api/auth/login", json={
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
    response = requests.post(f"{BASE_URL}/api/auth/login", json={
        "Login": login_user,
        "Password": pass_user
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
    token = _login()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(f"{BASE_URL}/api/auth/check-token", headers=headers)
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
    response = requests.get(f"{BASE_URL}/api/auth/check-token", headers=headers)
    try:
        data = response.json()
        if response.status_code == 401 and data["detail"]["error"] == "TokenInvalid":
            print("Тест №6 Пройден. ✅ ⛔ Недействительный Токен:", response.status_code, response.json())
        else:
            print("Тест №6 Ошибка!!!. ❌  Недействительный Токен:", response.status_code)
    except Exception as e:
        print("❌ Тест №6. Не удалось обработать ответ:", e)
        print("🔁 Ответ сервера:", response.text)

def invalid_schema_token():
    token = _login()
    headers = {
        "Authorization": f"Token {token}"
    }
    response = requests.get(f"{BASE_URL}/api/auth/check-token", headers=headers)
    try:
        data = response.json()
        if response.status_code == 401 and data["detail"]["error"] == "TokenMalformed":
            print("Тест №7 Пройден. ✅ ⛔ Неправильная схема Токена:", response.status_code, response.json())
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
    response = requests.get(f"{BASE_URL}/api/auth/check-token", headers=headers)

    try:
        data = response.json()
        if response.status_code == 401 and data.get("detail", {}).get("error") == "StudentNotFound":
            print("Тест №8 Пройден. ✅ ⛔: Извлеченный из токена логин не найден в бд", response.status_code, data)
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
    response = requests.get(f"{BASE_URL}/api/auth/check-token", headers=headers)

    try:
        data = response.json()
        if response.status_code == 401 and data.get("detail", {}).get("error") == "TokenInvalidPayload":
            print("Тест №9 Пройден. ✅ ⛔: Токен без 'sub'", response.status_code, data)
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
    response = requests.get(f"{BASE_URL}/api/auth/check-token", headers=headers)
    try:
        data = response.json()
        if response.status_code == 401 and data.get("detail", {}).get("error") == "TokenExpired":
            print("Тест №10 Пройден. ✅ ⛔ Срок действия токена истёк ", response.status_code, data)
        else:
            print("Тест №10. Ошибка!!! ❌ Срок действия токена истёк.  Ответ сервера:", response.status_code, data)
    except Exception as e:
        print("Ошибка при разборе ответа:", e)
        print("Ответ сервера:", response.text)


def student_change_password_wrong_old():
    token = _login()  # Получаем токен авторизации
    headers = {
        "Authorization": f"Bearer {token}"
    }
    json = {
        "old_password": "неверный_пароль",  # ❌ неправильный текущий
        "new_password": "standart",
        "repeat_new_password": "standart"
    }
    response = requests.post(f"{BASE_URL}/api/auth/change-password", headers=headers, json=json)

    try:
        data = response.json()
        if response.status_code == 400 and data.get("detail", {}).get("error") == "OldPasswordIncorrect":
            print("Тест №11 Пройден. ✅ ⛔ Неверный старый пароль:", response.status_code, data)
        else:
            print("Тест №11 Ошибка!!! ❌ Неверный старый пароль:", response.status_code, data)
    except Exception as e:
        print("Ошибка при разборе ответа:", e)
        print("Ответ сервера:", response.text)

def student_change_password_mismatch():
    token = _login()  # Получаем токен авторизации
    headers = {
        "Authorization": f"Bearer {token}"
    }
    json = {
        "old_password": pass_user,   # ✅ правильный старый
        "new_password": "newpassword123",
        "repeat_new_password": "newpassword321"  # ❌ не совпадает
    }
    response = requests.post(f"{BASE_URL}/api/auth/change-password", headers=headers, json=json)

    try:
        data = response.json()
        if response.status_code == 400 and data.get("detail", {}).get("error") == "NewPasswordsMismatch":
            print("Тест №12 Пройден. ✅ ⛔ Новые пароли не совпадают:", response.status_code, data)
        else:
            print("Тест №12 Ошибка!!! ❌ Новые пароли не совпадают:", response.status_code, data)
    except Exception as e:
        print("Ошибка при разборе ответа:", e)
        print("Ответ сервера:", response.text)

def student_change_password():
    token = _login()

    headers = {
        "Authorization": f"Bearer {token}"
    }
    json_t = {
        "old_password": pass_user,
        "new_password": new_pass_user,
        "repeat_new_password": new_pass_user
    }
    json_orig = {
        "old_password": new_pass_user,
        "new_password": pass_user,
        "repeat_new_password": pass_user
    }
    response = requests.post(f"{BASE_URL}/api/auth/change-password", headers=headers, json=json_t)
    try:
        data = response.json()
        if response.status_code == 200:
            print("Тест №13 Пройден. ✅ ✅ Пароль пользователя изменен ", response.status_code, data)
            response = requests.post(f"{BASE_URL}/api/auth/change-password", headers=headers, json=json_orig)
        else:
            print("Тест №13. Ошибка!!! ❌ Пароль пользователя не изменен  Ответ сервера:", response.status_code, data)
    except Exception as e:
        print("Ошибка при разборе ответа:", e)
        print("Ответ сервера:", response.text)

if __name__ == "__main__":
    strat_time = time()
    login_wrong_password()            #1
    login_wrong_username()            #2
    login_inactive_user()             #3
    login_success()                   #4
    check_token()                     #5
    invalid_token()                   #6
    invalid_schema_token()            #7
    student_not_found()               #8
    token_without_sub()               #9
    expired_Token()                   #10
    student_change_password_wrong_old()#11
    student_change_password_mismatch() #12
    student_change_password()         #13
    end_time = time()
    print(f"Время выполнения запросов: {end_time-strat_time}")