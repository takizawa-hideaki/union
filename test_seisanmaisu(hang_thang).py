import pandas as pd
from datetime import datetime, date, timedelta
import os
import base64
import urllib.request
import json
import csv
file_path = r"C:\Users\DSP189\Desktop\user1.txt"
with open(file_path, "r") as file:
    lines = file.readlines()
    username = lines[0].strip()  # Line1: username
    password = lines[1].strip() # Line2: password

#kintone 接続
DOMAIN = 'union-plate'## kintoneのドメイン
LOGIN = f"{username}"## ログイン名
PASS = f"{password}"## パスワード
appno = 1205## 取得したいアプリのアプリNo
uri = "https://" + DOMAIN + ".cybozu.com/k/v1/record.json"
## パスワード認証　の部分
## LOGIN と PASSを「：」でつないでbase64でエンコード
AUTH = base64.b64encode((LOGIN + ":" + PASS).encode())
## ヘッダ作成
headers = {
    "Host":DOMAIN + ".cybozu.com:443",
    "X-Cybozu-Authorization":AUTH,
    "Content-Type": "application/json",
    "Content-Encoding": "deflate" ,
}
line_path = r"C:\Users\DSP189\Desktop\line1.txt"

from datetime import datetime

# Khởi tạo ngày bắt đầu và ngày kết thúc
start_date = datetime(2021, 5, 1)
end_date = datetime(2023, 4, 30)

# Biến tạm để lưu trữ ngày hiện tại trong vòng lặp
current_date = start_date

# Đọc các giá trị lines từ file 'line1.txt'
lines_dict = {}
with open(line_path, 'r', encoding='utf-8') as file:
    for line in file:
        lines_dict[current_date.date().isoformat()] = line.strip()
        # Chuyển sang ngày đầu tiên của tháng tiếp theo
        next_month = current_date.month + 1 if current_date.month < 12 else 1
        next_year = current_date.year if current_date.month < 12 else current_date.year + 1
        current_date = datetime(next_year, next_month, 1)

# Khởi tạo lại biến tạm để lưu trữ ngày hiện tại trong vòng lặp
current_date = start_date

# Tạo danh sách các dòng dữ liệu

while current_date <= end_date:
    # Trích xuất phần ngày tháng năm từ current_date bằng phương thức isoformat()
    a = current_date.date().isoformat()

    # Lấy giá trị lines tương ứng từ lines_dict
    lines = lines_dict.get(a, 0)

    # Tạo từ điển body_fields chứa dữ liệu của mỗi tháng
    body_fields = {
        "日付": {"value": a},
        "生産枚数": {"value": int(lines)},
        "工場": {"value": "㈲鈴木鋼管工業"}
    }



    # Di chuyển đến ngày đầu tiên của tháng tiếp theo
    next_month = current_date.month + 1 if current_date.month < 12 else 1
    next_year = current_date.year if current_date.month < 12 else current_date.year + 1
    current_date = datetime(next_year, next_month, 1)


            
    # Di chuyển đến ngày đầu tiên của tháng tiếp theo
            
    body_record = {"record": body_fields}#grouped_body_fieldsからrecord作成
    body = {"app": appno, **body_record}
    print (body)  
        # HTTP　リクエスト作成
    req = urllib.request.Request(
            url=uri,
            data=json.dumps(body).encode(),# "body" :JSONに変換
            headers=headers,
            method="POST"
            )
    #kintoneにリクエストする
    try:
        response = urllib.request.urlopen(req)
        res_dict = json.load(response)
        print(res_dict)  # kintone から帰還表示
    except urllib.error.URLError as e:
        if hasattr(e, "reason"):
            print("Failed to reach the server:", e.reason)
        elif hasattr(e, 'code'):
            print('The server couldn\'t fulfill the request.', e.code)
        input("k:")
      
    