from auth import _login
import requests
from time import time, sleep
from dotenv import load_dotenv

import jwt
from datetime import datetime, timedelta, timezone
import os

#from Service.Scripts.check_token import headers

load_dotenv()

BASE_URL = "https://info-run.ru/"
#BASE_URL = "http://127.0.0.1:9000/"

# актуальный пользователь
login_user = 'test'
pass_user = 'standart'
new_pass_user = 'standart_password'
token = _login()



def list_tasks(subjectID, expected_status, test_num, success_message):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "subjectID": subjectID
    }

    response = requests.get(f"{BASE_URL}/api/tasks", headers=headers, params=params)
    data = response.text

    try:
        if response.status_code == expected_status:
            print(f"Тест №{test_num} пройден. ✅ {success_message}:",
                  response.status_code, data)
        else:
            print(f"❌ Тест №{test_num} не пройден",
                  "Код:", response.status_code, "Ответ:", data)
    except Exception as e:
        print(f"❌ Ошибка при разборе JSON-ответа в тесте №{test_num}:", e)
        print("Ответ:", response.text)



if __name__ == "__main__":
    list_tasks(10, 200, 1, "Получили категории с предметами")
    list_tasks(2, 200, 2, "Получили пустой список с категориями")
    list_tasks(None, 200, 3, "Получили категории по всем предметам")
    list_tasks("aasd", 422, 4, "Неправильный тип параметра")