#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate

from models import db, Hero, HeroPower, Power
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact= False
migrate = Migrate(app,db)

db.init_app(app)
api = Api(app)

class Heroes(Resource):
    def get(self):
        hero = [{"id":hero.id,"name":hero.name, "super_name":hero.super_name} for hero in Hero.query.all()]
        return make_response(jsonify(hero), 200)
api.add_resource(Heroes, '/heroes')

class HeroById(Resource):
    def get(self, id):
        hero = Hero.query.filter_by(id=id).first()
        if not hero:
            return make_response(jsonify({"message": "Hero not found"}))
        hero_data = {"id":hero.id, "name":hero.name, "super_name": hero.super_name, "powers": []}
        for power in hero.powers:
            power_data = {
                "id": power.id,
                "name": power.name,
                "description": power.description
            }
            hero_data["powers"].append(power_data)
        return make_response(jsonify(hero_data), 200)
api.add_resource(HeroById, "/heroes/<int:id>")

class Powers(Resource):
    def get(self):
        power = [{
            "id": power.id,
            "name": power.name,
            "description": power.description
        }for power in Power.query.all()]
        return make_response(jsonify(power), 200)
api.add_resource(Powers, '/powers')

class PowerById(Resource):
    def get(self, id):
        power = Power.query.filter_by(id=id).first()
        if not power:
            return make_response(jsonify({"message": "Power not found"}))
        power_data = {
            "id": power.id,
            "name": power.name,
            "description": power.description
        }
        return make_response(jsonify(power_data), 200)
    
    def patch(self, id):
        power = Power.query.filter_by(id=id).first()
        if not power:
            return make_response(jsonify({"error": "Power not found"}), 404)
        if 'description' in request.json:
            power.description = request.json['description']
            try:
                db.session.commit()
                return make_response(jsonify({
                    "id": power.id,
                    "name": power.name,
                    "description": power.description
                }), 200)
            except Exception as e:
                db.session.rollback()
                return make_response(jsonify({
                    "errors": ["Validation errors"]
                }), 400)
        else:
            return make_response(jsonify({
                "errors": ["Description not provided"]
            }), 400)

api.add_resource(PowerById, "/powers/<int:id>")


if __name__ == '__main__':
    app.run(port=5555, debug=True)
