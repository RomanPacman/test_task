# app/routes.py
from datetime import datetime

from flask import Blueprint, request, jsonify, abort
from .models import Weather
from . import db

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
    db.session.add(new_weather)
    db.session.commit()
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
