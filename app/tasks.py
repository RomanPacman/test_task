import requests
from datetime import datetime
import os

# Импортируем модели внутри функции, чтобы избежать циклического импорта
def fetch_weather_data(city):
    API_KEY = os.getenv('WEATHER_API_KEY')
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    return response.json()

def collect_weather_data(app, db):
    with app.app_context():
        from .models import City, Weather  # Импорт внутри функции

        cities = City.query.all()
        for city in cities:
            data = fetch_weather_data(city.name)
            if 'main' in data:
                temperature = data['main']['temp']
                description = data['weather'][0]['description']
                humidity = data['main']['humidity']
                wind_speed = data['wind']['speed']

                weather = Weather.query.filter_by(city_id=city.id, date=datetime.now().date()).first()
                if weather:
                    weather.temperature = temperature
                    weather.description = description
                    weather.humidity = humidity
                    weather.wind_speed = wind_speed
                else:
                    new_weather = Weather(
                        city_id=city.id,
                        date=datetime.now().date(),
                        temperature=temperature,
                        description=description,
                        humidity=humidity,
                        wind_speed=wind_speed
                    )
                    db.session.add(new_weather)
                db.session.commit()
            else:
                print(f"Error fetching weather data for {city.name}: {data}")
