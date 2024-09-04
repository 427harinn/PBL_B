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
#----------------  ----------------#

#---------------- gtfs取得 ----------------#
# ベースURL
base_url = 'https://api.gtfs-data.jp/v2'

# フィード情報を取得するエンドポイント
feed_endpoint = '/feeds'

# クエリパラメータ
params = {
    'pref': '40'  # 特定のフィードIDに変更
}

# フルURL
feed_url = base_url + feed_endpoint

# APIキー（必要な場合）
api_key = 'YOUR_API_KEY'

# リクエストヘッダー
headers = {
    'Authorization': f'Bearer {api_key}'
}

# フィード情報を取得するGETリクエストを送信
response = requests.get(feed_url, headers=headers, params=params)

# ステータスコードの確認
print(response.status_code)

if response.status_code == 200:
    try:
        feed_data = response.json()
        # フィード情報をファイルに書き込む
        with open('response_data.json', 'w', encoding='utf-8') as json_file:
            json.dump(feed_data, json_file, ensure_ascii=False, indent=4)
        print("フィード情報がresponse_data.jsonに書き込まれました。")
    except requests.exceptions.JSONDecodeError:
        print("レスポンスはJSONではありません。")
else:
    print(f'Failed to retrieve feed data: {response.status_code}')
#----------------  ----------------#

#---------------- gtfsを読み込む ----------------#
# JSONファイルを読み込む
with open('response_data.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

organization_names = set()
feed_data = {}

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

organization_names = sorted(organization_names)    
# print(organization_names, feed_data)
# print(organization_names)
# print(feed_data)
#----------------  ----------------#

#---------------- データ初期化 ----------------#
conn = None
try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # SQLクエリの作成
    truncate_query = "TRUNCATE TABLE Agency"


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
agency_id = 0
for item in organization_names:
    agency_id += 1
    print(f"{agency_id}, {item}")
    conn = None

    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # SQLクエリの作成
        insert_query = f"INSERT INTO Agency (agency_id, agency_name) VALUES ({agency_id}, '{item}')"


        cursor.execute(insert_query)
        conn.commit()

        print("データ挿入完了！")
    except mysql.connector.Error as err:
        print(f"エラー: {err}")
    finally:
        if conn and conn.is_connected():
            conn.close()
            print("接続が閉じられました。\n")
#----------------  ----------------#
