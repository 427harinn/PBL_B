import requests
import json
import zipfile
import os

# ユーザーからの入力を待つ
target_organization_name = input("Enter the organization name: ")

# JSONファイルを読み込む
with open('response_data.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# target_organization_name に一致するデータを検索
organization_id = None
feed_id = None

for item in data['body']:
    if item['organization_name'] == target_organization_name:
        organization_id = item['organization_id']
        feed_id = item['feed_id']
        break

if organization_id and feed_id:
    print(f"Organization ID: {organization_id}")
    print(f"Feed ID: {feed_id}")
else:
    print(f"No match found for organization_name: {target_organization_name}")

# ---------------------------------------------------------------------------------------------------------

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
else:
    print(f'Failed to retrieve feed data: {response.status_code}')
    print(response.text)  # エラーメッセージの内容を表示
