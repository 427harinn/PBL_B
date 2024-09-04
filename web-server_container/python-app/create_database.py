import mysql.connector

# MySQLサーバーの設定
config = {
    'host': 'web-server_container-db-1',
    'user': 'root',
    'password': 'password',
}
conn = None

try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # SQLクエリの作成
    create_database_query = "CREATE DATABASE operation"

    cursor.execute(create_database_query)
    conn.commit()

    print("データベース作成成功！")

except mysql.connector.Error as err:
    print(f"エラー: {err}")
finally:
    if conn and conn.is_connected():
        conn.close()
        print("接続が閉じられました。\n")
