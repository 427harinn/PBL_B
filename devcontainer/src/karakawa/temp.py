from flask import Flask, render_template, request
import requests
import json
import zipfile
import os

app = Flask(__name__)

@app.route('/')
def index():
    # JSONファイルを読み込んで、organization_nameのリストとfeed_dataを取得
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
    
    return render_template('index_read.html', organization_names=organization_names, feed_data=feed_data)

@app.route('/get_feed', methods=['POST'])
def get_feed():
    target_organization_id = request.form['organization_id']
    target_feed_id = request.form['feed_name']

    # ベースURL
    base_url = 'https://api.gtfs-data.jp/v2'
    feed_endpoint = f'/organizations/{target_organization_id}/feeds/{target_feed_id}/files/feed.zip'
    feed_url = base_url + feed_endpoint

    # APIキー
    api_key = 'YOUR_API_KEY'

    # リクエストヘッダー
    headers = {
        'Authorization': f'Bearer {api_key}'
    }

    # 最終的なURLを表示
    print(f"Final Request URL: {feed_url}")

    # フィード情報を取得するGETリクエストを送信
    response = requests.get(feed_url, headers=headers)

    if response.status_code == 200:
        # 現在の作業ディレクトリにファイルを保存するパスを指定
        extracted_folder = 'extracted_files'
        os.makedirs(extracted_folder, exist_ok=True)

        # extracted_files フォルダの中身を削除
        for root, dirs, files in os.walk(extracted_folder):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))

        # ZIPファイルの保存
        zip_filename = 'feed.zip'
        with open(zip_filename, 'wb') as file:
            file.write(response.content)
        
        # ZIPファイルを解凍
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall(extracted_folder)

        # 解凍後の処理をここに記述（必要に応じて）

        return "フィードファイルが正常に解凍され、内部処理が完了しました。"
    else:
        return f'Failed to retrieve feed data: {response.status_code}', 400

if __name__ == '__main__':
    app.run(debug=True)
