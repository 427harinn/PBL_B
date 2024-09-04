#!/bin/bash

# cronをバックグラウンドで実行
cron

# 毎年1月1日に実行するcronジョブを設定
echo "0 0 1 1 * /usr/local/bin/python /app/insert_agency.py" >> /etc/cron.d/my-cron-job
echo "0 0 1 1 * /usr/local/bin/python /app/insert_feed.py" >> /etc/cron.d/my-cron-job
echo "0 0 1 1 * /usr/local/bin/python /app/insert_route.py" >> /etc/cron.d/my-cron-job
# パーミッションの設定
chmod 0644 /etc/cron.d/my-cron-job

# メインプロセスを開始（例: Flaskアプリケーションを起動する）
#python read_web.py

