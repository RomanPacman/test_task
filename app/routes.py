from datetime import datetime
from flask import Blueprint, request, jsonify, abort
from .models import Weather
from . import db
import requests
import os
from sqlalchemy.exc import IntegrityError

bp = Blueprint('main', __name__)


@bp.route('/weather', methods=['POST'])
def add_weather():
    data = request.get_json()
    city = data.get('city')
    date = data.get('date')
    temperature = data.get('temperature')
    description = data.get('description')
    humidity = data.get('humidity')
    wind_speed = data.get('wind_speed')

    if not all([city, date, temperature, humidity, wind_speed]):
        abort(400, description="Missing required fields")

    try:
        date = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        abort(400, description="Invalid date format. Use YYYY-MM-DD.")

    new_weather = Weather(
        city=city,
        date=date,
        temperature=temperature,
        description=description,
        humidity=humidity,
        wind_speed=wind_speed
    )

    try:
        db.session.add(new_weather)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()  # Откат транзакции в случае ошибки
        abort(400, description="Weather data for this city and date already exists.")

    return jsonify({'id': new_weather.id}), 201


@bp.route('/weather/<int:id>', methods=['PUT'])
def update_weather(id):
    data = request.get_json()
    weather = Weather.query.get_or_404(id)

    weather.city = data.get('city', weather.city)
    weather.date = datetime.strptime(data.get('date', weather.date.strftime('%Y-%m-%d')), '%Y-%m-%d').date()
    weather.temperature = data.get('temperature', weather.temperature)
    weather.description = data.get('description', weather.description)
    weather.humidity = data.get('humidity', weather.humidity)
    weather.wind_speed = data.get('wind_speed', weather.wind_speed)

    db.session.commit()
    return jsonify({'id': weather.id})


@bp.route('/weather/<int:id>', methods=['DELETE'])
def delete_weather(id):
    weather = Weather.query.get_or_404(id)
    db.session.delete(weather)
    db.session.commit()
    return '', 204


@bp.route('/weather/<int:id>', methods=['GET'])
def get_weather(id):
    weather = Weather.query.get_or_404(id)
    return jsonify({
        'id': weather.id,
        'city': weather.city,
        'date': weather.date.strftime('%Y-%m-%d'),
        'temperature': weather.temperature,
        'description': weather.description,
        'humidity': weather.humidity,
        'wind_speed': weather.wind_speed
    })


@bp.route('/weather/fetch/<string:city>', methods=['POST'])
def fetch_weather(city):
    api_key = os.getenv('WEATHER_API_KEY')
    if not api_key:
        abort(500, description='API key not found in environment variables')

    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

    response = requests.get(url)
    if response.status_code != 200:
        abort(response.status_code, description='Failed to fetch weather data from external API')

    data = response.json()
    weather_data = {
        'city': city,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'temperature': data['main']['temp'],
        'description': data['weather'][0]['description'],
        'humidity': data['main']['humidity'],
        'wind_speed': data['wind']['speed']
    }

    new_weather = Weather(
        city=weather_data['city'],
        date=datetime.strptime(weather_data['date'], '%Y-%m-%d').date(),
        temperature=weather_data['temperature'],
        description=weather_data['description'],
        humidity=weather_data['humidity'],
        wind_speed=weather_data['wind_speed']
    )

    try:
        db.session.add(new_weather)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()  # Откат транзакции в случае ошибки
        return jsonify({'error': 'Weather data for this city and date already exists.'}), 400

    return jsonify({'id': new_weather.id}), 201
