from flask import Flask, render_template, request
import requests
import json
import zipfile
import os
import csv

app = Flask(__name__)

def process_extracted_files_for_routes(extracted_folder):
    #ルート選択画面の処理　パスワードを付けたりしたい場合はここで処理を書くといいかも
    routes_file_path = None
    route_long_names = []

    # 解凍されたフォルダ内を探索し、routes.txtファイルを探す
    for root, dirs, files in os.walk(extracted_folder):
        for file in files:
            if file == 'routes.txt':
                routes_file_path = os.path.join(root, file)
                break

    if routes_file_path:
        print(f"routes.txt found: {routes_file_path}")
        # routes.txt の内容を読み込み、route_long_nameをリストに追加
        with open(routes_file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                route_long_names.append(row['route_long_name'])
    else:
        print("routes.txt file not found.")

    return route_long_names

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

        # 解凍後の処理（route_long_nameをリストで取得）
        route_long_names = process_extracted_files_for_routes(extracted_folder)

        if route_long_names:
            return render_template('select_route.html', route_long_names=route_long_names)
        else:
            return "routes.txt ファイルが見つかりませんでした。"
        
    else:
        return f'Failed to retrieve feed data: {response.status_code}', 400

@app.route('/process_route', methods=['POST'])
def process_route():
    selected_route = request.form['route_long_name']
    operation_status = request.form['operation_status']
    
    # 選択されたルートと運行ステータスに基づいて次の処理を行う
    # ここに処理内容を追加します
    return f'Selected route_long_name: {selected_route}, Operation status: {operation_status}'


if __name__ == '__main__':
    app.run(debug=True)
