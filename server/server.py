from flask import Flask, jsonify, request, Response, current_app, g
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

## ------------------------------------------------------------------------------------------------

# # token을 decode하여 반환함, decode에 실패하는 경우 payload = None으로 반환
# def check_access_token(access_token):
#     try:
#         payload = jwt.decode(access_token, current_app.config['JWT_SECRET_KEY'], "HS256")
#         if payload['exp'] < datetime.utcnow():  # 토큰이 만료된 경우
#             payload = None
#     except jwt.InvalidTokenError:
#         payload = None
    
#     return payload


# # decorator 함수
# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwagrs):
#         access_token = request.headers.get('Authorization') # 요청의 토큰 정보를 받아옴
#         if access_token is not None: # 토큰이 있는 경우
#             payload = check_access_token(access_token) # 토큰 유효성 확인
#             if payload is None: # 토큰 decode 실패 시 401 반환
#                 return Response(status=401)
#         else: # 토큰이 없는 경우 401 반환
#             return Response(status=401)
        
#         return f(*args, **kwagrs)

#     return decorated_function

## ------------------------------------------------------------------------------------------------


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
        return jsonify({"message" : "Login Fail"})

@app.route('/rank', methods=['GET'])
# @login_required
def get_ranks():
    return json.dumps(api.get_rank(), ensure_ascii=False)

# @app.route('/admin/show_users', methods=['GET'])
# def get_all_users():
#     return json.dumps(api.get_users(), ensure_ascii=False)

# @app.route('/admin/delete_all_users', methods=['GET'])
# def __delete__():
#     return json.dumps(api.delete_all_users(), ensure_ascii=False)

@app.route("/point", methods=['POST'])
# @login_required
def create_point():
    data = request.get_json()
    user_id = data["user_id"]
    lat = data["lat"]
    lnt = data["lnt"]
    image = date["image"]

    now = datetime.now()
    date = now.strftime("%Y년 %m월 %d일")
    time = now.strftime("%H:%M")

    api.create_point(user_id, lat, lnt, image, date, time)
    return jsonify({"message" : "You got a point!"})

# Others ---
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
