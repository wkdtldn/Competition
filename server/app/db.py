from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, Response

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://jangsiu:Wkdtldn.mat18!@localhost/Trash_db?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'my_own_secret_key'

db = SQLAlchemy(app)