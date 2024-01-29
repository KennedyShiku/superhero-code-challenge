from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
from sqlalchemy.orm import validates


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Power(db.Model, SerializerMixin):
    __tablename__ = 'power'
  
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
  
    heroes = db.relationship("HeroPower", backref="power")
    
    @validates("description")
    def  validate_description(self, key, description):
        
        if not description:
            raise ValueError("Description cannot be empty")
        elif len(description) < 20 :
            raise ValueError("Description must be at least 20 characters long")
        
        return description

    def __repr__(self):
        return f"\nPower name: {self.name}\nDescription: {self.description}\nCreated at: {self.created_at}\n"
        
      

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'hero'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    powers = db.relationship("Power", secondary="heropower", backref="hero", viewonly=True)
    hero_powers = db.relationship("HeroPower", backref="hero")
    
    
    def __repr__(self):
        return f"\nSuperhero name: {self.name}\nSuper name: {self.super_name}\nCreated at: {self.created_at}\n"

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'heropower'
  
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('power.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    
    @validates('strength')
    def validate_strength(self,key,strength):
      valid_strength=['Strong','Weak','Average']
      if strength not in valid_strength:
        raise ValueError("Strength must be Strong, Weak or Average")
      return strength
    
    def __repr__(self):
        return f"\nStrength: {self.strength}\nSuper Hero: {self.hero}\nPower name: {self.power}\n"