from config_test import BASE_URL, login_admin, pass_admin, login_user, pass_user, token_admin, token
import requests
import pytest
import httpx
from uuid import uuid4

# Фикстура создаёт уникальный логин, который потом используем в тестах
@pytest.fixture(scope="module")
def unique_login():
    return f"test_student_{uuid4().hex[:8]}"

@pytest.mark.asyncio
async def test_add_new_student_success(unique_login):
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        print(unique_login)
        headers = {"Authorization": f"Bearer {token_admin}"}
        payload = {
            "Login": unique_login,
            "Email": f"{unique_login}@example.com",
            "Password": "Secret123!",
            "Last_Name": "Иванов",
            "First_Name": "Иван",
            "Middle_Name": "Иванович",
            "Sex": "М",
            "BirthDate": "2000-01-01",
            "Comment": "Тестовый пользователь",
            "RoleID": 3,  # Укажи актуальный ID роли
            "IsActive": True
        }

        response = await client.post("/api/students/new_student", headers=headers, json=payload)

        assert response.status_code == 200, f"❌ Ошибка при добавлении студента: {response.text}"
        assert response.json()["message"] == "Студент успешно добавлен"
        print("✅ Новый студент успешно добавлен")


@pytest.mark.asyncio
async def test_edit_existing_student(unique_login):
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        headers = {"Authorization": f"Bearer {token_admin}"}
        print(unique_login)
        # 🔍 Получаем ID по логину
        search_response = await client.get(
            "/api/students/search",
            headers=headers,
            params={"field_name": "Login", "value": unique_login}
        )

        assert search_response.status_code == 200, f"Поиск студента не удался: {search_response.text}"
        student = search_response.json()

        # Подготавливаем полные новые данные (все поля из StudentCreate)
        student_id = student["ID"]
        update_payload = {
            "Login": f"{unique_login}",
            "Email": f"{unique_login}_updated@example.com",
            "Last_Name": "Иванов",
            "First_Name": "Пётр",
            "Middle_Name": "Сергеевич",
            "Sex": "М",
            "BirthDate": "1990-12-31",
            "Comment": "Обновлено полностью",
            "RoleID": 2,
            "IsActive": False
        }
        # Отправляем PATCH запрос с полным обновлением
        patch_response = await client.patch(
            f"/api/students/edit_student?id={student_id}",
            headers=headers,
            json=update_payload
        )

        assert patch_response.status_code == 200, f"PATCH не прошёл: {patch_response.text}"
        assert "успешно изменен" in patch_response.json()["message"]
        print(f"✅ Данные студента ID {student_id} обновлены")


STUDENT_ID = 8
STUDENT_LOGIN = 'test'
STUDENT_EMAIL = 'test@gmail.com'
STUDENT_PHONE = '78889997766'


@pytest.mark.asyncio
@pytest.mark.parametrize("field_name, value", [
    ("ID", STUDENT_ID),
    ("Login", STUDENT_LOGIN),
    ("Email", STUDENT_EMAIL),
    ("Phone", STUDENT_PHONE),
])
async def test_search_student(field_name, value):
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        headers = {"Authorization": f"Bearer {token_admin}"}

        params = {
            "field_name": field_name,
            "value": value
        }

        response = await client.get("/api/students/search", headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            assert field_name in data or (field_name == "ID" and "ID" in data), "В ответе нет искомого поля"
            print(f"✅ Поиск по {field_name} = {value} успешен, найден студент {data.get('Login')}")
        else:
            # Можно проверять, что при неверных данных возвращается 404
            assert response.status_code == 404
            print(f"⚠️ Студент с {field_name} = {value} не найден (ожиданный результат)")

@pytest.mark.asyncio
async def test_activate_deactivate_student(unique_login):
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        headers = {"Authorization": f"Bearer {token_admin}"}

        # 1. Сначала ищем студента по логину, чтобы получить ID
        search_response = await client.get(
            "/api/students/search",
            headers=headers,
            params={"field_name": "Login", "value": unique_login}
        )
        assert search_response.status_code == 200, f"Студент не найден: {search_response.text}"
        student = search_response.json()
        student_id = student["ID"]

        # 2. Активация студента (flag=True)
        activate_response = await client.post(
            "/api/students/active",
            headers=headers,
            params={"id": student_id, "flag": True}
        )
        assert activate_response.status_code == 200, f"Ошибка активации: {activate_response.text}"
        assert "активирован" in activate_response.json().get("message", "").lower()

        # 3. Деактивация студента (flag=False)
        deactivate_response = await client.post(
            "/api/students/active",
            headers=headers,
            params={"id": student_id, "flag": False}
        )
        assert deactivate_response.status_code == 200, f"Ошибка деактивации: {deactivate_response.text}"
        assert "деактивирован" in deactivate_response.json().get("message", "").lower()

        print(f"✅ Студент с ID {student_id} успешно активирован и деактивирован")


@pytest.mark.asyncio
async def test_delete_student(unique_login):
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        headers = {"Authorization": f"Bearer {token_admin}"}

        # Сначала ищем студента по логину, чтобы получить ID
        search_response = await client.get(
            "/api/students/search",
            headers=headers,
            params={"field_name": "Login", "value": unique_login}
        )
        assert search_response.status_code == 200, f"Студент не найден: {search_response.text}"
        student = search_response.json()
        student_id = student["ID"]

        # Теперь отправляем запрос на удаление
        delete_response = await client.post(
            "/api/students/delete_student",
            headers=headers,
            params={"id": student_id}  # если роут принимает через query
            # Если роут ожидает form, то json= не подойдет, надо data= или json=
        )

        assert delete_response.status_code == 200, f"Удаление не прошло: {delete_response.text}"
        assert "успешно удалён" in delete_response.json().get("message", ""), "Сообщение об успешном удалении отсутствует"
        print(f"✅ Студент с ID {student_id} успешно удалён")
