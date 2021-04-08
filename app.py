from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:VFvf2380@localhost/lab6-db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    price = db.Column(db.Integer, unique=False)
    producer = db.Column(db.String(250), unique=False)
    gender = db.Column(db.String(250), unique=False)

    def __init__(self, name, price, producer, gender):
        self.name = name
        self.price = price
        self.producer = producer
        self.gender = gender


class ItemSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'price', 'producer', 'gender')


item_schema = ItemSchema(strict=True)
items_schema = ItemSchema(many=True, strict=True)


@app.route('/', methods=['POST'])
def add_items():
    name = request.json['name']
    price = request.json['price']
    producer = request.json['producer']
    gender = request.json['gender']

    new_item = Items(name, price, producer, gender)

    db.session.add(new_item)
    db.session.commit()

    return item_schema.jsonify(new_item)


@app.route('/get', methods=['GET'])
def get_items():
    all_items = Items.query.all()
    result = items_schema.dump(all_items)
    return jsonify(result.data)


@app.route('/get/<id>', methods=['GET'])
def get_items_by_id(id):
    item = Items.query.get(id)
    return item_schema.jsonify(item)


@app.route('/update/<id>', methods=['PUT'])
def update_items_by_id(id):
    item = Items.query.get(id)

    name = request.json['name']
    price = request.json['price']
    producer = request.json['producer']
    gender = request.json['gender']

    item.name = name
    item.price = price
    item.producer = producer
    item.gender = gender

    db.session.commit()

    return item_schema.jsonify(item)


@app.route('/delete/<id>', methods=['DELETE'])
def delete_items_by_id(id):
    item = Items.query.get(id)
    db.session.delete(item)
    db.session.commit()
    return item_schema.jsonify(item)


if __name__ == '__main__':
    app.run(debug=True)
