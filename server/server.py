from flask import Flask, jsonify, request, Response, current_app, g
from functools import wraps
from services.auth import login_required
import flask
import json
import mysql.connector
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from Edit import edit
from datetime import datetime, timedelta
from flask_cors import CORS

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'just_my_own_secret_key'
jwt = JWTManager(app)
CORS(app)

trash_db = mysql.connector.connect(
    host="localhost",
    user="jangsiu",
    password="Wkdtldn.mat18!",
    database="Trash_db",
    connect_timeout=1000,
    use_unicode=True
)

cursor = trash_db.cursor()

## ------------------------------------------------------------------------------------------------

# token을 decode하여 반환함, decode에 실패하는 경우 payload = None으로 반환
def check_access_token(access_token):
    try:
        payload = jwt.decode(access_token, current_app.config['JWT_SECRET_KEY'], "HS256")
        if payload['exp'] < datetime.utcnow():  # 토큰이 만료된 경우
            payload = None
    except jwt.InvalidTokenError:
        payload = None
    
    return payload


# decorator 함수
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwagrs):
        access_token = request.headers.get('Authorization') # 요청의 토큰 정보를 받아옴
        if access_token is not None: # 토큰이 있는 경우
            payload = check_access_token(access_token) # 토큰 유효성 확인
            if payload is None: # 토큰 decode 실패 시 401 반환
                return Response(status=401)
        else: # 토큰이 없는 경우 401 반환
            return Response(status=401)

        return f(*args, **kwagrs)

    return decorated_function

## ------------------------------------------------------------------------------------------------

@app.route('/api/data', methods=['GET','POST'])
def post():
    print(request.method)
    sql = "SELECT * FROM wastes"
    cursor.execute(sql)

    wastes = cursor.fetchall()

    dict_res = edit(dbList=wastes)

    return json.dumps(dict_res, ensure_ascii = False)

@app.route('/api/data/<int:ID>', methods=['GET'])
def get_item(ID):
    print(request.method)
    sql = "SELECT * FROM wastes where id = {}".format(ID)
    cursor.execute(sql)
    
    waste = cursor.fetchall()
    dict_res = edit(dbList=waste)
    return json.dumps(dict_res[0], ensure_ascii=False)

@app.route('/search', methods=['GET','POST'])
def search():
    print(request.method)

    data = request.get_json()
    targetTrash = data['trash']
    
    print(targetTrash)

    sql = "SELECT * FROM wastes"
    cursor.execute(sql)
    
    wastes = cursor.fetchall()
        
    RelatedWastes = []

    for trash in wastes:
        relatedWord = trash[1]
        if targetTrash in relatedWord:
            RelatedWastes.append(trash)
    
    return json.dumps(edit(dbList=RelatedWastes), ensure_ascii = False)

@app.route("/register", methods=['POST'])
def register():
    data = request.get_json()
    nickname = data['nickname']
    password = data['password']
    email = data['email']
    
    print(nickname, password, email)

    sql = "SELECT * FROM users"
    cursor.execute(sql)

    users = cursor.fetchall()

    if users:
        for user in users:
            if user[1] == nickname:
                return jsonify({'message' : 'Username already exists'}), 400

    sql = 'INSERT INTO users (nickname, email, password) VALUES (%s, %s, %s)'
    val = (nickname,email,password)

    cursor.execute(sql,val)
    cursor.commit()

    return jsonify({'message' : 'User registered successfully'}), 200

@app.route('/login', methods=['GET','POST'])
def login():
    print(request.method)

    data = request.get_json()
    email = data['email']
    password = data['password']

    sql = "SELECT * FROM users"
    cursor.execute(sql)

    users = cursor.fetchall()

    for user in users:
        if user[2] != email or user[3] != password:
            return jsonify({'message' : 'Wrong email or password'}), 401

    access_token = create_access_token(identity=email)

    return jsonify({'access_token': access_token}), 200

@app.route('/ranks', methods=['POST','GET'])
def get_ranks():

    print(request.method)

    sql = "SELECT * FROM users"
    cursor.execute(sql)

    users = cursor.fetchall()

    if users:
        return make_dict(users)
    else:
        return json.dumps({"message" : "No User"}, ensure_ascii=False)

def make_dict(list):
    result = []
    for user in list:
        result.append({"id" : user[0], "nickname" : user[1], "email" : user[2], "password" : user[3], "image" : user[4], "point" : user[5]})
    return result

def ascending_rank(list):

    if len(list) == 1:
        return list
    
    print(list)    

    pivot = list[0]
    tail = list[1:]

    left_side = [x for x in tail if x["point"] <= pivot["point"]]
    right_side = [x for x in tail if x["point"] > pivot["point"]]

    return ascending_rank(left_side) + [pivot] + ascending_rank(right_side)

@app.route("/points", methods=['POST'])
@login_required
def create_point():
    print(request.method)

    data = request.get_json()
    user_id = data["user_id"]
    lat = data["lat"]
    lnt = data["lnt"]

    now = datetime.now()
    date = now.strftime("%Y년 %m월 %d일")
    time = now.strftime("%H:%M")

    sql = "INSERT INTO point (user_id, lat, lnt, date, time) VALUES (%d, %lf, %lf, %s, %s)"
    val = (user_id, lat, lnt, date, time)

    cursor.execute(sql,val)
    cursor.commit()

    return jsonify({"message" : "You get a point!"})

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
