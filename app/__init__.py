import os
import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

db = SQLAlchemy()
migrate = Migrate()

cities = ['minsk', 'warsaw', 'berlin', 'paris', 'new york', 'moscow']


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL',
                                                      'postgresql://postgres:admin@localhost/project_task_12_bd')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import bp as main_bp
    with app.app_context():
        from . import routes
        app.register_blueprint(main_bp)
    start_scheduler(app)

    return app


def trigger_fetch_weather(city):
    url = f'http://127.0.0.1:5000/weather/fetch/{city}'
    try:
        response = requests.post(url)
        if response.status_code == 201:
            print(f"Successfully fetched weather for {city}")
        else:
            print(f"Failed to fetch weather for {city}: {response.status_code}")
    except Exception as e:
        print(f"Error fetching weather for {city}: {e}")


def start_scheduler(app):
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=lambda: fetch_weather_for_cities(app),
        trigger=IntervalTrigger(hours=24),
        id='fetch_weather_job',
        name='Fetch weather data for cities every day',
        replace_existing=True
    )
    scheduler.start()


def fetch_weather_for_cities(app):
    with app.app_context():
        for city in cities:
            print(city)
            trigger_fetch_weather(city)
