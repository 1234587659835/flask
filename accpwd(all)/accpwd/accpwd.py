from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import MySQLdb



accpwd = Flask(__name__)

CORS(accpwd)
CORS(accpwd,resources={r"/api/*": {"origins":"http://localhost:3000"}})

# Database connection settings
# 設定 MySQL 資料庫連接
accpwd.config['MYSQL_HOST'] = 'localhost'
accpwd.config['MYSQL_USER'] = 'DevAuth'
accpwd.config['MYSQL_PASSWORD'] = 'Dev127336'
accpwd.config['MYSQL_DB'] = 'pydb'
mysql = MySQL(accpwd)

# 設定 SQLAlchemy 資料庫 URI
accpwd.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://DevAuth:Dev127336@localhost/pydb'
db = SQLAlchemy(accpwd)

ma = Marshmallow(accpwd)

def check_database_connection():
    with accpwd.app_context():
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
@accpwd.route('/api/accpwd/post', methods=['POST'])
def create_accpwd():
    data = request.get_json()

    # 提供預設值
    password = data.get('PASSWORD', None)

    un = data.get('UN', None)


    # 如果沒有提供至少一個值，可以返回錯誤（視需求而定）
    if not any([password, un]):
        return jsonify({'error': '至少需要一個欄位'}), 400

    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO accpwd (PASSWORD, UN ) VALUES (%s, %s)", 
        (password, un)
    )
    mysql.connection.commit()
    cur.close()

    return jsonify({'status': '資料輸入成功'}), 201


@accpwd.route('/api/accpwd/get', methods=['GET'])
def get_accpwd():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM accpwd")
    accpwd = cur.fetchall()
    cur.close()
    return jsonify(accpwd)

@accpwd.route('/api/accpwd/<int:id>', methods=['PUT'])
def update_accpwd(id):
    data = request.get_json()

    new_password = data.get('PASSWORD')
    new_un = data.get('UN')

    # Check if the necessary fields are provided
    if new_password is None or new_un is None:
        return jsonify({'error': 'Required data not provided in request'}), 400

    # Update only PASSWORD and UN fields
    cur = mysql.connection.cursor()
    cur.execute("UPDATE accpwd SET PASSWORD = %s, UN = %s WHERE ID = %s", 
                (new_password, new_un, id))
    mysql.connection.commit()
    cur.close()

    return jsonify({'status': 'accpwd 更新成功'}), 200

@accpwd.route('/api/accpwd/<int:id>', methods=['DELETE'])
def delete_accpwd(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM accpwd WHERE id = %s", [id])
    mysql.connection.commit()
    return jsonify({'status': 'accpwd 刪除成功'}), 200

@accpwd.route('/', methods=['GET'])
def home():
    return "Welcome to my API!"

@accpwd.errorhandler(404)
def resourcenotfound(e):
    return jsonify(error=str(e)), 404

@accpwd.errorhandler(KeyError)
def handlekeyerror(e):
    return jsonify(error='Key not found in request data'), 400

if __name__ == '__main__':
    with accpwd.app_context():
        db.create_all()
    accpwd.run(debug=True)
