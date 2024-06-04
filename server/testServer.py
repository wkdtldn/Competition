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
    
    data = request.get_json()
    nickname = data['nickname']
    password = data['password']
    email = data['email']

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

    data = request.get_json()
    nickname = data['nickname']
    password = data['password']

    sql = "SELECT * FROM User"
    cursor.execute(sql)

    users = cursor.fetchall()

    for user in users:
        if user[1] != nickname or user[3] != password:
            return jsonify({'message' : 'Wrong nickname or password'}), 401
    access_token = create_access_token(identity=nickname)

    return jsonify({'access_token': access_token}), 200

# 사용자 정보 보기 엔드포인트
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users), 200

rank_list = []

@app.route('/ranks', methods=['POST','GET'])
def get_ranks():

    sql = "SELECT * FROM User"
    cursor.execute(sql)

    users = cursor.fetchall()
    

    for user in users:
        rank_list.append(user)
        return json.dumps(ascending_rank(rank_list), ensure_ascii = False)


def ascending_rank(list):
    
    pivot = list[0]
    tail = list[1:]

    left_side = [x for x in tail if x <= pivot]
    right_side = [x for x in tail if x > pivot]

    return ascending_rank(left_side) + [pivot] + ascending_rank(right_side)


# 보호된 리소스 엔드포인트
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)

