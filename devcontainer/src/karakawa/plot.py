import pandas as pd
import folium
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

# テキストファイルからデータを読み込む
file_path = os.path.join(folder_path, file_name)
df = pd.read_csv(file_path)

# サイズを指定する
folium_figure = folium.Figure(width=1500, height=700)

# 初期表示の中心の座標を指定して地図を作成する
center_lat = df['stop_lat'].mean()
center_lon = df['stop_lon'].mean()
folium_map = folium.Map([center_lat, center_lon], zoom_start=12).add_to(folium_figure)

# stop_idが300未満の場合に対応
for i in range(min(300, len(df))):
    folium.Marker(
        location=[df.loc[i, "stop_lat"], df.loc[i, "stop_lon"]],
        popup=df.loc[i, "stop_name"]
    ).add_to(folium_map)

# 地図を表示する
folium_map

# 地図を保存して、ブラウザで確認できるようにする
folium_map.save('map.html')
