#from Service.main import app  # твоё FastAPI приложение
from fastapi.testclient import TestClient
import requests

def _login(login_user: str = "test", pass_user: str = "standart"):
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

# URL
BASE_URL = "https://info-run.ru/"
#BASE_URL = "http://localhost:9000/"

# админ пользователь
login_admin = 'test'
pass_admin = 'standart'

# актуальный пользователь
login_user = 'test'
pass_user = 'standart'
new_pass_user = 'standart_password'

#токены
token_admin =  _login(login_admin, pass_admin)
token = _login(login_user, pass_user)

STUDENT_ID = 2 # id существубщего студента


#client = TestClient(app)

'''в дальнейшем для прогона тестов на тестовой базе'''
# app.dependency_overrides[get_db] = override_get_db
# app.dependency_overrides[permission_required("admin")] = override_get_current_admin

