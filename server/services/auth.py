from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask import Flask, jsonify, request, Response, current_app, g
from datetime import datetime

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'just_my_own_secret_key'
jwt = JWTManager(app)

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
