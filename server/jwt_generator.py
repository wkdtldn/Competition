import jwt
import os

# 환경 변수에서 비밀 키 읽어오기
secret_key = os.environ.get('JWT_SECRET_KEY')

# 클레임 정보
claims = {
    'user_id': 123,
    'username': 'user123',
    'role': 'admin'
}

# JWT 생성
token = jwt.encode(claims, secret_key, algorithm='HS256')

print("Generated JWT token:", token)

