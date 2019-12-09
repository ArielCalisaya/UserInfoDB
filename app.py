from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import uuid
import os

# init app
app = Flask(__name__)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))

# DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database/usersList.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# INIT DB && Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

# user Class/Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    public_id = db.Column(db.Integer, unique =True)
    username = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(100))
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(100))
    gender = db.Column(db.String(50))
    Img_url = db.Column(db.String(150))


    def __init__(self, public_id, username, password, firstname, lastname, email, gender, Img_url):
        self.public_id = public_id
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.gender = gender
        self.Img_url = Img_url

db.create_all()

# User SCHEMA data content, id=display_none
class UserSchema(ma.Schema):
    class Meta:
        fields=(
        'public_id',
        'username',
        'password',
        'firstname',
        'lastname',
        'email',
        'gender',
        'Img_url')

# Init SCHEMA
this_userSchema = UserSchema()
this_userSchemas = UserSchema(many=True)

@app.route('/')
def home():
    return render_template('index.html')

# GET all Users & Table For Users
@app.route('/all_users', methods=['GET'])
def get_allUser():
    users = User.query.all()
    output = []
    if not users:
        return jsonify({ 'message': 'No user found'})
    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['username'] = user.username
        user_data['password'] = user.password
        user_data['firstname'] = user.firstname
        user_data['lastname'] = user.lastname
        user_data['email'] = user.email
        user_data['gender'] = user.gender
        user_data['Img_url'] = user.Img_url

        output.append(user_data)
        return jsonify({ 'users': output })
    # all_users = User.query.all()
    # result = this_userSchemas.dump(all_users)
    # return jsonify(result)

@app.route('/get_user/<public_id>', methods=['GET'])
def get_User(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({ 'message': 'No user found'})

    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['username'] = user.username
    user_data['password'] = user.password
    user_data['firstname'] = user.firstname
    user_data['lastname'] = user.lastname
    user_data['email'] = user.email
    user_data['gender'] = user.gender
    user_data['Img_url'] = user.Img_url

    return jsonify({ 'user': user_data })

# POST new User
@app.route('/create_user', methods=['POST'])
def createUser():
    data = request.get_json()
    public_id = str(uuid.uuid4())
    username = data['username']
    password = data['password']
    firstname = data['firstname']
    lastname = data['lastname']
    email = data['email']
    gender = data['gender']
    Img_url = data['Img_url']

    newUser = User(public_id, username, password, firstname, lastname, email, gender, Img_url)
    db.session.add(newUser)
    db.session.commit()
    return this_userSchema.jsonify(newUser)

# Update User
@app.route('/update_user/<public_id>', methods=['PUT'])
def update_User(public_id):
    user = User.query.filter_by(public_id=public_id).first()

    username = request.json['username']
    password = request.json['password']
    firstname = request.json['firstname']
    lastname = request.json['lastname']
    email = request.json['email']
    gender = request.json['gender']
    Img_url = request.json['Img_url']

    user.username = username
    user.password = password
    user.firstname = firstname
    user.lastname = lastname
    user.email = email
    user.gender = gender
    user.Img_url = Img_url

    db.session.commit()
    return this_userSchema.jsonify(user)

@app.route('/del_user/<public_id>', methods=['DELETE'])
def delete_user(public_id):
    user= User.query.filter_by(public_id=public_id).first()
    db.session.delete(user)
    db.session.commit()

    return this_userSchema.jsonify(user)

if __name__ == '__main__':
    app.run(port= 5000, debug= True)
