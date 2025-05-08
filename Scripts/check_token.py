import requests

# Запрос на получения инфмы по токену
url1 = "http://127.0.0.1:9000/login/me/"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJpdmFub3YiLCJleHAiOjE3NDY3MTc0Mjd9.XcziRt-uljrmVOCCQ_5qGXMAiiezLA6FLmAjNQOdlqI"
}
response1 = requests.get(url1, headers=headers)
print(response1.json())  # Выведет ответ от сервера
#print("Response status code:", response1.status_code)
#print("Response content:", response1.text)



# Запрос на получаения токена
'''
url2 = "http://127.0.0.1:9000/login/"
data = {
    "Login": "ivanov",
    "Password": "default123"
}
response2 = requests.post(url2, json=data)
# Печатаем полный ответ для диагностики
#print("Response status code:", response2.status_code)
#print("Response content:", response2.text)
print(response2.json())  # Выведет ответ от сервера

'''
