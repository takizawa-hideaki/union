
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import os
import csv
import requests
import base64
""""""
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

# Đọc dữ liệu từ PostgreSQL vào DataFrame
df = pd.read_sql_query(query, engine)

# Đóng kết nối
engine.dispose()


# Save to CSV
# Lấy ngày hiện tại
current_date = datetime.now()
formatted_date = current_date.strftime("%m%d")

new_year = current_date.strftime("%Y")[-2:] 
new_date = new_year + formatted_date

# Tạo tên file dựa trên ngày hiện tại
file_name = f"{new_date}.csv"

file_path = r"C:\\Users\\DSP189\\Desktop\\新しいフォルダー (2)"
full_path = os.path.join(file_path, file_name)
df.to_csv(full_path, index=False, encoding='cp932')
print(f"Da luu file: {full_path}")




"""----------------------------------------------------------------"""
# Thông tin của Kintone
domain = 'union-plate'
app_id = '1167'
api_token = 'dvPYLYJ8RnArbsChKQg3yHVTSK4neGSw0SIJ9x4l'


# Đọc dữ liệu từ file CSV
with open(full_path, 'r') as file:
    csv_data = list(csv.DictReader(file))
print(csv_data)

# Gửi dữ liệu lên Kintone
url = f'https://{domain}.cybozu.com/k/v1/records.json'
headers = {
    'Content-Type': 'application/json',
    'X-Cybozu-API-Token': api_token,
}

payload = {
    'app': app_id,
    'records': csv_data,
}

response = requests.post(url, headers=headers, json=payload)

if response.status_code == 200:
    print("Dữ liệu đã được tải lên Kintone thành công.")
else:
    print(f"Lỗi khi tải lên Kintone. Mã lỗi: {response.status_code}")
    print(response.text)
