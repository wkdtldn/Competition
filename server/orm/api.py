from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://jangsiu:Wkdtldn.mat18!@localhost/Trash_db?charset=utf8'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = 'my_own_secret_key'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(1024), nullable=False, default="https://mblogthumb-phinf.pstatic.net/MjAyMDExMDFfMTgy/MDAxNjA0MjI4ODc1NDMw.Ex906Mv9nnPEZGCh4SREknadZvzMO8LyDzGOHMKPdwAg.ZAmE6pU5lhEdeOUsPdxg8-gOuZrq_ipJ5VhqaViubI4g.JPEG.gambasg/%EC%9C%A0%ED%8A%9C%EB%B8%8C_%EA%B8%B0%EB%B3%B8%ED%94%84%EB%A1%9C%ED%95%84_%ED%95%98%EB%8A%98%EC%83%89.jpg?type=w800")
    point = db.Column(db.Integer)

    def __repr__(self):
        return '<User %r>' % self.nickname

class Trash(db.Model):
    __tablename__ = "wastes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text(), nullable=False)
    disposal_method = db.Column(db.Text(), nullable=False)
    image = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return '<Trash %r>' % self.name
    
class Point(db.Model):
    __tablename__ = "point"

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    lnt = db.Column(db.Float, nullable=False)
    lat = db.Column(db.Float, nullable=False)
    image = db.Column(db.Text, nullable=False)
    date = db.Column(db.Text, nullable=False)
    time = db.Column(db.Text, nullable=False)

    user = relationship("User")

with app.app_context():
    db.create_all()


## Function ---------------------------------------------------------
# User ---
def get_users():
    users = User.query.all()

    user_list = []

    for user in users:
        user_list.append(
            {"id" : user.id,
             "nickname" : user.nickname,
             "email" : user.email,
             "password" : user.password,
             "image" : user.image,
             "point" : user.point})

    return user_list

def sign_up(nickname, email, password):
    users = User.query.all()

    for user in users:
        if nickname == user.nickname:
            return {"message" : "Try another one"}
            
    with app.app_context():
        new_user = User(nickname=nickname, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return {"message" : "Sign up Success"}
    
def login(email, password):
    user = User.query.filter_by(email=email).all()
    
    if user:
        if password == user.password:
            return True
        else:
            return False
        
def get_rank():
    with app.app_context():
        ranked_users = User.query.order_by(User.point.desc()).all()
    
    rank_list = []

    for user in ranked_users:
        rank_list.append(
            {"id" : user.id,
            "nickname" : user.nickname,
            "email" : user.email,
            "password" : user.password,
            "image" : user.image,
            "point" : user.point})

    return ranked_users
    
def create_point(user_id, lat, lnt, image, date, time):
    point = Point(user_id=user_id, lat=lat, lnt=lnt, image=image, date=date, time=time)
    db.session.add(point)
    db.session.commit()
    return True
    
# Trash -- 
def get_trash():
    wastes = Trash.query.all()

    trash_list = []

    for trash in wastes:
        trash_list.append(
            {"id" : trash.id,
             "name" : trash.name,
             "description" : trash.description,
             "disposal_method" : trash.disposal_method,
             "image" : trash.image})
    
    return trash_list

def __search__(keyword):
    wastes = Trash.query.all()

    result = []

    for trash in wastes:
        if keyword in trash.name:
            result.append(
                {"id" : trash.id,
                "name" : trash.name,
                "description" : trash.description,
                "disposal_method" : trash.disposal_method,
                "image" : trash.image})
            
    return result

def find_trash(ID):
    trash = Trash.query.filter_by(id=ID).all()

    return [{"id" : trash.id,
             "name" : trash.name,
             "description" : trash.description,
             "disposal_method" : trash.disposal_method,
             "image" : trash.image}]