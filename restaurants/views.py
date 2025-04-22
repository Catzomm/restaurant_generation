from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import sqlite3
import random
import json
from pprint import pprint

def index(request):
    return render(request, 'index.html')

def filtered_restaurants(filters):
    query = "SELECT * FROM restaurants_restaurant"
    conditions = []
    params = []

    if cuisine := filters.get("cuisine"):
        if cuisine != "All":
            conditions.append("cuisine = ?")
            params.append(cuisine)

    avg_check = filters.get("averageCheck", [0, 0])
    if avg_check[0] > 0:
        conditions.append("average_check >= ?")
        params.append(avg_check[0])
    if avg_check[1] > 0:
        conditions.append("average_check <= ?")
        params.append(avg_check[1])

    lunch_price = filters.get("lunchPrice", [0, 0])
    if lunch_price[0] > 0:
        conditions.append("lunch_price >= ?")
        params.append(lunch_price[0])
    if lunch_price[1] > 0:
        conditions.append("lunch_price <= ?")
        params.append(lunch_price[1])

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    return query, params


@csrf_exempt
def get_random_restaurant(request):
    # Подключаемся к базе данных
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    data = json.loads(request.body)
    filtered_restaurants(data)


    # Получаем рестораны по фильтрации
    try:
        query, params = filtered_restaurants(data)
        cursor.execute(query, params)
        restaurants = cursor.fetchall()
    except Exception as e:
        print("Ошибка:", e)
    
    if restaurants:
        # Выбираем случайный ресторан
        restaurant = random.choice(restaurants)
        
        try:
            cursor.execute(f'SELECT * FROM set_lunch WHERE restaurant_id = {restaurant[0]}')
            lunch_composition = cursor.fetchall()[0][3]
        except Exception as e:
            print("Ошибка:", e)

        try:
            cursor.execute(f'SELECT * FROM restaurant_review WHERE restaurant_id = {restaurant[0]}')
            reviews = cursor.fetchall()
        except Exception as e:
            print("Ошибка:", e)
        
        # Формируем ответ
        response = {
            'name': restaurant[1],
            'average_check': restaurant[2],
            'lunch_price': restaurant[3],
            'cuisine': restaurant[4],
            'address': restaurant[5],
            'lunch_composition': lunch_composition,
            'nameReview': f'Отзывы на ресторан {restaurant[1]}',
            'name1': reviews[0][2],
            'raiting1': reviews[0][3],
            'feedback1': reviews[0][4],
            'name2': reviews[1][2],
            'raiting2': reviews[1][3],
            'feedback2': reviews[1][4],
            'name3': reviews[2][2],
            'raiting3': reviews[2][3],
            'feedback3': reviews[2][4],
        }
    else:
        response = {'message': 'Нет доступных ресторанов'}


    conn.close()
    return JsonResponse(response)
