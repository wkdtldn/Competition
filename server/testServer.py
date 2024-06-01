from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # JWT에 사용될 비밀 키 설정
jwt = JWTManager(app)

# 사용자 정보 (임시로 딕셔너리 형태로 저장)
users = {
    'user1': 'password1',
    'user2': 'password2'
}

# 회원가입 엔드포인트
@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    if username in users:
        return jsonify({'message': 'Username already exists'}), 400

    users[username] = generate_password_hash(password)
    return jsonify({'message': 'User registered successfully'}), 200

# 로그인 엔드포인트
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if username not in users or not check_password_hash(users[username], password):
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

