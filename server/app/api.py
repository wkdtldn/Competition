from models import *
from sqlalchemy import text

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
            return {"message" : "Try another one"}
            
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
    ranked_users = User.query.order_by(User.point.desc()).all()
    
    rank_list = []

    for user in ranked_users:
        rank_list.append(
            {"id" : user.id,
            "nickname" : user.nickname,
            "email" : user.email,
            "password" : user.password,
            "image" : user.image,
            "point" : user.point}
        )

    return ranked_users
    
def create_point(user_id, lat, lnt, image, date, time):
    point = Point(user_id=user_id, lat=lat, lnt=lnt, image=image, date=date, time=time)
    db.session.add(point)
    db.session.commit()
    return True

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

        import __hello__
        __hello__.main()

        db.session.execute(text('ALTER TABLE users AUTO_INCREMENT = 1'))
        db.session.commit()

        return {"message" : f"{deleted_users} users have been deleted"}
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


    return [{"id" : trash[0].id,
             "name" : trash[0].name,
             "description" : trash[0].description,
             "disposal_method" : trash[0].disposal_method,
             "image" : trash[0].image}]