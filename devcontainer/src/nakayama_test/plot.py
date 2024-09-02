import pandas as pd
import folium
import webbrowser
import os

# CSVファイルを読み込み、欠損値を削除
# df =pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")
# スクリプトのディレクトリを取得
script_dir = os.path.dirname(os.path.abspath(__file__))
# ファイルパスを構築
file_path = os.path.join(script_dir, "shapes.csv")
df = pd.read_csv(file_path)
df.dropna(inplace=True)

#サイズを指定する
folium_figure = folium.Figure(width=1500, height=700)

# 初期表示の中心の座標を指定して地図を作成する。
center_lat = 33.88
center_lon = 130.67
folium_map = folium.Map([center_lat,center_lon],
zoom_start=13).add_to(folium_figure)

# trainデータの300行目までマーカーを作成する。
# for i in range(300):
#     folium.Marker(location=[df.loc[i, "lat"],
#     df.loc[i, "lon"]]).add_to(folium_map)
# # folium_map

for i in range(min(300, len(df))):  # データの長さが300未満の場合にも対応
    lat = df.loc[i, "shape_pt_lat"]
    lon = df.loc[i, "shape_pt_lon"]
    folium.Marker(location=[lat, lon],
                  popup=f"ID: {df.loc[i, 'shape_id']} Seq: {df.loc[i, 'shape_pt_sequence']}").add_to(folium_map)


# 一時的なHTMLファイルとして保存
map_path = "temp_map.html"
folium_map.save(map_path)

# ブラウザで自動的に開く
# webbrowser.open('file://' + os.path.realpath(map_path))

input("表示を続けるには Enter キーを押してください...")

# 終了後、ファイルを削除
os.remove(map_path)
