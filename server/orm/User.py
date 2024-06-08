from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://jangsiu:Wkdtldn.mat18!@localhost/Trash_db?charset=utf8'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = 'my_own_secret_key'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"
    # def __init__(self, id, nickname, email, password, image, point):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(1024), nullable=False, default="https://mblogthumb-phinf.pstatic.net/MjAyMDExMDFfMTgy/MDAxNjA0MjI4ODc1NDMw.Ex906Mv9nnPEZGCh4SREknadZvzMO8LyDzGOHMKPdwAg.ZAmE6pU5lhEdeOUsPdxg8-gOuZrq_ipJ5VhqaViubI4g.JPEG.gambasg/%EC%9C%A0%ED%8A%9C%EB%B8%8C_%EA%B8%B0%EB%B3%B8%ED%94%84%EB%A1%9C%ED%95%84_%ED%95%98%EB%8A%98%EC%83%89.jpg?type=w800")
    point = db.Column(db.Integer)

    def __repr__(self):
        return '<User %r>' % self.nickname

with app.app_context():
    db.create_all()


@app.route('/users', methods=['GET','POST'])
def get_users():
    print(request.method)

    users = User.query.all()
    return {"users" : users[0]}

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)