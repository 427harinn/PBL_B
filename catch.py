import os

def display_file_content(folder_path, file_name):
    # フォルダとファイルのパスを結合
    file_path = os.path.join(folder_path, file_name)
    
    # ファイルが存在するか確認
    if os.path.isfile(file_path):
        # ファイルを開いて内容を表示
        with open(file_path, 'r') as file:
            content = file.read()
            print(content)
    else:
        print(f"ファイル '{file_name}' はフォルダ '{folder_path}' に存在しません。")

# 使用例
folder_path = './extracted_files'                  # フォルダのパスを指定
file_name = input("ファイル名を入力してください: ")     # 読み込みたいファイル名を指定
display_file_content(folder_path, file_name)
