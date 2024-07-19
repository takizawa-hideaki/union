### ver 0.0.1 : log file 追加-----
###ver 0.0.2 : もしデータがない場合はｃｓｖファイル、logファイル出力しない----
###ver 0.0.3 :取込ｃｓｖファイル、logファイル月事に別れる----
###ver 0.0.4: cybozuにlogファイルのデータを自動コメント機能追加


import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import os
import base64
import urllib.request
import json
import csv
from selenium.webdriver import Edge
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
database_uri = 'postgresql://unionplate:etalpnoinu@192.168.160.83:5432/union_hanbai'
engine = create_engine(database_uri)

query = ("""
select 

--１．営業本部行き先　　送付先マスタから取得し各部名に変換

	CASE sdc.sender_code WHEN 11 THEN '営業1部'
						 WHEN 12 THEN '営業2部'
						 WHEN 13 THEN '営業3部'
	END as 営業本部行き先,

--２．バーコード　　受注№上下と明細№を結合

	jh.juchu_no_upper || lpad(cast(jh.juchu_no_lower as varchar),6, '0') || lpad(cast(jd.juchu_detail_no as varchar),2, '0') as バーコード,

--３．発送日コード　受注明細から取得し'/'を''に置き換え
	replace(jd.shuka_date, '/', '' ) as 発送日コード,

--４．出荷日　　受注明細から取得

	jd.shuka_date as 出荷日,

--５．特記事項[配達品]　　配達品なら1

	CASE jh.express_code WHEN 4 THEN 1
								ELSE 0
	END as "特記事項[配達品]",

--６．特記事項[仕入れ品]　　全て仕入手配品なので1

	1 as "特記事項[仕入れ品]",

--７．特記事項[仕入れ品]　　全て0

	0 as "特記事項[工場差戻し]",

--８．特記事項[FAX＆製品添付]　　出荷備考のどれかが１８５：ミルシート　ＦＡＸ＆添付なら1

	CASE WHEN jh.shuka_biko_code1 = 185 THEN 1
		 WHEN jh.shuka_biko_code2 = 185 THEN 1
		 WHEN jh.shuka_biko_code3 = 185 THEN 1
										ELSE 0
	END as "特記事項[FAX＆製品添付]",

--９．特記事項[メール＆添付]　　出荷備考のどれかが２６３：ミルシート　メール＆添付なら1

	CASE WHEN jh.shuka_biko_code1 = 263 THEN 1
		 WHEN jh.shuka_biko_code2 = 263 THEN 1
		 WHEN jh.shuka_biko_code3 = 263 THEN 1
										ELSE 0
	END as "特記事項[メール＆添付]",

--１０．特記事項[熱処理検査表あり]

	CASE WHEN jh.sagyo_biko_code1 in ('217','226','215') THEN 1 --　作業備考のどれかが２１７：２２６：２１５：熱処理検査表関連なら1
		 WHEN jh.sagyo_biko_code2 in ('217','226','215') THEN 1
		 WHEN jh.sagyo_biko_code3 in ('217','226','215') THEN 1
		 WHEN jh.shuka_biko_code1 in ('184','183') THEN 1 --　出荷備考のどれかが１８４：１８３：熱処理検査表関連なら1
		 WHEN jh.shuka_biko_code2 in ('184','183') THEN 1
		 WHEN jh.shuka_biko_code3 in ('184','183') THEN 1
												   ELSE 0
	END as "特記事項[熱処理検査表あり]",

--１１．工場　　工場コードから工場名に変換

	CASE jd.factory_office_code WHEN 100 THEN '本社工場'
								WHEN 101 THEN '本社工場'
								WHEN 500 THEN 'INS'
								WHEN 510 THEN '藤精工'
								WHEN 520 THEN '尾道工場'
								WHEN 530 THEN 'サンテック'
								WHEN 540 THEN 'MK精工'
								WHEN 550 THEN '渡辺製作所'
								WHEN 560 THEN 'UPM'
								WHEN 570 THEN '尾道工場'
								WHEN 580 THEN '厚木工場'
								WHEN 590 THEN 'MTS'
								WHEN 600 THEN 'AUK'
								WHEN 601 THEN 'AUK'
								WHEN 620 THEN '峰岸加工工場'
								WHEN 630 THEN 'MM'
								WHEN 640 THEN '鈴木鋼管'
								WHEN 650 THEN '小牧工場'
								WHEN 670 THEN '上田工場'
								WHEN 680 THEN '千曲工場'
	END as 工場,

--１２．注番

	lpad(cast(jh.juchu_no_lower as varchar),6, '0') as 注番,

--１３．枝番　

	LPAD (cast(jd.juchu_detail_no as character varying), 2, '0') as 枝番,

--１４． 工場コード 
	
		 concat(
				jd.factory_corporation_code,'',
				CASE jd.factory_office_code WHEN 101 then '100'
				else jd.factory_office_code
				end) as 工場コード,


--１５．作業者備考

	--jh.create_staff as 作業者備考,

--１６. ミルシート処理
							 --    '製品添付'
	CASE WHEN jh.shuka_biko_code1 in('185','263', '176','183','184') THEN '製品添付'
		 WHEN jh.shuka_biko_code2 in('185','263', '176','183','184') THEN '製品添付'
		 WHEN jh.shuka_biko_code3 in('185','263', '176','183','184') THEN '製品添付'
							 --　'営業本部処理'
		 --WHEN jh.sagyo_biko_code1 in ('217','226','215') THEN '営業本部処理'
		 --WHEN jh.sagyo_biko_code2 in ('217','226','215') THEN '営業本部処理'
		 --WHEN jh.sagyo_biko_code3 in ('217','226','215') THEN '営業本部処理'

		 --WHEN jh.shuka_biko_code1 in ('184','183') THEN '営業本部処理' 
		 --WHEN jh.shuka_biko_code2 in ('184','183') THEN '営業本部処理'
		 --WHEN jh.shuka_biko_code3 in ('184','183') THEN '営業本部処理'
													
	ELSE '営業本部処理'
	END as ミルシート処理,

--１７．ミルシート得意先コードを左ゼロ埋めで６桁に修正
	LPAD(cast(jh.tokuisaki_code as varchar),6,'0') as ミルシート得意先コード,

--１８．製品仕様
	jd.zaishitsu_name || ' ' || jd.size_a || ' * ' || jd.size_b || ' * ' || jd.size_c  || ' = ' || jd.suryo as 製品仕様

from offc_trn_juchu_head as jh
join offc_mst_sender_code as sdc --　送付元コードマスタを内部結合（得意先コード）
on jh.tokuisaki_code = sdc.tokuisaki_code
and sdc.delete_flag != 1
--join offc_mst_sender as sd --　送付元マスタを内部結合（送付元コード）
--on sdc.sender_code = sd.sender_code

         
join offc_trn_juchu_details as jd --　受注明細を内部結合（受注№上下）
on jh.juchu_no_upper = jd.juchu_no_upper
and jh.juchu_no_lower = jd.juchu_no_lower
and jd.delete_flag != 1
and jd.detail_gyomu_cf='1011'

where jh.delete_flag != 1

and (jh.sagyo_biko_code1 = '145' or jh.sagyo_biko_code2 = '145' or jh.sagyo_biko_code3 = '145') --　作業備考のどれかが１４５：仕入手配品

and (
	   jh.sagyo_biko_code1 = '44' or jh.sagyo_biko_code2 = '44' or jh.sagyo_biko_code3 = '44' --　作業備考のどれかが４４：ミルシート　ＦＡＸ
	or jh.sagyo_biko_code1 = '176' or jh.sagyo_biko_code2 = '176' or jh.sagyo_biko_code3 = '176' --　作業備考のどれかが１７６：熱処理検査表ＦＡＸ
	or jh.sagyo_biko_code1 = '200' or jh.sagyo_biko_code2 = '200' or jh.sagyo_biko_code3 = '200' --　作業備考のどれかが２００：ミルシート　メール送信
	or jh.sagyo_biko_code1 = '217' or jh.sagyo_biko_code2 = '217' or jh.sagyo_biko_code3 = '217' --　作業備考のどれかが２１７：ミルシート熱処理検査表ＦＡＸ
	or jh.sagyo_biko_code1 = '226' or jh.sagyo_biko_code2 = '226' or jh.sagyo_biko_code3 = '226' --　作業備考のどれかが２２６：ミルシート熱処理検査表メール
	or jh.sagyo_biko_code1 = '215' or jh.sagyo_biko_code2 = '215' or jh.sagyo_biko_code3 = '215' --　作業備考のどれかが２１５：熱処理検査表メール

	or jh.shuka_biko_code1 = '176' or jh.shuka_biko_code2 = '176' or jh.shuka_biko_code3 = '176' --　出荷備考のどれかが１７６：ミルシート　添付
	or jh.shuka_biko_code1 = '184' or jh.shuka_biko_code2 = '184' or jh.shuka_biko_code3 = '184' --　出荷備考のどれかが１８４：ミルシート熱処理検査表付
	or jh.shuka_biko_code1 = '185' or jh.shuka_biko_code2 = '185' or jh.shuka_biko_code3 = '185' --　出荷備考のどれかが１８５：ミルシート　ＦＡＸ＆添付
	or jh.shuka_biko_code1 = '263' or jh.shuka_biko_code2 = '263' or jh.shuka_biko_code3 = '263' --　出荷備考のどれかが２６３：ミルシート　メール＆添付
	or jh.shuka_biko_code1 = '183' or jh.shuka_biko_code2 = '183' or jh.shuka_biko_code3 = '183' --　出荷備考のどれかが１８３：熱処理検査表　添付
)

and (jh.create_date, jh.create_time) >= (to_char(CURRENT_TIMESTAMP + cast( '-1 days' as INTERVAL ), 'YYYY/MM/DD'), '14:00:00')
and (jh.create_date, jh.create_time) < (to_char(CURRENT_TIMESTAMP, 'YYYY/MM/DD'), '14:00:00')

order by jh.create_date, jh.create_time, jh.juchu_no_upper, jh.juchu_no_lower, jd.juchu_detail_no

""")

# データをＰｏｓｔｇｒｅＳＱＬからＤａｔａＦｒａｍｅに
df = pd.read_sql_query(query, engine)

# DB切断
engine.dispose()

# Save to CSV
# day 取得する
current_date = datetime.now()
formatted_date = current_date.strftime("%m%d")

new_year = current_date.strftime("%Y")[-2:] 
new_date = new_year + formatted_date

# "本日"名前付け保存する
file_name = f"{new_date}.csv"
file_path = r"\\192.168.160.6\usbdisk3\システム運用\■新システム\kintone 関連\ミルシート業務\取込CSV"
folder_name = current_date.strftime("%Y_%m")
folder_path = os.path.join(os.getcwd(), file_path , folder_name)		
if not os.path.exists(folder_path):								#月のフォルダーなければ作成
    os.makedirs(folder_path)
    print("フォルダー作成しました:", folder_path)
full_path = os.path.join(file_path, folder_path, file_name)
if not df.empty: #もしデータがあれべ保存
        df.to_csv(full_path, index=False, encoding='cp932')
        print(f"CSVファイル保存しました: {full_path}")
else: #なかったら終わり
        exit()


"------------------------------------------------------------------------------------------------"
count=0
#kintone 接続
DOMAIN = 'union-plate'## kintoneのドメイン
LOGIN = "659oda"## ログイン名
PASS = "union659"## パスワード
appno = 884## 取得したいアプリのアプリNo
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
    # CSVファイル読み込み
with open(full_path, 'r', newline='', encoding='cp932') as csvfile:
    #辞書型を作る：
    ## サイボウズ用にデータを整形に
     
    # 1行目無くして
    next(csv.reader(csvfile), None)  

    for row in csv.reader(csvfile):
        checkbox_labels = ["配達品", "仕入れ品", "工場差戻し", "FAX＆製品添付", "メール＆添付", "熱処理検査表あり"]
        checkbox_values = [label for label, value in zip(checkbox_labels, row[4:10]) if value == '1'] 
         
        body_fields = {
#1科目 = １即 "key-value":
        #営業本部行き先
        "営業本部行き先":{"value":row[0]},        
## バーコード
        "バーコード":{"value":row[1]},       
## 発送日コード
        "発送日コード":{"value":row[2]},       
## 出荷日
        "出荷日":{"value":datetime.strptime(row[3], '%Y/%m/%d').strftime('%Y-%m-%d')},     
## 特記事項　:(チェックボックス)       
        "特記事項": {"value": checkbox_values},
        #temp_body.update({label: value for label, value in zip(checkbox_labels, checkbox_values)})
        #body_fields.append(temp_body)
## 工場
        "ラジオボタン_0":{"value":row[10]},      
## 注番
        "注番":{"value":row[11]},      
## 枝番
        "枝番":{"value":row[12]},       
## 工場コード
        "工場コード":{"value":row[13]},      
## ミルシート処理
        "ラジオボタン":{"value":row[14]},       
## ミルシート得意先コード
        "ミルシート得意先コード":{"value":row[15]},       
## 製品仕様
        "製品仕様":{"value":row[16]}
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
                count +=1
                print(res_dict)  # kintone から帰還表示
        except urllib.error.URLError as e:
                if hasattr(e, "reason"):
                        print("Failed to reach the server:", e.reason)
                elif hasattr(e, 'code'):
                        print('The server couldn\'t fulfill the request.', e.code)
log_path = r'\\192.168.160.6\usbdisk3\システム運用\■新システム\kintone 関連\ミルシート業務\取込CSV\log'
file_log_name = f'{new_date}.txt'
folder_log_path = os.path.join(os.getcwd(), log_path , folder_name)
if not os.path.exists(folder_log_path):
    os.makedirs(folder_log_path)
    print("フォルダー作成しました:", folder_log_path)
full_log_path = os.path.join(log_path, folder_log_path, file_log_name)
#logフィル
# 新しいｔｘｔファイル作って開く
with open(full_log_path, 'w') as file:
    # 内容書き込む
    file.write("本日分の読み込み完了しました。\n {}件です。".format(count))

delta_date = current_date.strftime("%Y.%#m.%d")#YYYY.M.DD
# 利用するブラウザー
driver =Edge()
driver.get(r"https://union-plate.cybozu.com/login")
file_path = r"C:\Users\DSP189\Desktop\user1.txt"

with open(file_path, "r") as file:
    lines = file.readlines()
    username = lines[0].strip()  # Line1: username
    password = lines[1].strip() # Line2: password
# ID入力フィールドを見つけて値を入力します。
username_field = driver.find_element(By.NAME, "username")
username_field.send_keys(username)

# パスワード入力フィールドを見つけて値を入力します。
password_field = driver.find_element(By.NAME, "password")
password_field.send_keys(password)

 
# ログイン
submit_button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='ログイン']")
submit_button.click()
button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.service-slash[href="/o/"]'))
    )
 
   # ボタンをクリックする
button.click()
#備忘:仕入品ミルシート添付kintone登録 link:
link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, f'a.event[href*="ag.cgi?page=ScheduleView&UID=942&GID=&Date=da.{delta_date}&BDate=da.{delta_date}"][title*="備忘:仕入品ミルシート添付kintone登録"]'))
    )

    
link.click()
#logファイ読み込み：
with open(full_log_path, "r") as file:
        comment_data = file.read()
comment = driver.find_element(By.ID,"dz_NewComment")
comment.send_keys(comment_data) #コメントの所に書き込み
file_input = driver.find_element(By.CSS_SELECTOR, 'input[type="file"][id*="filese"][name="files[]"][size="0"][multiple]')
file_input.send_keys(full_path)#CSVファイル添付する
send = driver.find_element_by_css_selector('input.vr_hotButton[type="submit"][name="WriteFollow"]')
 
send.click()#書き込みボタンをクリックする。
input("j:")