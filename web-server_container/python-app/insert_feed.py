import requests
import json
import zipfile
import os
import mysql.connector

# MySQLサーバーの設定
config = {
    'host': 'web-server_container-db-1',
    'user': 'root',
    'password': 'password',
    'database': 'operation',
}
conn = None

# JSONファイルを読み込む
with open('response_data.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

organization_names = set()
feed_data = {}

# feed_id = 0
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
    # feed_id += 1
    # print(f"{feed_id}, {item['feed_name']}")

organization_names = sorted(organization_names)
sorted_feed_data = sorted(feed_data.items(), key=lambda x: x[0])
feed_data = dict(sorted_feed_data)
# print(organization_names, feed_data)
# print(organization_names)
print(feed_data)

agency_id = 0
feed_id = 0
previous_agency = ""
for details in feed_data.values():
    current_agency = details['organization_id']
    print(details)
    if(previous_agency != current_agency):
        agency_id += 1
    previous_agency = current_agency
    for feed in details['feeds']:
        feed_id += 1
        feed_name = feed['feed_name']
        print(f"{feed_id}, {agency_id}, {feed_name}")
        
        conn = None

        try:
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()

            # SQLクエリの作成
            insert_query = f"INSERT INTO Feed (feed_id, feed_name, agency_id, password) VALUES ({feed_id}, '{feed_name}', {agency_id}, default)"

            cursor.execute(insert_query)
            conn.commit()

            print("データ挿入完了！")
        except mysql.connector.Error as err:
            print(f"エラー: {err}")
        finally:
            if conn and conn.is_connected():
                conn.close()
                print("接続が閉じられました。")

# ---------------------------------------------------------------------------------------------------------
'''
# organization_id と feed_id を直接取り出して表示
for details in feed_data.values():
    organization_id = details['organization_id']
    for feed in details['feeds']:
        feed_id = feed['feed_id']
        feed_name = feed['feed_name']
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
            # input("次に行く場合はenterを押せ！")
            try:
                conn = mysql.connector.connect(**config)
                print("接続成功！")
            except mysql.connector.Error as err:
                print(f"エラー: {err}")
            finally:
                if conn and conn.is_connected():
                    conn.close()
                    print("接続が閉じられました。")
        else:
            print(f'Failed to retrieve feed data: {response.status_code}')
            print(response.text)  # エラーメッセージの内容を表示
'''
