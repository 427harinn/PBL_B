import mysql.connector

# MySQLサーバーの設定
config = {
    'host': 'web-server_container-db-1',
    'user': 'root',
    'password': 'password',
    'database': 'operation',
}

conn = None

try:
    conn = mysql.connector.connect(**config)
    print("接続成功！")
except mysql.connector.Error as err:
    print(f"エラー: {err}")
finally:
    if conn and conn.is_connected():
        conn.close()
        print("接続が閉じられました。")
