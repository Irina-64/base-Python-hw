import requests
from pprint import pprint

def task1():
    print("=== ЗАДАНИЕ 1: Получение данных ===")
    
    url = "https://api.github.com/search/repositories"
    params = {"q": "html"}
    
    response = requests.get(url, params=params)
    print("Статус-код:", response.status_code)
    print("JSON ответ (первые 200 символов):")
    pprint(response.json(), depth=1)
    print()

def task2():
    print("=== ЗАДАНИЕ 2: Параметры запроса ===")
    
    url = "https://jsonplaceholder.typicode.com/posts"
    params = {"userId": 1}
    
    response = requests.get(url, params=params)
    print("Статус-код:", response.status_code)
    print("Количество записей:", len(response.json()))
    
    # Покажем первые 3 записи для краткости
    for i, post in enumerate(response.json()[:3]):
        print(f"Запись {i+1}:")
        print(f"  Title: {post['title']}")
        print(f"  Body: {post['body'][:50]}...")
        print()
    print()

def task3():
    print("=== ЗАДАНИЕ 3: Отправка данных ===")
    
    url = "https://jsonplaceholder.typicode.com/posts"
    data = {
        'title': 'foo',
        'body': 'bar', 
        'userId': 1
    }
    
    response = requests.post(url, json=data)
    print("Статус-код:", response.status_code)
    print("Ответ сервера:")
    pprint(response.json())
    print()

if __name__ == "__main__":
    task1()
    task2()
    task3()