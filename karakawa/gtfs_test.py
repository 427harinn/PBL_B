import requests
import json
import zipfile
import os

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

