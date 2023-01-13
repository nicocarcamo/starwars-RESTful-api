import os
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
from models import db, User, Planet, Character, Favorite

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



# User routes
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



# Planet routes
@app.route('/api/planets', methods=['GET'])
def get_planets():

    planets = Planet.query.all()
    planets = list(map(lambda planet: planet.serialize(), planets))

    return jsonify(planets), 200

@app.route('/api/planets', methods=['POST'])
def create_planet():

    datos = request.get_json()
    planet = Planet()
    planet.name = datos['name']
    planet.climate = datos['climate']
    planet.terrain = datos['terrain']
    planet.save()

    return jsonify(planet.serialize()), 201


@app.route('/api/planets/<int:id>', methods=['PUT'])
def update_planet(id):
    
    name = request.json.get('name')
    climate = request.json.get('climate')
    terrain =  request.json.get('terrain')

    planet = Planet.query.get(id)
    planet.name = name
    planet.climate = climate
    planet.terrain = terrain
    planet.update()

    return jsonify(planet.serialize()), 200

@app.route('/api/planets/<int:id>', methods=['DELETE'])
def delete_planet(id):

    planet = Planet.query.get(id)
    planet.delete()

    return jsonify({ "message": "Planet Deleted" }), 200



# Character routes
@app.route('/api/characters', methods=['GET'])
def get_characters():

    characters = Character.query.all()
    characters = list(map(lambda character: character.serialize(), characters))

    return jsonify(characters), 200

@app.route('/api/characters', methods=['POST'])
def create_character():

    datos = request.get_json()
    character = Character()
    character.name = datos['name']
    character.age = datos['age']
    character.save()

    return jsonify(character.serialize()), 201


@app.route('/api/characters/<int:id>', methods=['PUT'])
def update_character(id):
    
    name = request.json.get('name')
    age = request.json.get('age')


    character = Character.query.get(id)
    character.name = name
    character.age = age
    character.update()

    return jsonify(character.serialize()), 200

@app.route('/api/characters/<int:id>', methods=['DELETE'])
def delete_character(id):

    character = Character.query.get(id)
    character.delete()

    return jsonify({ "message": "Character Deleted" }), 200


# Favorite routes
@app.route('/api/favorites', methods=['GET'])
def get_favorites():

    favorites = Favorite.query.all()
    favorites = list(map(lambda favorite: favorite.serialize(), favorites))
    return jsonify(favorites), 200

@app.route('/api/favorites', methods=['POST'])
def create_favorite():

    datos = request.get_json()
    favorite = Favorite()
    favorite.user_id = datos['user_id']
    favorite.character_id = datos['character_id']
    favorite.planet_id = datos['planet_id']
    favorite.save()

    return jsonify(favorite.serialize()), 201


@app.route('/api/favorites/<int:id>', methods=['PUT'])
def update_favorite(id):
    
    user_id = request.json.get('user_id')
    character_id = request.json.get('character_id')
    planet_id = request.json.get('planet_id')


    favorite = Favorite.query.get(id)
    favorite.user_id = user_id
    favorite.character_id = character_id
    favorite.planet_id = planet_id
    favorite.update()

    return jsonify(favorite.serialize()), 200

@app.route('/api/favorites/<int:id>', methods=['DELETE'])
def delete_favorite(id):

    favorite = Favorite.query.get(id)
    favorite.delete()

    return jsonify({ "message": "Favorite Deleted" }), 200

if __name__ == '__main__':
    app.run()