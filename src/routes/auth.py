from flask import Blueprint, request, jsonify
from models import User
from werkzeug.security import generate_password_hash, check_password_hash # libreria para encriptar las contraseñas
from flask_jwt_extended import create_access_token, create_refresh_token
import datetime

bpUsers = Blueprint('bpUsers', __name__)

@bpUsers.route('/register', methods=['POST'])
def register():

    username = request.json.get('username') 
    password = request.json.get('password')
    active = request.json.get('active', True)

    if not username: return jsonify({ "status": "error", "code": 400, "message": "Username is required!"}), 400
    if not password: return jsonify({ "status": "error", "code": 400, "message": "Password is required!"}), 400


    user = User()
    user.username = username
    user.password = generate_password_hash(password)
    user.active = active
    user.save()

    data = {
        "user": user.serialize()
    }

    return jsonify({ "status": "success", "code": 201, "message": "User registered successfully!", "data": data}), 201


@bpUsers.route('/login', methods=['POST'])
def login():

    username = request.json.get('username') 
    password = request.json.get('password')

    if not username: return jsonify({ "status": "error", "code": 400, "message": "Username is required!"}), 400
    if not password: return jsonify({ "status": "error", "code": 400, "message": "Password is required!"}), 400

    user = User.query.filter_by(username=username, active=True).first()

    if not user: return jsonify({ "status": "error", "code": 401, "message": "Username/Password are incorrects"}), 401
    if not check_password_hash(user.password, password): return jsonify({ "status": "error", "code": 401, "message": "Username/Password are incorrects"}), 401

    expires = datetime.timedelta(hours=3)
    access_token = create_access_token(identity=user.id, expires_delta=expires)

    data = {
        "access_token": access_token,
        "user": user.serialize()
    }

    return jsonify({ "status": "success", "code": 200, "message": "User loggin successfully!", "data": data}), 200