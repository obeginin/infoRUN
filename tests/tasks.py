import requests
from time import time, sleep
from dotenv import load_dotenv
from config_test import BASE_URL, login_admin, pass_admin, login_user, pass_user, new_pass_user, token_admin, token


load_dotenv()

# def list_tasks(subjectID, expected_status, test_num, success_message):
#     headers = {
#         "Authorization": f"Bearer {token}"
#     }
#     params = {
#         "subjectID": subjectID
#     }
#
#     response = requests.get(f"{BASE_URL}/api/tasks", headers=headers, params=params)
#     data = response.text
#
#     try:
#         if response.status_code == expected_status:
#             print(f"Тест №{test_num} пройден. ✅ {success_message}:",
#                   response.status_code, data)
#         else:
#             print(f"❌ Тест №{test_num} не пройден",
#                   "Код:", response.status_code, "Ответ:", data)
#     except Exception as e:
#         print(f"❌ Ошибка при разборе JSON-ответа в тесте №{test_num}:", e)
#         print("Ответ:", response.text)

def list_tasks():
    headers = {
        "Authorization": f"Bearer {token}"
    }
    body = {
        "Login": "Login11",
        "Last_Name": "string",
        "First_Name": "string",
        "Middle_Name": "string",
        "Email": "user@example.com",
        "Sex": "М",
        "RoleID": 1,
        "Password": "pass"
    }

    response = requests.post(f"{BASE_URL}/api/students/new_student", headers=headers, json=body)

    print(f"URL: {response.url}")
    print(f"Status Code: {response.status_code}")
    print(f"Raw Text: {response.text}")

    try:
        data = response.json()
    except Exception as e:
        print("Ошибка при парсинге JSON:", str(e))
        data = None

    print("DATA:", data)


list_tasks()

#if __name__ == "__main__":
    # list_tasks(10, 200, 1, "Получили категории с предметами")
    # list_tasks(2, 200, 2, "Получили пустой список с категориями")
    # list_tasks(None, 200, 3, "Получили категории по всем предметам")
    # list_tasks("aasd", 422, 4, "Неправильный тип параметра")