from flask import Flask, jsonify, request
import flask
import json
import mysql.connector
from Edit import edit
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

trash_db = mysql.connector.connect(
    host="localhost",
    user="jangsiu",
    password="Wkdtldn.mat18!",
    database="Trash_db",
    use_unicode=True
)

cursor = trash_db.cursor()

@app.route('/api/data', methods=['GET','POST'])
def post():
    print(request.method)
    sql = "SELECT * FROM wastes"
    cursor.execute(sql)

    wastes = cursor.fetchall()

    dict_res = edit(dbList=wastes)

    return json.dumps(dict_res, ensure_ascii = False)

@app.route('/search', methods=['GET','POST'])
def search():
    print(request.method)

    data = request.get_json()
    targetTrash = data['trash']

    sql = "SELECT * FROM wastes"
    cursor.execute(sql)
    
    wastes = cursor.fetchall()

    RelatedResult = List()
        
    for trash in wastes:
        relatedWord = trash[1]
        if targetTrash in relatedWord:
            RelatedResult.append({"name" : trash[1],"image" : trash[4]})

    return json.dump(RelatedResult, ensure_ascii = False)
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
