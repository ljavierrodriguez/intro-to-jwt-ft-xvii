from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User

bpMain = Blueprint('bpMain', __name__)

@bpMain.route('/')
def main():
    return jsonify({ "msg": "REST API FLASK"}), 200


@bpMain.route('/profile')
@jwt_required()
def profile():

    id = get_jwt_identity()

    user = User.query.get(id)


    return jsonify({ "msg": "User Profile", "user": user.serialize()}), 200