from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)

    restaurant_pizzas = db.relationship(
        'RestaurantPizza',
        back_populates='restaurant',
        cascade='all, delete-orphan',
        overlaps="pizzas,restaurant_pizzas"
    )

    pizzas = db.relationship(
        'Pizza',
        secondary='restaurant_pizzas',
        back_populates='restaurants',
        overlaps="restaurant_pizzas,restaurant"
    )

    serialize_rules = ('-restaurant_pizzas.restaurant', '-pizzas.restaurants')


class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ingredients = db.Column(db.String, nullable=False)

    restaurant_pizzas = db.relationship(
        'RestaurantPizza',
        back_populates='pizza',
        overlaps="restaurants,restaurant_pizzas"
    )

    restaurants = db.relationship(
        'Restaurant',
        secondary='restaurant_pizzas',
        back_populates='pizzas',
        overlaps="restaurant_pizzas,pizza"
    )

    serialize_rules = ('-restaurant_pizzas.pizza', '-restaurants.pizzas')


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = 'restaurant_pizzas'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)

    pizza = db.relationship(
        'Pizza',
        back_populates='restaurant_pizzas',
        overlaps="restaurants,pizzas"
    )

    restaurant = db.relationship(
        'Restaurant',
        back_populates='restaurant_pizzas',
        overlaps="pizzas,restaurants"
    )

    serialize_rules = ('-pizza.restaurant_pizzas', '-restaurant.restaurant_pizzas')

    @validates('price')
    def validate_price(self, key, value):
        if not (1 <= value <= 30):
            raise ValueError("validation errors")
        return value
