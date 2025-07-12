import requests

# Запрос на получаения токена ()

url2 = "http://localhost:9000/auth/login"
data = {
    "Login": "ivan",
    "Password": "standart"
}
response2 = requests.post(url2, json=data)
# Печатаем полный ответ для диагностики
#print("Response status code:", response2.status_code)
#print("Response content:", response2.text)
print(response2.json())  # Выведет ответ от сервера
input()
# Запрос на получаения токена (student)

data2 = {
    "Login": "petrovv",
    "Password": "default123"
}
response2 = requests.post(url2, json=data2)
# Печатаем полный ответ для диагностики
#print("Response status code:", response2.status_code)
#print("Response content:", response2.text)
print(response2.json())  # Выведет ответ от сервера

"""Авторизация пользователя"""
# Запрос на получения инфмы по токену (все пользователи)
url1 = "http://127.0.0.1:9000/login/me/"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJpdmFub3YiLCJleHAiOjE3NDY3MjAwMTJ9.Qr4U4qt02xfo9SXfTT4_BFY-FNBQg8wjok269TBBrtI"
}
response1 = requests.get(url1, headers=headers)
print(response1.json())  # Выведет ответ от сервера

"""Авторизация админа"""
# Запрос на получения инфмы по токену (admin)
url3 = "http://127.0.0.1:9000/admin/dashboard/"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJpdmFub3YiLCJleHAiOjE3NDY3MjAwMTJ9.Qr4U4qt02xfo9SXfTT4_BFY-FNBQg8wjok269TBBrtI"
}
response3 = requests.get(url3, headers=headers)
print(response3.json())  # Выведет ответ от сервера

# Запрос на получения инфмы по токену (not admin)
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJwZXRyb3Z2IiwiZXhwIjoxNzQ2NzIwNTc1fQ.-EsbtvODODvVzQ8Iefp1dkafhezMdN_h6NfWWxshAo4"
}
response4 = requests.get(url3, headers=headers)
print(response4.json())  # Выведет ответ от сервера





