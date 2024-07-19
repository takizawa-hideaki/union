#test_sql2
import psycopg2
import datetime
from openpyxl import Workbook
import pandas as pd
# データベースへの接続用設定
users = 'unionplate'			# ユーザID 
host = '192.168.160.83'			# 接続先IPアドレス
dbnames = 'union_hanbai'		# DB名
passwords = 'etalpnoinu'		# パスワード

def get_date_range(year, month):
    # Tính toán ngày bắt đầu (1st day of the month)
    start_date = datetime.date(year, month, 1)
    
    # Tính toán ngày kết thúc (last day of the month)
    next_month = start_date.replace(month=start_date.month+1, day=1)
    end_date = next_month - datetime.timedelta(days=1)
    
    return start_date, end_date

previous_month = datetime.date.today().month-1 
previous_year = datetime.date.today().year 
if previous_month <= 0: 
    previous_month +=12
    previous_year = previous_year - 1
print( previous_month,previous_year)
# Sử dụng hàm để lấy ngày bắt đầu và ngày kết thúc
start_date, end_date = get_date_range(previous_year, previous_month)
start_date = start_date.strftime("%Y/%m/%d")
end_date = end_date.strftime("%Y/%m/%d")
excel_path = r"C:\Users\DSP189\Desktop\test\example.xlsx"
def sql_juchu(users, host, dbnames, passwords, staff_department_mapping, tables, start_date, end_date):
    # DB kết nối
    conn = psycopg2.connect(f"user={users} host={host} dbname={dbnames} password={passwords}")
    
    # Khởi tạo một ExcelWriter để ghi vào file Excel
    writer = pd.ExcelWriter(excel_path, engine='xlsxwriter')
    for table, new_table_name in tables.items():
        # Tạo phần truy vấn SQL dựa trên tập hợp staff_name
        for staff_name, eigyou_bu in staff_department_mapping.items():
            sql_query = f"SELECT * FROM {table} WHERE create_staff in ({staff_name})\
                AND create_date BETWEEN '{start_date}' AND '{end_date}'\
                    order by create_date, create_time, create_staff, update_date, update_time, update_staff
                    "
            data = pd.read_sql_query(sql_query, conn)

            # Ghi dữ liệu vào sheet mới với tên là tên bảng
            data.to_excel(writer, sheet_name=f"{new_table_name}_{eigyou_bu}", index=False)


        
        
        #for row in results:
         #   for eigyou_bu, count in zip(staff_department_mapping.values(), row):
          #      print(results)
        

                    
        
        

    # Đóng kết nối
    conn.close()
    # Lưu và đóng writer
    
    writer.close()

# Tạo danh sách các bảng cần thực hiện truy vấn
tables = {"offc_trn_juchu_details":"受注", "offc_trn_mitsumori_details":"見積", "offc_trn_hachu":"発注","offc_trn_juchu_details_check":"チェック"}
# Tạo ánh xạ giữa tên nhân viên và tên bộ phận
staff_department_mapping = {"'竹内奈波','成澤真菜','藤沢寿珠','倉嶋健人','村越大輔','廣田舞','今井萌','武井千尋','小林勇太','加藤新大','葛嶋一騎','小山和真','高橋健太','佐藤輝一'": "１部",
                            "'永坂風歌','河野真由美','奥村かの子','清水明日花','亘由紀子','千野幸恵','宮本玲愛','中村芽雅美','内藤彩乃','唐澤大貴','吉野来美','那須野豊','安齋朋洋','松本拓巳','出野ちぇりー','北航大','笠井光'": "２部",
                            "'高山紗弓','久保咲羽','両角和香菜','落合渉','松岡里奈','池内裕樹','伊藤真緒','小泉直美','市川敬吾','葛嶋一騎','岡島海祐','鍋嶋蓮','佐藤浩輔','遠藤　匠'":"３部",
                            "'仲俣智子','中村洋子','宮嵜彩子','西澤夏恵','寺澤綾','松崎和世','遠藤一枝','近藤徳子','國安百合子','内山善美','吉田美加','松岡愛','宮本理香','久保田美穂','栁町めぐみ','森屋麻希子','小林美保','宮崎美加','三井恵美','中川愛理','古澤亜沙美','高村美佳','山崎菜月','白石汐那','中澤沙季','小泉夏菜子','竹内茜','荻原夏季','中村めぐみ'":"アルバイト"}

sql_juchu(users, host, dbnames, passwords, staff_department_mapping, tables, start_date, end_date)


    