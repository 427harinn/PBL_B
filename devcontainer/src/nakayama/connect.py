import mysql.connector

# MySQLサーバーに接続
conn = mysql.connector.connect(
    host='mysql',  # コンテナ名
    user='root',  # 使用するユーザー名
    password='password',  # パスワード
    database='operation'  # データベース名
)

# 接続確認
if conn.is_connected():
    print('Connected to MySQL database')
else:
    print('Failed to connect')
