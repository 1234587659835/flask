from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import MySQLdb
from flask_cors import CORS


fr06 = Flask(__name__)

CORS(fr06)
CORS(fr06,resources={r"/api/*": {"origins":"http://localhost:3000"}})

# Database connection settings
# 設定 MySQL 資料庫連接
fr06.config['MYSQL_HOST'] = 'localhost'
fr06.config['MYSQL_USER'] = 'DevAuth'
fr06.config['MYSQL_PASSWORD'] = 'Dev127336'
fr06.config['MYSQL_DB'] = 'pydb'
mysql = MySQL(fr06)

# 設定 SQLAlchemy 資料庫 URI
fr06.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://DevAuth:Dev127336@localhost/pydb'
db = SQLAlchemy(fr06)

ma = Marshmallow(fr06)

def check_database_connection():
    with fr06.app_context():
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT 1")
            data = cur.fetchone()
            cur.close()
            print("Connected to the database successfully.")
        except Exception as e:
            print(f"Error connecting to the database: {str(e)}")

check_database_connection()

# API routes...
@fr06.route('/api/fr06/post', methods=['POST'])
def create_fr06():
    data = request.get_json()

    # 定義所有可能的欄位及其默認值為 None
    fields = ['DateUsed', 'FieldCode', 'Crop', 'FertilizerType', 'MaterialCodeOrName', 'FertilizerAmount', 'DilutionFactor', 'Operator']

    # 使用字典推導來獲取所有欄位的值，未提供的欄位默認為 None
    values = {field: data.get(field) for field in fields}

    # 生成插入語句的欄位名和佔位符
    columns = ', '.join(values.keys())
    placeholders = ', '.join(['%s'] * len(values))

    cur = mysql.connection.cursor()
    cur.execute(f"INSERT INTO fr06 ({columns}) VALUES ({placeholders})", tuple(values.values()))
    mysql.connection.commit()
    cur.close()

    return jsonify({'status': '資料輸入成功'}), 201




@fr06.route('/api/fr06/get', methods=['GET'])
def get_fr06():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM fr06")
    fr06 = cur.fetchall()
    cur.close()
    return jsonify(fr06)

@fr06.route('/api/fr06/<int:id>', methods=['DELETE'])
def delete_fr06(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM fr06 WHERE id = %s", [id])
    mysql.connection.commit()
    return jsonify({'status': 'fr06 刪除成功'}), 200

@fr06.route('/api/fr06/<int:id>', methods=['PUT'])
def update_fr06(id):
    data = request.get_json()

    # 定義所有可能的欄位
    fields = ['DateUsed', 'FieldCode', 'Crop', 'FertilizerType', 'MaterialCodeOrName', 'FertilizerAmount', 'DilutionFactor', 'Operator']

    # 生成需要更新的欄位和值的對應列表，僅更新有提供的欄位
    updates = {field: data[field] for field in fields if field in data}

    # 如果沒有提供任何欄位，則返回錯誤
    if not updates:
        return jsonify({'error': '沒有提供任何欄位進行更新'}), 400

    # 動態生成 SQL 更新語句
    set_clause = ', '.join([f"{key} = %s" for key in updates.keys()])

    cur = mysql.connection.cursor()
    cur.execute(f"UPDATE fr06 SET {set_clause} WHERE ID = %s", (*updates.values(), id))
    mysql.connection.commit()
    cur.close()

    return jsonify({'status': 'fr06 更新成功'}), 200



@fr06.route('/', methods=['GET'])
def home():
    return "Welcome to my API!"

@fr06.errorhandler(404)
def resourcenotfound(e):
    return jsonify(error=str(e)), 404

@fr06.errorhandler(KeyError)
def handlekeyerror(e):
    return jsonify(error='Key not found in request data'), 400

if __name__ == '__main__':
    with fr06.app_context():
        db.create_all()
    fr06.run(debug=True)
