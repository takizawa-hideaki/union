import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import os
import base64
import urllib.request
import json
import csv

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

"------------------------------------------------------------------------------------------------"
count=0
file_path = r"C:\\Users\\DSP189\\Desktop\\新しいフォルダー (2)"
full_path = os.path.join(file_path, file_name)
df.to_csv(full_path, index=False, encoding='cp932')
print(f"CSVファイル保存しました: {full_path}")

#kintone 接続
DOMAIN = 'union-plate'## kintoneのドメイン
LOGIN = "659oda"## ログイン名
PASS = "union659"## パスワード
appno = 1167## 取得したいアプリのアプリNo
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

file_path = r"C:\\Users\\DSP189\\Desktop\\新しいフォルダー (2)"
## body作成

    # CSVファイル読み込み
with open(full_path, 'r', newline='', encoding='cp932') as csvfile:
    #辞書型を作る：
    csv_reader = csv.reader(csvfile)
    ## サイボウズ用にデータを整形に
    body_fields = [] 
    # 1行目無くして
    next(csv_reader, None)  
          
    for row in csv_reader:

#1科目 = １即 "key-value":
        #営業本部行き先
        temp_body = {"営業本部行き先":{"value":row[0]}}
        body_fields.append(temp_body)
## バーコード
        temp_body = {"バーコード":{"value":row[1]}}
        body_fields.append(temp_body)
## 発送日コード
        temp_body = {"発送日コード":{"value":row[2]}}
        body_fields.append(temp_body)
## 出荷日
        temp_body = {"出荷日":{"value":datetime.strptime(row[3], '%Y/%m/%d').strftime('%Y-%m-%d')}}
        body_fields.append(temp_body)
## 特記事項　:(チェックボックス)
        checkbox_labels = ["配達品", "仕入れ品", "工場差戻し", "FAX＆製品添付", "メール＆添付", "熱処理検査表あり"]

        checkbox_values = [label for label, value in zip(checkbox_labels, row[4:10]) if value == '1']
        temp_body = {"特記事項": {"value": checkbox_values},}
        temp_body.update({label: value for label, value in zip(checkbox_labels, checkbox_values)})
        body_fields.append(temp_body)
## 工場
        temp_body = {"ラジオボタン_0":{"value":row[10]}}
        body_fields.append(temp_body)
## 注番
        temp_body = {"注番":{"value":row[11]}}
        body_fields.append(temp_body)
## 枝番
        temp_body = {"枝番":{"value":row[12]}}
        body_fields.append(temp_body)
## 工場コード
        temp_body = {"工場コード":{"value":row[13]}}
        body_fields.append(temp_body)
## ミルシート処理
        temp_body = {"ラジオボタン":{"value":row[14]}}
        body_fields.append(temp_body)
## ミルシート得意先コード
        temp_body = {"ミルシート得意先コード":{"value":row[15]}}
        body_fields.append(temp_body)
        ## 製品仕様
        temp_body = {"製品仕様":{"value":row[16]}}
        body_fields.append(temp_body)


# CSVファイルから１レコード取得 11即 "key-value":
chunk_size = 12
chunks = [body_fields[i:i+chunk_size] for i in range(0, len(body_fields),chunk_size)]

# 各"key-value"含まれるリスト作成
grouped_body_fields = []
# 11即 "key-value"含まれる大きい辞書作成
for chunk in chunks:    
    group_dict = {}
    # chunksの中に item_dict 回す
    for item_dict in chunk:
        # item_dictからkey, value 回す
        for key, value in item_dict.items():
            # group_dict　の中にkey の値があったらそのまま大き辞書に追加する
            if key in group_dict:
                group_dict[key].append(value)
            else:
                # 値がなかったら値入れて大き辞書に追加する
                group_dict[key] = value
    #"key-value"は group_dict　から　grouped_body_fieldsに追加
    grouped_body_fields.append(group_dict)


# サイボウズに書き込む
for group in grouped_body_fields:
    body_record = {"record": group}#grouped_body_fieldsからrecord作成
    body = {"app": appno, **body_record}
    print(body)
    # "body" :JSONに変換
    json_data = json.dumps(body).encode()
    # HTTP　リクエスト作成
    req = urllib.request.Request(
        url=uri,
        data=json_data,
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
print("本日分の読み込み完了しました。\n {}件です。".format(count))
input("閉じるには'Enter'キーを押してください . . .")
