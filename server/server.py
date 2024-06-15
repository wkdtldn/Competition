from flask import Flask, jsonify, request, Response, current_app, g
from pytz import timezone
from functools import wraps
import flask
import json
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, create_refresh_token
from datetime import datetime, timedelta
from flask_cors import CORS
from app import create_app
from app import api

app = Flask(__name__)
app = create_app()
app.config['JWT_SECRET_KEY'] = 'just_my_own_secret_key'
jwt = JWTManager(app)
CORS(app)

# Trash --------------------------
@app.route('/trash/data', methods=['GET'])
def trash_all():
    return json.dumps(api.get_trash(), ensure_ascii=False)

@app.route('/trash/data/<int:ID>', methods=['GET'])
def trash_one(ID):
    return json.dumps(api.find_trash(ID=ID), ensure_ascii=False)

@app.route('/trash/search', methods=['POST'])
def trash_search():
    data = request.get_json()
    word = data['word']
    return api.__search__(keyword=word)

# User --------------------------
@app.route("/sign_up", methods=['POST'])
def register():
    data = request.get_json()
    nickname = data['nickname']
    password = data['password']
    email = data['email']

    return api.sign_up(nickname=nickname, password=password, email=email)

@app.route('/login', methods=['GET','POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    if api.login(email, password):
        access_token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)
        return jsonify({'access_token': access_token, 'refresh_token' : refresh_token}), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401

@app.route('/rank', methods=['GET'])
def get_ranks():
    if api.get_rank():
        return json.dumps(api.get_rank(), ensure_ascii=False)
    return jsonify({"msg" : "No user"})

# @app.route('/admin/show_users', methods=['GET'])
# def get_all_users():
#     return json.dumps(api.get_users(), ensure_ascii=False)

# @app.route('/admin/delete_all_users', methods=['GET'])
# def __delete__():
#     return json.dumps(api.delete_all_users(), ensure_ascii=False)

@app.route("/point", methods=['POST'])
def create_point():
    data = request.get_json()
    user_id = data["user_id"]
    lat = data["lat"]
    lng = data["lng"]
    image = data["image"]

    api.create_point(user_id, lat, lng, image)
    return jsonify({"msg" : "You got a point!"})

# Jwt ---
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
