# app/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Инициализация расширений
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Настройка конфигурации
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:admin@localhost/project_task_12_bd')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Инициализация базы данных
    db.init_app(app)

    # Регистрация маршрутов
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app
