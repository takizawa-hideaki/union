import pandas as pd
import os
from datetime import datetime

# Đường dẫn tới tệp Excel
excel_file_path = r'C:\Users\DSP189\Downloads\123.xlsm'

# Tên của sheet bạn muốn lưu
sheet_name = 'CSV'

# Đọc dữ liệu từ sheet vào DataFrame
df = pd.read_excel(excel_file_path, sheet_name=sheet_name)

# day 取得する
current_date = datetime.now()
formatted_date = current_date.strftime("%m%d")

new_year = current_date.strftime("%Y")[-2:] 
new_date = new_year + formatted_date
file_name = f"{new_date}.csv"

# Đường dẫn tới tệp CSV mà bạn muốn lưu
file_path = r'C:\Users\DSP189\Downloads\test'
folder_name = current_date.strftime("%Y_%m")
folder_path = os.path.join(os.getcwd(), file_path , folder_name)		
if not os.path.exists(folder_path):								#月のフォルダーなければ作成
    os.makedirs(folder_path)
    print("フォルダー作成しました:", folder_path)
full_path = os.path.join(file_path, folder_path, file_name)

# Lưu DataFrame vào tệp CSV
df.to_csv(full_path, index=False, encoding='cp932')

print(f"Dữ liệu từ sheet '{sheet_name}' đã được lưu thành công vào tệp CSV.")
