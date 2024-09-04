import requests
import json
import zipfile
import os
import mysql.connector

#---------------- MySQLサーバーの設定 ----------------#
config = {
    'host': 'web-server_container-db-1',
    'user': 'root',
    'password': 'password',
    'database': 'operation',
}
conn = None
#----------------  ----------------#

#---------------- gtfsを読み込む ----------------#
# JSONファイルを読み込む
with open('response_data.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

organization_names = set()
feed_data = {}

# データの抽出と整形
for item in data['body']:
    organization_name = item['organization_name']
    organization_id = item['organization_id']
    organization_names.add(organization_name)
    if organization_name not in feed_data:
        feed_data[organization_name] = {
            'organization_id': organization_id,
            'feeds': []
        }
    feed_data[organization_name]['feeds'].append({
        'feed_id': item['feed_id'],
        'feed_name': item['feed_name']
    })

# organization_namesのソート
organization_names = sorted(organization_names)
sorted_feed_data = sorted(feed_data.items(), key=lambda x: x[0])
feed_data = dict(sorted_feed_data)
#----------------  ----------------#

#---------------- データ初期化 ----------------#
conn = None
try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # SQLクエリの作成
    truncate_query = "TRUNCATE TABLE Route"


    cursor.execute(truncate_query)
    conn.commit()

    print("データ初期化完了！")
except mysql.connector.Error as err:
    print(f"エラー: {err}")
finally:
    if conn and conn.is_connected():
        conn.close()
        print("接続が閉じられました。\n\n")
#----------------  ----------------#

#---------------- DBに登録 ----------------#
route_id = 0
feed_num = 0
# フィードデータの処理
for details in feed_data.values():
    organization_id = details['organization_id']
    for feed in details['feeds']:
        feed_id = feed['feed_id']
        feed_name = feed['feed_name']
        feed_num += 1
        print(feed_id, feed_name)

        # ベースURL
        base_url = 'https://api.gtfs-data.jp/v2'

        # フィード情報を取得するエンドポイント
        feed_endpoint = f'/organizations/{organization_id}/feeds/{feed_id}/files/feed.zip'

        # フルURL
        feed_url = base_url + feed_endpoint

        # APIキー（必要な場合）
        api_key = 'YOUR_API_KEY'

        # リクエストヘッダー
        headers = {
            'Authorization': f'Bearer {api_key}'
        }

        # フィード情報を取得するGETリクエストを送信
        response = requests.get(feed_url, headers=headers)

        # ステータスコードの確認
        print(response.status_code)

        if response.status_code == 200:
            # ZIPファイルをバイナリとして保存
            zip_filename = 'feed.zip'
            with open(zip_filename, 'wb') as file:
                file.write(response.content)
            print("フィード情報がfeed.zipに書き込まれました。")
            
            # ZIPファイルを解凍
            with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
                zip_ref.extractall('extracted_files')
            print("ZIPファイルが解凍されました。")

            # routes.txtからroute_idを抽出してMySQLに格納
            routes_file_path = 'extracted_files/routes.txt'
            if os.path.exists(routes_file_path):
                try:
                    conn = mysql.connector.connect(**config)
                    cursor = conn.cursor()

                    # routes.txtを読み込んでroute_idを挿入
                    with open(routes_file_path, 'r', encoding='utf-8') as routes_file:
                        next(routes_file)  # ヘッダーをスキップ
                        for line in routes_file:
                            fields = line.strip().split(',')
                            route_long_name = fields[3]  # 最初のフィールドがroute_id

                            # route_idの挿入クエリ
                            route_id += 1
                            # print(f"{route_id}, {route_long_name}, {feed_num}")
                            insert_query = f"INSERT INTO Route (route_id, route_name, feed_id) VALUES ({route_id}, '{route_long_name}', {feed_num})"
                            cursor.execute(insert_query)

                    # データベースへの変更をコミット
                    conn.commit()
                    print("routes.txtのデータがデータベースに挿入されました。")

                except mysql.connector.Error as err:
                    print(f"エラー: {err}")

                finally:
                    # MySQL接続のクローズ
                    if conn and conn.is_connected():
                        conn.close()
                        print("接続が閉じられました。\n")
            else:
                print(f"{routes_file_path} が見つかりませんでした。")

        else:
            print(f'Failed to retrieve feed data: {response.status_code}')
            print(response.text)  # エラーメッセージの内容を表示
#----------------  ----------------#
