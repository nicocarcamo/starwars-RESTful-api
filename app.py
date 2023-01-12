import os
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
from models import db, Contact

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


@app.route('/api/contacts', methods=['GET'])
def get_contacts():

    # SELECT * FROM contacts;
    contacts = Contact.query.all() # [<Contact 1>, <Contact 2>]
    contacts = list(map(lambda contact: contact.serialize(), contacts)) # convertir en diccionarios

    return jsonify(contacts), 200

@app.route('/api/contacts', methods=['POST'])
def crear_contact():
    # INSERT INTO contacts (name, email, phone) VALUES (?, ?, ?)

    datos = request.get_json()
    contact = Contact()
    contact.name = datos['name']
    contact.email = datos['email']
    contact.phone = datos['phone']
    contact.save() # ejecuta los dos siguiente comandos internamente

    #db.session.add(contact)
    #db.session.commit()

    return jsonify(contact.serialize()), 201


@app.route('/api/contacts/<int:id>', methods=['PUT'])
def actualizar_contact(id):
    # UPDATE contacts SET name="", email="", phone="" WHERE id = ?
    
    name = request.json.get('name') # None
    email =  request.json.get('email') # None
    phone =  request.json.get('phone') # None

    # SELECT * FROM contacts WHERE id = ?
    contact = Contact.query.get(id)
    contact.name = name
    contact.email = email
    contact.phone = phone
    contact.update()
    
    #db.session.commit()

    return jsonify(contact.serialize()), 200

@app.route('/api/contacts/<int:id>', methods=['DELETE'])
def eliminar_contact(id):
    # SELECT * FROM contacts WHERE id = ?
    contact = Contact.query.get(id)

    # DELETE FROM contacts WHERE id=?
    contact.delete()

    return jsonify({ "message": "Contacto Eliminado" }), 200

if __name__ == '__main__':
    app.run()