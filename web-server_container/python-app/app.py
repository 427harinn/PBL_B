from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# データベース接続設定
def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="youruser",  # ここにMySQLのユーザー名
        password="yourpassword",  # ここにMySQLのパスワード
        database="operation"  # 使用するデータベース名
    )
    return conn

@app.route('/')
def index():
    return "a"
    return render_template('index.html')

@app.route('/get_feeds', methods=['GET'])
def get_feeds():
    agency_name = request.args.get('agency_name')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT f.feed_id, f.feed_name 
        FROM Feed f
        JOIN Agency a ON f.agency_id = a.agency_id
        WHERE a.agency_name = %s
    """, (agency_name,))
    feeds = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(feeds)

@app.route('/get_routes', methods=['GET'])
def get_routes():
    feed_id = request.args.get('feed_id')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT r.route_id, r.route_name 
        FROM Route r
        WHERE r.feed_id = %s
    """, (feed_id,))
    routes = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(routes)

@app.route('/save_route_status', methods=['POST'])
def save_route_status():
    data = request.json
    selected_date = data['date']
    routes = data['routes']

    conn = get_db_connection()
    cursor = conn.cursor()

    for route in routes:
        cursor.execute("""
            INSERT INTO Status (status, date, route_id)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE
            status = VALUES(status),
            date = VALUES(date)
        """, (route['status'], selected_date, route['route_id']))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
