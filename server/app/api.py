from .models import User, Trash, Point
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, Response

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'my_own_secret_key'

db = SQLAlchemy(app)


def __init__():

    db.init_app(app)

    with app.app_context():
        db.create_all()

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

if __name__ == "__main__":
    __init__()