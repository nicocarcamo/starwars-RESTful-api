import os
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
from models import db, User

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

db.init_app(app) # vincular archivo models a nuestra app
Migrate(app, db) # vincular comandos de migraciones de nuestra app y base de datos (db init, db migrate, db upgrade)
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/') # Method GET by Default
def root():
    return jsonify({ "message": "Welcome to my Flask API" }), 200


@app.route('/api/users', methods=['GET'])
def get_users():

    # SELECT * FROM users;
    users = User.query.all() # [<Contact 1>, <Contact 2>]
    users = list(map(lambda user: user.serialize(), users)) # convertir en diccionarios

    return jsonify(users), 200

@app.route('/api/users', methods=['POST'])
def create_user():
    # INSERT INTO users (name, lastname, email, password) VALUES (?, ?, ?)

    datos = request.get_json()
    user = User()
    user.name = datos['name']
    user.lastname = datos['lastname']
    user.email = datos['email']
    user.password = datos['password']
    user.save() # ejecuta los dos siguiente comandos internamente

    #db.session.add(user)
    #db.session.commit()

    return jsonify(user.serialize()), 201


@app.route('/api/users/<int:id>', methods=['PUT'])
def update_user(id):
    # UPDATE user SET name="", lastname="" email="", password="" WHERE id = ?
    
    name = request.json.get('name') # None
    lastname = request.json.get('lastname') # None
    email =  request.json.get('email') # None
    password =  request.json.get('password') # None

    # SELECT * FROM users WHERE id = ?
    user = User.query.get(id)
    user.name = name
    user.lastname = lastname
    user.email = email
    user.password = password
    user.update()
    
    #db.session.commit()

    return jsonify(user.serialize()), 200

@app.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    # SELECT * FROM users WHERE id = ?
    user = User.query.get(id)

    # DELETE FROM users WHERE id=?
    user.delete()

    return jsonify({ "message": "User Deleted" }), 200

if __name__ == '__main__':
    app.run()