from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import MySQLdb
from flask_cors import CORS


items = Flask(__name__)

CORS(items)
CORS(items,resources={r"/api/*": {"origins":"http://localhost:3000"}})

# Database connection settings
# 設定 MySQL 資料庫連接
items.config['MYSQL_HOST'] = 'localhost'
items.config['MYSQL_USER'] = 'DevAuth'
items.config['MYSQL_PASSWORD'] = 'Dev127336'
items.config['MYSQL_DB'] = 'pydb'
mysql = MySQL(items)

# 設定 SQLAlchemy 資料庫 URI
items.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://DevAuth:Dev127336@localhost/pydb'
db = SQLAlchemy(items)

ma = Marshmallow(items)

def check_database_connection():
    with items.app_context():
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
@items.route('/api/items/post', methods=['POST'])
def create_items():
    data = request.get_json()

    # 定義所有可能的欄位及其默認值為 None
    fields = ['items']

    # 使用字典推導來獲取所有欄位的值，未提供的欄位默認為 None
    values = {field: data.get(field) for field in fields}

    # 生成插入語句的欄位名和佔位符
    columns = ', '.join(values.keys())
    placeholders = ', '.join(['%s'] * len(values))

    cur = mysql.connection.cursor()
    cur.execute(f"INSERT INTO items ({columns}) VALUES ({placeholders})", tuple(values.values()))
    mysql.connection.commit()
    cur.close()

    return jsonify({'status': '資料輸入成功'}), 201




@items.route('/api/items/get', methods=['GET'])
def get_items():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM items")
    items = cur.fetchall()
    cur.close()
    return jsonify(items)

@items.route('/api/items/<int:id>', methods=['DELETE'])
def delete_items(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM items WHERE id = %s", [id])
    mysql.connection.commit()
    return jsonify({'status': 'items 刪除成功'}), 200

@items.route('/api/items/<int:id>', methods=['PUT'])
def update_items(id):
    data = request.get_json()

    # 定義所有可能的欄位
    fields = ['items']

    # 生成需要更新的欄位和值的對應列表，僅更新有提供的欄位
    updates = {field: data[field] for field in fields if field in data}

    # 如果沒有提供任何欄位，則返回錯誤
    if not updates:
        return jsonify({'error': '沒有提供任何欄位進行更新'}), 400

    # 動態生成 SQL 更新語句
    set_clause = ', '.join([f"{key} = %s" for key in updates.keys()])

    cur = mysql.connection.cursor()

    # 这里使用f-string来插入动态生成的set_clause
    query = f"UPDATE items SET {set_clause} WHERE ID = %s"
    
    # 然后执行 SQL 查询
    cur.execute(query, (*updates.values(), id))
    mysql.connection.commit()
    cur.close()

    return jsonify({'status': 'items 更新成功'}), 200




@items.route('/', methods=['GET'])
def home():
    return "Welcome to my API!"

@items.errorhandler(404)
def resourcenotfound(e):
    return jsonify(error=str(e)), 404

@items.errorhandler(KeyError)
def handlekeyerror(e):
    return jsonify(error='Key not found in request data'), 400

if __name__ == '__main__':
    with items.app_context():
        db.create_all()
    items.run(debug=True)
