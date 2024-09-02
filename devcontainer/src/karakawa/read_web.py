from flask import Flask, render_template, request, send_file
import requests
import json
import zipfile
import os

app = Flask(__name__)

# ホームページ（ユーザーからの入力を待つフォームを表示）
@app.route('/')
def index():
    # JSONファイルを読み込んで、organization_nameのリストを取得
    with open('response_data.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        # organization_nameのリストをセットに変換して重複を削除
        organization_names = list(set(item['organization_name'] for item in data['body']))
        # アルファベット順にソート
        organization_names.sort()
    
    return render_template('index_read.html', organization_names=organization_names)

# フォーム送信後の処理
@app.route('/get_feed', methods=['POST'])
def get_feed():
    target_organization_name = request.form['organization_name']
    
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
            print(f"Selected organization_id: {organization_id}, feed_id: {feed_id}")
            break

    if organization_id and feed_id:
        # ベースURL
        base_url = 'https://api.gtfs-data.jp/v2'
        feed_endpoint = f'/organizations/{organization_id}/feeds/{feed_id}/files/feed.zip'
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
            # karakawaフォルダにファイルを保存するパスを指定
            save_folder = 'karakawa'
            os.makedirs(save_folder, exist_ok=True)
            zip_filename = os.path.join(save_folder, 'feed.zip')

            with open(zip_filename, 'wb') as file:
                file.write(response.content)
            
            # ZIPファイルを解凍
            with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
                zip_ref.extractall(os.path.join(save_folder, 'extracted_files'))

            return send_file(zip_filename, as_attachment=True)
        else:
            return f'Failed to retrieve feed data: {response.status_code}', 400

    else:
        return f'No match found for organization_name: {target_organization_name}', 404

if __name__ == '__main__':
    app.run(debug=True)
