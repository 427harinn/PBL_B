FROM python:3.12

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y cron

# Pythonパッケージのインストール
RUN pip install Flask requests

# cronジョブの設定
RUN echo "0 0 1 1 * /usr/local/bin/python /app/test.py" >> /etc/cron.d/my-cron-job

# cronジョブのパーミッション設定
RUN chmod 0644 /etc/cron.d/my-cron-job

# cronサービスを開始するためのスクリプト
COPY start.sh /start.sh
RUN chmod +x /start.sh

# 作業ディレクトリを設定
WORKDIR /app

# 必要なファイルをコンテナにコピー
COPY . /app

# コンテナ起動時にcronを開始
CMD ["/start.sh"]
