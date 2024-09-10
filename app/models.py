from . import db
from datetime import datetime

class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    humidity = db.Column(db.Float, nullable=False)
    wind_speed = db.Column(db.Float, nullable=False)

    __table_args__ = (
        db.UniqueConstraint('city', 'date', name='unique_city_date'),
    )
