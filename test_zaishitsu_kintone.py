import pandas as pd
from datetime import datetime, date
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
appno = 1212## 取得したいアプリのアプリNo
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


file_path1 = r"C:\Users\DSP189\Desktop\test\2024年.xlsx"
## body作成

    # CSVファイル読み込み

    #辞書型を作る：
df = pd.read_excel(file_path1, sheet_name="2024年")
    ## サイボウズ用にデータを整形に 
     
print("b")          
gia_tri_V93 = df.iloc[91, 21] #V93 : 1973
print(gia_tri_V93)
koujou= df.iloc[0, 18]
print(koujou)
if koujou== "ＵＰ本社工場":
    koujou= "本社工場"
print(koujou)
gia_tri_A93 = df.iloc[91, 0]
p = pd.to_datetime(gia_tri_A93).date()
p1 = p.isoformat()
print(p)
body_fields = {
#1科目 = １即 "key-value":
        #日付
        "日付":{"value":p1},
        
## 生産枚数
        "生産枚数":{"value":gia_tri_V93},
        
## 発送日コード
        "工場":{"value":koujou}
        
        }


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