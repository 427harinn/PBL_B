from flask import Flask, render_template, request
import os

app = Flask(__name__)

# ホームページ（ユーザーからの入力を待つフォームを表示）
@app.route('/')
def index():
    return render_template('index_catch.html')

# フォーム送信後の処理
@app.route('/display', methods=['POST'])
def display():
    file_name = request.form['file_name']
    folder_path = './extracted_files'
    
    file_path = os.path.join(folder_path, file_name)
    
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            content = file.read()
        return render_template('display.html', file_name=file_name, content=content)
    else:
        return render_template('display.html', file_name=file_name, content=f"ファイル '{file_name}' はフォルダ '{folder_path}' に存在しません。")

if __name__ == '__main__':
    app.run(debug=True)
