from models import *
from sqlalchemy import text, desc, asc

# User --------------------------
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
             "point" : user.point}
        )

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
    user = User.query.filter_by(email=email).all()
    
    if user:
        if password == user[0].password:
            return True
    return False
        
def get_rank():
    ranked_users = User.query.order_by(desc(User.point)).all()
    
    rank_list = []

    if ranked_users:
        for user in ranked_users:
            rank_list.append(
                {"id" : user.id,
                "nickname" : user.nickname,
                "email" : user.email,
                "password" : user.password,
                "image" : user.image,
                "point" : user.point}
            )
        return rank_list
    return False
    
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
        today_point_list.append(
            {"id" : point.id,
            "user_id" : point.user_id,
            "lat" : point.lat,
            "lng" : point.lng,
            "image" : point.image,
            "date" : point.date,
            "time" : point.time})

    return today_point_list

def find_mark_point(ID):
    point = Point.query.get(ID)

    print(point)

    return {"id" : point.id,
            "user_id" : point.user_id,
            "lat" : point.lat,
            "lng" : point.lng,
            "image" : point.image,
            "date" : point.date,
            "time" : point.time}


def all_users():
    users_query = User.query.all()

    users = []

    for user in users_query:
        users.append(
            {"id" : user.id,
            "nickname" : user.nickname,
            "email" : user.email,
            "password" : user.password,
            "image" : user.image,
            "point" : user.point}
        )
    
    return users

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
    
# Trash --------------------------
def get_trash():
    wastes = Trash.query.all()

    trash_list = []

    for trash in wastes:
        trash_list.append(
            {"id" : trash.id,
             "name" : trash.name,
             "description" : trash.description,
             "disposal_method" : trash.disposal_method,
             "image" : trash.image}
        )
    
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
                "image" : trash.image}
            )
            
    return result

def find_trash(ID):
    trash = Trash.query.filter_by(id=ID).all()

    return {"id" : trash[0].id,
             "name" : trash[0].name,
             "description" : trash[0].description,
             "disposal_method" : trash[0].disposal_method,
             "image" : trash[0].image}