from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import MySQLdb
from flask_cors import CORS


reft14 = Flask(__name__)

CORS(reft14)
CORS(reft14,resources={r"/api/*": {"origins":"http://localhost:3000"}})

# Database connection settings
# 設定 MySQL 資料庫連接
reft14.config['MYSQL_HOST'] = 'localhost'
reft14.config['MYSQL_USER'] = 'DevAuth'
reft14.config['MYSQL_PASSWORD'] = 'Dev127336'
reft14.config['MYSQL_DB'] = 'pydb'
mysql = MySQL(reft14)

# 設定 SQLAlchemy 資料庫 URI
reft14.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://DevAuth:Dev127336@localhost/pydb'
db = SQLAlchemy(reft14)

ma = Marshmallow(reft14)

def check_database_connection():
    with reft14.app_context():
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
@reft14.route('/api/reft14/post', methods=['POST'])
def create_reft14():
    data = request.get_json()

    # 定義所有可能的欄位及其默認值為 None
    fields = ['MaterialID', 'MaterialName', 'Manufacturer', 'Supplier', 'PackagingUnit', 'PackagingVolume', 'Date', 'PurchaseQuantity', 'UsageQuantity', 'RemainingQuantity']

    # 使用字典推導來獲取所有欄位的值，未提供的欄位默認為 None
    values = {field: data.get(field) for field in fields}

    # 生成插入語句的欄位名和佔位符
    columns = ', '.join(values.keys())
    placeholders = ', '.join(['%s'] * len(values))

    cur = mysql.connection.cursor()
    cur.execute(f"INSERT INTO reft14 ({columns}) VALUES ({placeholders})", tuple(values.values()))
    mysql.connection.commit()
    cur.close()

    return jsonify({'status': '資料輸入成功'}), 201




@reft14.route('/api/reft14/get', methods=['GET'])
def get_reft14():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM reft14")
    reft14 = cur.fetchall()
    cur.close()
    return jsonify(reft14)

@reft14.route('/api/reft14/<int:id>', methods=['DELETE'])
def delete_reft14(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM reft14 WHERE id = %s", [id])
    mysql.connection.commit()
    return jsonify({'status': 'reft14 刪除成功'}), 200

@reft14.route('/api/reft14/<int:id>', methods=['PUT'])
def update_reft14(id):
    data = request.get_json()

    # 定義所有可能的欄位
    fields = ['MaterialID', 'MaterialName', 'Manufacturer', 'Supplier', 'PackagingUnit', 'PackagingVolume', 'Date', 'PurchaseQuantity', 'UsageQuantity', 'RemainingQuantity']

    # 生成需要更新的欄位和值的對應列表，僅更新有提供的欄位
    updates = {field: data[field] for field in fields if field in data}

    # 如果沒有提供任何欄位，則返回錯誤
    if not updates:
        return jsonify({'error': '沒有提供任何欄位進行更新'}), 400

    # 動態生成 SQL 更新語句
    set_clause = ', '.join([f"{key} = %s" for key in updates.keys()])

    cur = mysql.connection.cursor()
    cur.execute(f"UPDATE reft14 SET {set_clause} WHERE ID = %s", (*updates.values(), id))
    mysql.connection.commit()
    cur.close()

    return jsonify({'status': 'reft14reft14 更新成功'}), 200



@reft14.route('/', methods=['GET'])
def home():
    return "Welcome to my API!"

@reft14.errorhandler(404)
def resourcenotfound(e):
    return jsonify(error=str(e)), 404

@reft14.errorhandler(KeyError)
def handlekeyerror(e):
    return jsonify(error='Key not found in request data'), 400

if __name__ == '__main__':
    with reft14.app_context():
        db.create_all()
    reft14.run(debug=True)
