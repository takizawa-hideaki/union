
###Version 0.0.1 : 工場間通信時 追加

import psycopg2
import datetime
import subprocess
import msvcrt
import time 


class FactoryInfo:
	def __init__(self, coporation_code, office_factory_code, office_factory_name, office_factory_ryaku, ip_address):
		self.coporation_code = coporation_code
		self.factory_code = office_factory_code
		self.name = office_factory_name
		self.ryaku = office_factory_ryaku
		self.ip = ip_address

class ThrdTran:
	def __init__(self, test_tuple) :
		self.date = test_tuple[0]
		self.no = test_tuple[1]
		self.upper = test_tuple[2]
		self.lower = test_tuple[3]
		self.key = test_tuple[4]
		self.request = test_tuple[5]
		self.execute = test_tuple[6]
		self.complete = test_tuple[7]
		self.datafile = test_tuple[8]
		self.staff = test_tuple[9]
		self.create_date = test_tuple[10]
		self.create_time = test_tuple[11]
		self.update_date = test_tuple[12]
		self.update_time = test_tuple[13]

# DB接続 → SQL実行 → DB切断
def sql_run(users, host, dbnames, passwords):
	# DB接続
	conn = psycopg2.connect(" user=" + users +" host=" + host +" dbname=" + dbnames +" password=" + passwords)

	# sqlの実行
	cur = conn.cursor()
	cur.execute(f"\
				select * \
				from fact_thrd_transmission_request \
				where request_date = {date_today}"
				)
	results = cur.fetchall()

	# DB切断
	cur.close()
	conn.close()

	return results


# 工場の情報
factorys = [
	FactoryInfo(10, 100, "㈱ユニオンプレート本社工場", "本社", "192.168.162.51"),
	FactoryInfo(10, 101, "ユニオン本社ＦＣ工場", "FC工場", "192.168.162.61"),
	FactoryInfo(10, 520, "ユニオン尾道アルミ工場", "尾道アルミ", "192.168.17.61"),
	FactoryInfo(10, 520, "ユニオン尾道アルミ工場端材", "尾道アルミ端材", "192.168.17.121"),
	FactoryInfo(10, 570, "ユニオン尾道工場", "尾道", "192.168.17.51"),
	FactoryInfo(10, 570, "ユニオン尾道工場端材", "尾道端材", "192.168.17.101"),
	FactoryInfo(10, 580, "ユニオン厚木工場", "厚木", "192.168.18.51"),
	FactoryInfo(10, 580, "ユニオン厚木工場端材", "厚木端材", "192.168.18.101"),
	FactoryInfo(10, 650, "ユニオン小牧工場", "小牧", "192.168.25.51"),
	FactoryInfo(10, 650, "ユニオン小牧工場端材", "小牧端材", "192.168.25.101"),
	FactoryInfo(10, 670, "ユニオン上田工場", "上田", "192.168.161.51"),
	FactoryInfo(10, 680, "ユニオン千曲工場", "千曲", "192.168.28.51"),
	FactoryInfo(50, 500, "ＩＮＳ加工工場", "INS", "192.168.10.51"),
	FactoryInfo(51, 510, "㈲藤精工", "藤精工", "192.168.11.51"),
	FactoryInfo(53, 530, "㈲サンテック", "ｻﾝﾃｯｸ", "192.168.13.51"),
	FactoryInfo(54, 540, "㈲エムケイ精工", "MK", "192.168.14.51"),
	FactoryInfo(55, 550, "㈱渡辺製作所", "渡辺", "192.168.15.51"),
	FactoryInfo(55, 560, "㈲ＵＰＭ", "UPM", "192.168.16.51"),
	FactoryInfo(59, 590, "㈲エムテーエス", "MTS", "192.168.19.51"),
	FactoryInfo(60, 600, "ＡＵＫプレート㈱", "AUK", "192.168.20.51"),
	FactoryInfo(60, 601, "ＡＵＫプレート㈱アルミ工場", "ＡＵＫアルミ", "192.168.20.61"),
	FactoryInfo(63, 630, "㈱メカニックメタル", "MM", "192.168.23.51"),
	FactoryInfo(64, 640, "㈲鈴木鋼管工業", "鈴木", "192.168.24.51"),
	FactoryInfo(55, 560, "㈲峰岸商会", "峰岸商会", "192.168.22.61"),
	FactoryInfo(55, 560, "㈲峰岸加工工場", "峰岸加工工場", "192.168.22.51"),
]


# 本日日付の取得
date_today = datetime.date.today().strftime('\'%Y/%m/%d\'')

# 現在時刻の取得
time_now = datetime.datetime.now()

# 時間の閾値
time_limit = datetime.timedelta(minutes=1)


# データベースへの接続用設定
users = 'unionfactory'			# ユーザID 
host = ''						# 接続先IPアドレス
dbnames = 'union_factory'		# DB名
passwords = 'yrotcafnoinu'		# パスワード

# 登録工場分fact_thrd_transmission_requestのチェック
for factory in factorys:
	print("**********")
	host = factory.ip	# 工場のIPアドレスをセット
	NG_FLAG = 0

	# Pingチェック
	try:
		check_ping = subprocess.check_output(["ping", "-n", "1", host])
	except:
		print("NG", factory.ryaku, "No signal")
		continue

	# SQLの実行
	results = sql_run(users, host, dbnames, passwords)

	# 1レコードもない場合
	if len(results) < 1:
		print("NG", factory.ryaku, "No data")
		NG_FLAG = 1

	# １レコードずつチェック
	for result in results:
		thrd_tran = ThrdTran(result)

		# request、execute、completeの各フラグのどれかが0の場合NGとして出力
		if thrd_tran.request == 0 or thrd_tran.execute == 0 or thrd_tran.complete == 0:
			# 時間比較
			# create date、create timeかupdate date、update timeのあるなしをチェックupdate優先
			if (thrd_tran.update_date):
				check_time = datetime.datetime(year=int(thrd_tran.update_date.split('/')[0]), month=int(thrd_tran.update_date.split('/')[1]), day=int(thrd_tran.update_date.split('/')[2]), hour=int(thrd_tran.update_time.split(':')[0]), minute=int(thrd_tran.update_time.split(':')[1]), second=int(thrd_tran.update_time.split(':')[2]))
			else:
				check_time = datetime.datetime(year=int(thrd_tran.create_date.split('/')[0]), month=int(thrd_tran.create_date.split('/')[1]), day=int(thrd_tran.create_date.split('/')[2]), hour=int(thrd_tran.create_time.split(':')[0]), minute=int(thrd_tran.create_time.split(':')[1]), second=int(thrd_tran.create_time.split(':')[2]))

			check_limit = time_now - time_limit
			if (check_time < check_limit):
				print("NG", factory.ryaku, result)
				NG_FLAG = 1

	# NGがなかった場合の出力
	if NG_FLAG == 0:
		print(factory.ryaku, "OK")
print("工場間通信時：", time_now)

print("閉じるには'Enter'キーを押してください . . .")
start_time = time.time() # Thời điểm bắt đầu chờ

# Lặp cho đến khi người dùng nhập hoặc hết thời gian
while True:
    if time.time() - start_time >= 300: # Nếu đã hết 300 giây
        
        exit()
    if msvcrt.kbhit():  # Kiểm tra nếu có ký tự được nhấn từ bàn phím
        input()
        break # Thoát khỏi vòng lặp nếu có dữ liệu nhập từ bàn phím






