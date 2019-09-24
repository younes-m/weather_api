import requests
from sqlalchemy.exc import IntegrityError

import models, config


def check_city_on_api(name):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={name}&APPID={config.apikey}"
    response = requests.get(url)

    return response.status_code == 200


def add_city(name):
    check_city_on_api(name)

    city = models.City(name.lower())

    try :
        models.db.session.add(city)
        models.db.session.commit()

    except IntegrityError:
        models.db.session.rollback()
        raise  ServiceException(f"City {name} already in database")
    return city


class ServiceException(Exception):
    def __init__(self, message):
        super().__init__(message)


def get_city(name):
    city = models.City.query.filter_by(name=name).first()

    if not city :
        raise ServiceException("City is not in database")

    set_temperature(city)

    return city


def set_temperature(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city.name}&APPID={config.apikey}"
    response = requests.get(url)

    if response.status_code != 200 :
        raise  ServiceException("Could not find city on api")

    print(response.json)

    city.temp_k = response.json()["main"]["temp"]


def get_cities():
    cities = models.City.query.order_by(models.City.name).all()

    for city in cities :
        set_temperature(city)

    return cities
