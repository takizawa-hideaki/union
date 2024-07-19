import pandas as pd
from datetime import datetime, date, timedelta
import os
import base64
import urllib.request
import json
import csv
factorys = ["18","48","63","78","93","108","123","138","172","187","202","234","249","266","281","296","314"]
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
line_path = r"C:\Users\DSP189\Desktop\line.txt"

def increase_line(line):
    return line + 1
def increase_line1(line):
    return line + 2

def save_line(line):
    with open(line_path, "w") as file:
        file.write(str(line))
def read_value():
    try:
        with open(line_path, "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0
line = read_value() # row Excel -2

file_path1 = r"\\192.168.160.6\Union-FileSV\共通ファイル_Ⅱ\営業本部\システム\ユニオン販売フォルダ\受注状況表\2024年.xlsx"
## body作成

    # CSVファイル読み込み

    #辞書型を作る：
df = pd.read_excel(file_path1, sheet_name="2024年")
    ## サイボウズ用にデータを整形に 

yesterday = date.today() - timedelta(days=1)
today = date.today().month
if today != yesterday.month:
    line = increase_line1(line) # increase_row1を呼び込み、line　2個増える
    save_line(line)
create_date = df.iloc[line, 0] # row Excel -2
p = pd.to_datetime(create_date).date()
if yesterday == p: 
    p1 = p.isoformat()
    print(p1)             
    for factory in factorys:
    #print(int(factory))
        koujou= df.iloc[0, int(factory)] 
        print(koujou)
        if koujou== "ＵＰ本社工場":
            koujou= "本社工場"
            honsha = df.iloc[line, 21] + df.iloc[line,36] #V93 : 1973
            body_fields = {
                "日付":{"value":p1},
                "生産枚数":{"value":honsha},
                "工場":{"value":koujou}    
                }
        elif koujou== "ＩＮＳ加工工場":
            koujou= "㈱INステンレス加工センター"
            ins = df.iloc[line, 51]
            body_fields = {
            "日付":{"value":p1},
            "生産枚数":{"value":ins},
            "工場":{"value":koujou}    
            }
    
        elif koujou== "藤精工":
            koujou= "㈲藤精工"
            fuji = df.iloc[line, 66]
            body_fields = {
            "日付":{"value":p1},
            "生産枚数":{"value":fuji},
            "工場":{"value":koujou}    
            }
        elif koujou== "サンテック":
            koujou= "㈲サンテック"
            santec = df.iloc[line, 81]
            body_fields = {
            "日付":{"value":p1},
            "生産枚数":{"value":santec},
            "工場":{"value":koujou}    
            }
        elif koujou== "エムケイ精工":
            koujou= "㈲エムケイ精工"
            mk = df.iloc[line, 96]
            body_fields = {
            "日付":{"value":p1},
            "生産枚数":{"value":mk},
            "工場":{"value":koujou}    
            }
        elif koujou== "渡辺製作所":
            koujou= "㈱渡辺製作所"
            watanabe = df.iloc[line, 111]
            body_fields = {
            "日付":{"value":p1},
            "生産枚数":{"value":watanabe},
            "工場":{"value":koujou}    
            }
        elif koujou== "ユーピーエム":
            koujou= "㈲ユーピーエム"
            upm = df.iloc[line, 126]
            body_fields = {
            "日付":{"value":p1},
            "生産枚数":{"value":upm},
            "工場":{"value":koujou}    
            }
        elif koujou== "UP尾道工場":
            koujou= "尾道工場"
            onomichi = df.iloc[line, 142] + df.iloc[line, 158]
            body_fields = {
            "日付":{"value":p1},
            "生産枚数":{"value":onomichi},
            "工場":{"value":koujou}    
            }
        elif koujou== "UP厚木工場":
            koujou= "厚木工場"
            atsugi = df.iloc[line, 175]
            body_fields = {
            "日付":{"value":p1},
            "生産枚数":{"value":atsugi},
            "工場":{"value":koujou}    
            }
        elif koujou== "エムテーエス":
            koujou= "㈲エムテーエス"
            mts = df.iloc[line, 190]
            body_fields = {
            "日付":{"value":p1},
            "生産枚数":{"value":mts},
            "工場":{"value":koujou}    
            }
        elif koujou== "ＡＵＫプレート":
            koujou= "ＡＵＫプレート㈱"
            auk = df.iloc[line, 205] + df.iloc[line, 220]
            body_fields = {
            "日付":{"value":p1},
            "生産枚数":{"value":auk},
            "工場":{"value":koujou}    
            }
        elif koujou== "峰岸商会":
            koujou= "株式会社峰岸商会"
            mine = df.iloc[line, 237]
            body_fields = {
            "日付":{"value":p1},
            "生産枚数":{"value":mine},
            "工場":{"value":koujou}    
            }
        elif koujou== "メカニックメタル":
            koujou= "㈱メカニックメタル"
            mm = df.iloc[line, 252]
            body_fields = {
            "日付":{"value":p1},
            "生産枚数":{"value":mm},
            "工場":{"value":koujou}    
            }
        elif koujou== "鈴木鋼管工業":
            koujou= "㈲鈴木鋼管工業"
            suzuki = df.iloc[line, 269]
            body_fields = {
            "日付":{"value":p1},
            "生産枚数":{"value":suzuki},
            "工場":{"value":koujou}    
            }
        elif koujou== "UP小牧工場":
            koujou= "小牧工場"
            komaki = df.iloc[line, 284]
            body_fields = {
            "日付":{"value":p1},
            "生産枚数":{"value":komaki},
            "工場":{"value":koujou}    
            }
        elif koujou== "UP上田工場":
            koujou= "上田工場"
            ueda = df.iloc[line, 300]
            body_fields = {
            "日付":{"value":p1},
            "生産枚数":{"value":ueda},
            "工場":{"value":koujou}    
            }
        elif koujou== "UP千曲工場":
            koujou= "千曲工場"
            chikuma = df.iloc[line, 317]
            body_fields = {
            "日付":{"value":p1},
            "生産枚数":{"value":chikuma},
            "工場":{"value":koujou}    
            }
        else: exit()






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
    line = increase_line(line)# increase_rowを呼び込み、row　1個増える
     #新値の rowを　row.txtに保存
    save_line(line)
else :
    exit()