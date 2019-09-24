from flask import Flask, jsonify
from flask_restful import Resource, Api, abort, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

import models, weather_service

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

api = Api(app)


def abort_if_city_not_on_api(city):
    if not weather_service.check_city_on_api(city):
        abort(404, message=f"City {city} not found")


parser = reqparse.RequestParser()
parser.add_argument('name')


class City(Resource):
    def get(self, city_name):
        try :
            city = weather_service.get_city(city_name)
        except weather_service.ServiceException as e:
            abort(422, message=e)

        return city.serialize()


class CityList(Resource):
    def put(self):
        args = parser.parse_args()

        abort_if_city_not_on_api(args['name'])

        try :
            city = weather_service.add_city(args['name'])
        except weather_service.ServiceException as e:
            abort(422, message=e)

        return city.serialize(), 201

    def get(self):
        cities = weather_service.get_cities()
        return [city.serialize() for city in cities]


api.add_resource(City, '/<city_name>')
api.add_resource(CityList, '/cities')


if __name__ == '__main__':
    app.run(debug=True)
