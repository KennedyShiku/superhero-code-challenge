from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from faker import Faker
from random import choice

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import your models after creating the Flask app and SQLAlchemy instance
from models import Power, Hero, HeroPower

fake = Faker()
Faker.seed(123)  # Set a seed for reproducibility using the class method

def generate_fake_data(model_cls, num_instances=10, **kwargs):
    instances = []
    for _ in range(num_instances):
        instance = model_cls(**kwargs)
        instances.append(instance)
    db.session.add_all(instances)
    db.session.commit()

def generate_fake_hero_powers(num_connections=20):
    hero_powers = []
    for _ in range(num_connections):
        hero_id = choice(db.session.query(Hero.id).all())[0]
        power_id = choice(db.session.query(Power.id).all())[0]
        strength = fake.random_element(elements=('Strong', 'Weak', 'Average'))
        hero_power = HeroPower(
            hero_id=hero_id,
            power_id=power_id,
            strength=strength
        )
        hero_powers.append(hero_power)
    db.session.add_all(hero_powers)
    db.session.commit()

if __name__ == '__main__':
    # Generate fake data
    with app.app_context():
        generate_fake_data(Power)
        generate_fake_data(Hero)
        generate_fake_hero_powers()
