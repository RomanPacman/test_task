# import requests
# from datetime import datetime
# import os
#
#
# def fetch_weather_data(city):
#     API_KEY = os.getenv('WEATHER_API_KEY')
#     print(API_KEY)
#     url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
#     print(url)
#     response = requests.get(url)
#     return response.json()
#
#
#
# def periodic_task(app, db):
#     with app.app_context():  # Устанавливаем контекст приложения
#         city = 'Minsk'
#         data = fetch_weather_data(city)
#         print(data)
#         if 'main' in data:
#             temperature = data['main']['temp']
#             description = data['weather'][0]['description']
#             humidity = data['main']['humidity']
#             wind_speed = data['wind']['speed']
#
#             from app.models import Weather  # Импортируем внутри функции, чтобы избежать циклического импорта
#
#             # Работа с базой данных
#             weather = Weather.query.filter_by(city=city, date=datetime.now().date()).first()
#             if weather:
#                 # Обновляем существующую запись
#                 weather.temperature = temperature
#                 weather.description = description
#                 weather.humidity = humidity
#                 weather.wind_speed = wind_speed
#             else:
#                 # Создаем новую запись
#                 new_weather = Weather(
#                     city=city,
#                     date=datetime.now().date(),
#                     temperature=temperature,
#                     description=description,
#                     humidity=humidity,
#                     wind_speed=wind_speed
#                 )
#                 db.session.add(new_weather)
#             db.session.commit()
#         else:
#             print("Ошибка в ответе API:", data)