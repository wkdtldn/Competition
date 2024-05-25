from flask import Flask, jsonify, request
import flask
from flask_cors import CORS
import json
import mysql.connector
from Edit import edit

app = Flask(__name__)

CORS(app)

trash_db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Wkdtldn.mat18!",
    database="Trash_db",
    use_unicode=True
)

cursor = trash_db.cursor()

@app.route('/', methods=['GET','POST'])
def main():
    my_res = flask.Response()
    my_res.headers["Access-Control-Allow-Origin"] = "*"
    return "Hello World"

@app.route('/api/data', methods=['GET','POST'])
def post():
    print(request.method)
    sql = "SELECT * FROM waste_types"
    cursor.execute(sql)

    result = cursor.fetchall()

    dict_res = edit(dbList=result)

    return json.dumps(dict_res, ensure_ascii = False)

@app.route('/search', methods=['GET','POST'])
def search():
    print(request.method)
    

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080)