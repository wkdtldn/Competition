from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import json
import mysql.connector

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'just_my_own_secret_key'
jwt = JWTManager(app)
CORS(app)

users = mysql.connector.connect(
    host="localhost",
    user="jangsiu",
    password="Wkdtldn.mat18!",
    database="Users",
    use_unicode=True
)

cursor = users.cursor()

# 회원가입 엔드포인트
@app.route('/register', methods=['GET','POST'])
def register():
    print(request.method)
    
    nickname = request.json.get('nickname')
    password = request.json.get('password')
    email = request.json.get('email')

    sql = "SELECT * FROM User"
    cursor.execute(sql)

    users = cursor.fetchall()

    for user in users:
        if user[1] == nickname:
            return jsonify({'message' : 'Username already exists'}), 400

    sql = 'INSERT INTO User (nickname, email, password, point) VALUES (%s, %s, %s, %d)'
    val = (nickname,email,password, 0)

    cursor.execute(sql,val)
    users.commit()

    return jsonify({'message': 'User registered successfully'}), 200

# 로그인 엔드포인트
@app.route('/login', methods=['GET','POST'])
def login():
    print(request.method)

    nickname = request.json.get('nickname')
    password = request.json.get('password')

    sql = "SELECT * FROM User"
    cursor.execute(sql)

    users = cursor.fetchall()

    for user in users:
        if user[1] == nickname:
            if user[3] == password:
                return jsonify({'message' : 'User login sucessfully'}), 200

    return jsonify({'message': 'Invalid username or password'}), 401

    access_token = create_access_token(identity=username)
    return jsonify({'access_token': access_token}), 200

# 사용자 정보 보기 엔드포인트
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users), 200

# 보호된 리소스 엔드포인트
@app.route('/protected', methods=['GET'])
@jwt_required()  # JWT가 필요한 엔드포인트에 데코레이터 추가
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)

