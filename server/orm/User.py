from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://jangsiu:Wkdtldn.mat18!@localhost/Trash_db'  # MySQL 연결 정보
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(1024), nullable=False, default="https://mblogthumb-phinf.pstatic.net/MjAyMDExMDFfMTgy/MDAxNjA0MjI4ODc1NDMw.Ex906Mv9nnPEZGCh4SREknadZvzMO8LyDzGOHMKPdwAg.ZAmE6pU5lhEdeOUsPdxg8-gOuZrq_ipJ5VhqaViubI4g.JPEG.gambasg/%EC%9C%A0%ED%8A%9C%EB%B8%8C_%EA%B8%B0%EB%B3%B8%ED%94%84%EB%A1%9C%ED%95%84_%ED%95%98%EB%8A%98%EC%83%89.jpg?type=w800")

    def __repr__(self):
        return '<User %r>' % self.username

db.create_all()

@app.route('/', methods=['GET','POST'])
def main():
    user = User(nickname="kakakaka", email="asdf1234@gmail.com")
    db.session.add(user)
    db.session.commit()

    users = User.query.all()
    return '<br>'.join([user.nickname for user in users])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9080, debug=True)