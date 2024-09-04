import mysql.connector

# MySQLサーバーの設定
config = {
    'host': 'web-server_container-db-1',
    'user': 'root',
    'password': 'password',
    'database': 'operation',
}
conn = None

#---------------- Agencyテーブル ----------------#
try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # SQLクエリの作成
    create_table_query = "CREATE TABLE Agency (agency_id INTEGER NOT NULL, agency_name VARCHAR(8) NOT NULL, PRIMARY KEY(agency_id))"

    cursor.execute(create_table_query)
    conn.commit()

    print("Agencyテーブル作成成功！")

except mysql.connector.Error as err:
    print(f"エラー: {err}")
finally:
    if conn and conn.is_connected():
        conn.close()
        print("接続が閉じられました。\n")

#---------------- Feedテーブル ----------------#
try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # SQLクエリの作成
    create_table_query = "CREATE TABLE Feed (feed_id INTEGER NOT NULL, feed_name VARCHAR(64) NOT NULL, agency_id INTEGER NOT NULL, password VARCHAR(32) DEFAULT 'password' NOT NULL, PRIMARY KEY(feed_id))"

    cursor.execute(create_table_query)
    conn.commit()

    print("Feedテーブル作成成功！")

except mysql.connector.Error as err:
    print(f"エラー: {err}")
finally:
    if conn and conn.is_connected():
        conn.close()
        print("接続が閉じられました。\n")

#---------------- Routeテーブル ----------------#
try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # SQLクエリの作成
    create_table_query = "CREATE TABLE Route (route_id INTEGER NOT NULL, route_name VARCHAR(64) NOT NULL, feed_id INTEGER NOT NULL, PRIMARY KEY(route_id))"

    cursor.execute(create_table_query)
    conn.commit()

    print("Routeテーブル作成成功！")

except mysql.connector.Error as err:
    print(f"エラー: {err}")
finally:
    if conn and conn.is_connected():
        conn.close()
        print("接続が閉じられました。\n")

#---------------- Statusテーブル ----------------#
try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # SQLクエリの作成
    create_table_query = "CREATE TABLE Status (status BOOLEAN DEFAULT TRUE NOT NULL, date DATE NOT NULL, route_id INTEGER NOT NULL, comment TEXT)"

    cursor.execute(create_table_query)
    conn.commit()

    print("Statusテーブル作成成功！")

except mysql.connector.Error as err:
    print(f"エラー: {err}")
finally:
    if conn and conn.is_connected():
        conn.close()
        print("接続が閉じられました。\n")