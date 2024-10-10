from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import MySQLdb

from flask_cors import CORS


bd = Flask(__name__)

CORS(bd)
CORS(bd,resources={r"/api/*": {"origins":"http://localhost:3000"}})

# Database connection settings
# 設定 MySQL 資料庫連接
bd.config['MYSQL_HOST'] = 'localhost'
bd.config['MYSQL_USER'] = 'DevAuth'
bd.config['MYSQL_PASSWORD'] = 'Dev127336'
bd.config['MYSQL_DB'] = 'pydb'
mysql = MySQL(bd)

# 設定 SQLAlchemy 資料庫 URI
bd.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://DevAuth:Dev127336@localhost/pydb'
db = SQLAlchemy(bd)

ma = Marshmallow(bd)

def check_database_connection():
    with bd.app_context():
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
@bd.route('/api/bd/post', methods=['POST'])
def create_bd():
    data = request.get_json()

    # 定義所有可能的欄位及其默認值為 None
    fields = ['UN', 'FarmerName', 'ContactPhone', 'Fax', 'MobilePhone', 'Address', 'Email', 
              'TotalCultivationArea', 'Number', 'LandParcelNumber', 'Area', 'Crop', 
              'AreaCode', 'AreaSize', 'CropType', 'HarvestPeriod', 'EstimatedYield', 'Notes']

    # 使用字典推導來獲取所有欄位的值，未提供的欄位默認為 None
    values = {field: data.get(field) for field in fields}

    # 生成插入語句的欄位名和佔位符
    columns = ', '.join(values.keys())
    placeholders = ', '.join(['%s'] * len(values))

    cur = mysql.connection.cursor()
    cur.execute(f"INSERT INTO bd ({columns}) VALUES ({placeholders})", tuple(values.values()))
    mysql.connection.commit()
    cur.close()

    return jsonify({'status': '資料輸入成功'}), 201




@bd.route('/api/bd/get', methods=['GET'])
def get_bd():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM bd")
    bd = cur.fetchall()
    cur.close()
    return jsonify(bd)

@bd.route('/api/bd/<int:id>', methods=['DELETE'])
def delete_bd(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM bd WHERE id = %s", [id])
    mysql.connection.commit()
    return jsonify({'status': 'bd 刪除成功'}), 200

@bd.route('/api/bd/<int:id>', methods=['PUT'])
def update_bd(id):
    data = request.get_json()

    # 定義所有可能的欄位
    fields = ['UN', 'FarmerName', 'ContactPhone', 'Fax', 'MobilePhone', 'Address', 'Email', 
              'TotalCultivationArea', 'Number', 'LandParcelNumber', 'Area', 'Crop', 
              'AreaCode', 'AreaSize', 'CropType', 'HarvestPeriod', 'EstimatedYield', 'Notes']

    # 生成需要更新的欄位和值的對應列表，僅更新有提供的欄位
    updates = {field: data[field] for field in fields if field in data}

    # 如果沒有提供任何欄位，則返回錯誤
    if not updates:
        return jsonify({'error': '沒有提供任何欄位進行更新'}), 400

    # 動態生成 SQL 更新語句
    set_clause = ', '.join([f"{key} = %s" for key in updates.keys()])

    cur = mysql.connection.cursor()
    cur.execute(f"UPDATE bd SET {set_clause} WHERE ID = %s", (*updates.values(), id))
    mysql.connection.commit()
    cur.close()

    return jsonify({'status': 'bd 更新成功'}), 200



@bd.route('/', methods=['GET'])
def home():
    return "Welcome to my API!"

@bd.errorhandler(404)
def resourcenotfound(e):
    return jsonify(error=str(e)), 404

@bd.errorhandler(KeyError)
def handlekeyerror(e):
    return jsonify(error='Key not found in request data'), 400

if __name__ == '__main__':
    with bd.app_context():
        db.create_all()
    bd.run(debug=True)
