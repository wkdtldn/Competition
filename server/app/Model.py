from sqlalchemy import ForeignKey, Integer, Column, Text, String, Float
from sqlalchemy.orm import relationship
from .config import db
from sqlalchemy.ext.declarative import declarative_base

class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    nickname = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    image = Column(String(1024), nullable=False, default="https://mblogthumb-phinf.pstatic.net/MjAyMDExMDFfMTgy/MDAxNjA0MjI4ODc1NDMw.Ex906Mv9nnPEZGCh4SREknadZvzMO8LyDzGOHMKPdwAg.ZAmE6pU5lhEdeOUsPdxg8-gOuZrq_ipJ5VhqaViubI4g.JPEG.gambasg/%EC%9C%A0%ED%8A%9C%EB%B8%8C_%EA%B8%B0%EB%B3%B8%ED%94%84%EB%A1%9C%ED%95%84_%ED%95%98%EB%8A%98%EC%83%89.jpg?type=w800")
    point = Column(Integer)

    def __repr__(self):
        return '<User %r>' % self.nickname

class Trash(db.Model):
    __tablename__ = "wastes"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text(), nullable=False)
    disposal_method = Column(Text(), nullable=False)
    image = Column(Text(), nullable=False)

    def __repr__(self):
        return '<Trash %r>' % self.name
    
class Point(db.Model):
    __tablename__ = "point"

    id = Column(Integer, nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    lnt = Column(Float, nullable=False)
    lat = Column(Float, nullable=False)
    image = Column(Text, nullable=False)
    date = Column(Text, nullable=False)
    time = Column(Text, nullable=False)

    user = relationship("User")
