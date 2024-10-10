from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import MySQLdb
from flask_cors import CORS


ccfr22 = Flask(__name__)

CORS(ccfr22)
CORS(ccfr22,resources={r"/api/*": {"origins":"http://localhost:3000"}})

# Database connection settings
# 設定 MySQL 資料庫連接
ccfr22.config['MYSQL_HOST'] = 'localhost'
ccfr22.config['MYSQL_USER'] = 'DevAuth'
ccfr22.config['MYSQL_PASSWORD'] = 'Dev127336'
ccfr22.config['MYSQL_DB'] = 'pydb'
mysql = MySQL(ccfr22)

# 設定 SQLAlchemy 資料庫 URI
ccfr22.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://DevAuth:Dev127336@localhost/pydb'
db = SQLAlchemy(ccfr22)

ma = Marshmallow(ccfr22)

def check_database_connection():
    with ccfr22.app_context():
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
@ccfr22.route('/api/ccfr22/post', methods=['POST'])
def create_ccfr22():
    data = request.get_json()

    # 定義所有可能的欄位及其默認值為 None
    fields = ['FieldCode', 'Date', 'CustomerName', 'CustomerPhone','Complaint','Resolution','Processor']

    # 使用字典推導來獲取所有欄位的值，未提供的欄位默認為 None
    values = {field: data.get(field) for field in fields}

    # 生成插入語句的欄位名和佔位符
    columns = ', '.join(values.keys())
    placeholders = ', '.join(['%s'] * len(values))

    cur = mysql.connection.cursor()
    cur.execute(f"INSERT INTO ccfr22 ({columns}) VALUES ({placeholders})", tuple(values.values()))
    mysql.connection.commit()
    cur.close()

    return jsonify({'status': '資料輸入成功'}), 201

@ccfr22.route('/api/ccfr22/get', methods=['GET'])
def get_ccfr22():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM ccfr22")
    ccfr22 = cur.fetchall()
    cur.close()
    return jsonify(ccfr22)

@ccfr22.route('/api/ccfr22/<int:id>', methods=['DELETE'])
def delete_ccfr22(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM ccfr22 WHERE id = %s", [id])
    mysql.connection.commit()
    return jsonify({'status': 'ccfr22 刪除成功'}), 200

@ccfr22.route('/api/bd/<int:id>', methods=['PUT'])
def update_bd(id):
    data = request.get_json()
    new_UN = data.get('UN')
    new_FarmerName = data.get('FarmerName')
    new_ContactPhone = data.get('ContactPhone')
    new_Fax = data.get('Fax')
    new_MobilePhone = data.get('MobilePhone')
    new_Address = data.get('Address')
    new_Email = data.get('Email')
    new_TotalCultivationArea = data.get('TotalCultivationArea')
    new_Number = data.get('Number')
    new_LandParcelNumber = data.get('LandParcelNumber')
    new_Area = data.get('Area')
    new_Crop = data.get('Crop')
    new_AreaCode = data.get('AreaCode')
    new_AreaSize = data.get('AreaSize')
    new_CropTypeHarvestPeriodEstimatedYield = data.get('CropTypeHarvestPeriodEstimatedYield')
    new_Notes = data.get('Notes')
    
    if any(value is None for value in [data.get('UN'), data.get('FarmerName'), ...]):
        return jsonify({'error': 'Required data not provided in request'}), 400
    cur = mysql.connection.cursor()
    cur.execute("""
                UPDATE bd SET 
                UN = %s, 
                FarmerName = %s, 
                ContactPhone = %s, 
                Fax = %s, 
                MobilePhone = %s, 
                Address = %s, 
                Email = %s, 
                TotalCultivationArea = %s, 
                Number = %s, 
                LandParcelNumber = %s, 
                Area = %s, 
                Crop = %s, 
                AreaCode = %s, 
                AreaSize = %s, 
                CropTypeHarvestPeriodEstimatedYield = %s, 
                Notes = %s 
                WHERE ID = %s
                """, 
                (new_UN, new_FarmerName, new_ContactPhone, new_Fax, new_MobilePhone, new_Address, new_Email, new_TotalCultivationArea, 
                 new_Number, new_LandParcelNumber, new_Area, new_Crop, new_AreaCode, new_AreaSize, 
                 new_CropTypeHarvestPeriodEstimatedYield, new_Notes, id))
    mysql.connection.commit()
    cur.close()
    return jsonify({'status': 'bd 更新成功'}), 200

@ccfr22.route('/', methods=['GET'])
def home():
    return "Welcome to my API!"

@ccfr22.errorhandler(404)
def resourcenotfound(e):
    return jsonify(error=str(e)), 404

@ccfr22.errorhandler(KeyError)
def handlekeyerror(e):
    return jsonify(error='Key not found in request data'), 400

if __name__ == '__main__':
    with ccfr22.app_context():
        db.create_all()
    ccfr22.run(debug=True)
