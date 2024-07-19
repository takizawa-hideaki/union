import psycopg2
import datetime
from openpyxl import Workbook
from openpyxl import load_workbook
import pandas as pd
from openpyxl.styles import Font
import openpyxl as xl
from selenium.webdriver import Edge
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# データベースへの接続用設定
users = 'unionplate'			# ユーザID 
host = '192.168.160.83'			# 接続先IPアドレス
dbnames = 'union_hanbai'		# DB名
passwords = 'etalpnoinu'		# パスワード

# def get_date_range(year, month):
#     # Tính toán ngày bắt đầu (1st day of the month)
#     start_date = datetime.date(year, month, 1)
    
#     # Tính toán ngày kết thúc (last day of the month)
#     next_month = start_date.replace(month=start_date.month+1, day=1)
#     end_date = next_month - datetime.timedelta(days=1)
    
#     return start_date, end_date

start_day = datetime.date.today()-datetime.timedelta(days=7)
end_day = datetime.date.today()-datetime.timedelta(days=1)
start_date = start_day.strftime("%Y/%m/%d")
end_date = end_day.strftime("%Y/%m/%d")
tables = {
    'offc_trn_juchu_head': 'offc_trn_juchu_details',
    # Add more table mappings if needed
}

# def sql_count_juchu(users, host, dbnames, passwords, staff_department_mapping, tables, start_date, end_date):
#     # DB kết nối
conn = psycopg2.connect(f"user={users} host={host} dbname={dbnames} password={passwords}")
cur = conn.cursor()
    
all_results = []
columns = None
for head_table, detail_table in tables.items():
#         # Tạo phần truy vấn SQL dựa trên tập hợp staff_names
    sql_query = f"""select jh.juchu_no_upper, jh.juchu_no_lower, jd.juchu_detail_no, jh.tokuisaki_code, jh.tokuisaki_name1, jh.tokuisaki_name2, jh.tokuisaki_name3, jh.todokesaki_code, jh.todokesaki_name1, jh.todokesaki_name2, jh.todokesaki_name3,		
		jd.zaishitsu_code, jd.zaishitsu_name, jd.size_a, jd.size_b, jd.size_c, jd.suryo, jd.juryo, jd.jitsukan_juryo, jd.fraisu_name, jd.grind_name, jd.shuka_date, jd.tochaku_date,
		jdp.ipon_tanka_sup, jdp.total_sakes_kingaku
from {head_table} as jh		
		
join {detail_table} as jd		
on jh.juchu_no_upper = jd.juchu_no_upper		
and jh.juchu_no_lower = jd.juchu_no_lower		
and jd.delete_flag = 0		
		
join offc_trn_juchu_details_price as jdp		
on jh.juchu_no_upper = jdp.juchu_no_upper		
and jh.juchu_no_lower = jdp.juchu_no_lower		
and jd.juchu_detail_no = jdp.juchu_detail_no		
and jdp.kojokan_cf = '0'		
		
where jh.tokuisaki_code = '27693'		
and jd.shuka_date between '{start_date}' and '{end_date}'			
		
order by jh.juchu_no_upper, jh.juchu_no_lower, jd.juchu_detail_no
"""		


    cur.execute(sql_query)
    results = cur.fetchall()
    # print(results)
    # Save results to list
    if columns is None:
        columns = [desc[0] for desc in cur.description]
    
    # Save results to list
    all_results.extend(results)

# Close the cursor and connection
cur.close()
conn.close()

# Convert results to DataFrame
df = pd.DataFrame(all_results, columns=columns)

# Define filename
filename = f"双葉浜松受注明細一覧_{start_day}_{end_day}.xlsx"
excel_path = f"C:\\Users\\DSP189\\Desktop\\名豊浜松・双葉浜松受注明細一覧\\{filename}"

# Write DataFrame to Excel file
with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
    df.to_excel(writer, index=False, sheet_name="双葉浜松")

print(f"Data has been written to {filename}")
# # Thực hiện các truy vấn và ghi kết quả vào file Excel
# results = sql_count_juchu(users, host, dbnames, passwords, staff_department_mapping, tables, start_date, end_date)
# excel_date_str = pd.to_datetime(end_date).strftime('%Y%m%d')

# write_results_to_excel(results, staff_department_mapping, tables, excel_path)
# sql_juchu(users, host, dbnames, passwords, staff_department_mapping, tables, start_date, end_date, excel_path)
wb1 = xl.load_workbook(filename=excel_path)


# # set font
font = Font(name='游ゴシック')

for ws1 in wb1.worksheets:
    for row in ws1:
        for cell in row:
            ws1[cell.coordinate].font = font

# save xlsx file
wb1.save(excel_path)
#----------------------------------------------------------------
driver =Edge()
driver.get(r"https://union-plate.cybozu.com/o/ag.cgi?page=MyFolderMessageView&mid=23340&mdbid=2")
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
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.commentAreaWrapper textarea.resizeTarget"))
    )
 
   # ボタンをクリックする
button.click()
try:
	#comment = driver.find_element(By.ID,"dz_NewComment")
	#comment.send_keys(comment_data) #コメントの所に書き込み
	file_input = driver.find_element(By.CSS_SELECTOR, 'input[type="file"][id*="filesm1057_1"][name="files[]"][size="0"][multiple]')
	file_input.send_keys(excel_path)#CSVファイル添付する
	all_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@type="button" and @class="mentionAllMemberButton" and contains(text(), "@ 宛先全員を指定")]')))
	all_button.click()#書き込みボタンをクリックする。
	submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//input[@class="vr_hotButton" and @type="submit" and @value="書き込む" and @name="Submit"]')))
	submit_button.click()#書き込みボタンをクリックする。
	
except: 
	input("コメントできませんでした。")


