from models import *
from sqlalchemy import text, desc, asc

# User --------------------------
def get_users():
    users = User.query.all()

    user_list = []

    for user in users:
        user_list.append(user_dict(user))

    return user_list

def sign_up(nickname, email, password):
    users = User.query.all()

    for user in users:
        if nickname == user.nickname:
            return {"msg" : "Try another one"}
            
    new_user = User(nickname=nickname, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return {"msg" : "Sign up Success"}
    
def login(email, password):
    user = User.query.filter_by(email=email)
    
    if user:
        if password == user[0].password:
            return True
    return False
        
def get_rank():
    ranked_users = User.query.order_by(desc(User.point)).all()
    
    rank_list = []

    if ranked_users:
        for user in ranked_users:
            rank_list.append(user_dict(user))
        return rank_list
    return False

def delete_all_users():
    try:
        deleted_users = db.session.query(User).delete()
        db.session.commit()

        db.session.execute(text('ALTER TABLE users AUTO_INCREMENT = 1'))
        db.session.commit()

        return {"msg" : f"{deleted_users} users have been deleted"}
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}
    
def user_info(*args, **kwargs):
    for arg in args:
        user_args = User.query.get(arg)
        return user_dict(user_args)
    for key, value in kwargs.items():
        user_kwargs = User.query.filter_by(email=value)
        return user_dict(user_kwargs[0])

# Point --------------------------
def create_point(user_id, lat, lng, image, date, time):
    point = Point(user_id=user_id, lat=lat, lng=lng, image=image, date=date, time=time)
    db.session.add(point)
    db.session.commit()
    return True

def delete_all_point():
    try:
        deleted_point = db.session.query(Point).delete()
        db.session.commit()

        db.session.execute(text('ALTER TABLE point AUTO_INCREMENT = 1'))
        db.session.commit()

        return {"msg" : f"{deleted_point} point have been deleted"}
    
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}

def get_point():
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    points = Point.query.filter_by(date=today).all()

    today_point_list = []

    for point in points:
        today_point_list.append(point_dict(point))

    return today_point_list

def find_mark_point(ID):
    point = Point.query.get(ID)

    return point_dict(point)

def get_all_point():
    points = Point.query.all()
    
    point_list = []

    for point in points:
        point_list.append(point_dict(point))
    
    return point_list
    
# Trash --------------------------
def get_trash():
    wastes = Trash.query.all()

    trash_list = []

    for trash in wastes:
        trash_list.append(trash_dict(trash))
    
    return trash_list

def __search__(keyword):
    wastes = Trash.query.all()

    result = []

    for trash in wastes:
        if keyword in trash.name:
            result.append(trash_dict(trash))
            
    return result

def find_trash(ID):
    trash = Trash.query.get(ID)

    return {"id" : trash.id,
             "name" : trash.name,
             "description" : trash.description,
             "disposal_method" : trash.disposal_method,
             "image" : trash.image}

# Help --------------------------
def user_dict(key):
    return {"id" : key.id,
            "nickname" : key.nickname,
            "email" : key.email,
            "password" : key.password,
            "image" : key.image,
            "point" : key.point}

def point_dict(key):
    return {"id" : key.id,
            "user_id" : key.user_id,
            "lat" : key.lat,
            "lng" : key.lng,
            "image" : key.image,
            "date" : key.date,
            "time" : key.time}

def trash_dict(key):
    return {"id" : key.id,
            "name" : key.name,
            "description" : key.description,
            "disposal_method" : key.disposal_method,
            "image" : key.image}