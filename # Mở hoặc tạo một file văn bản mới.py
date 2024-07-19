import os
from datetime import datetime

current_date = datetime.now()
formatted_date = current_date.strftime("%m%d") 
new_year = current_date.strftime("%Y")[-2:] 
new_date = new_year + formatted_date
count = 15
log_path = r'\\192.168.160.6\usbdisk3\システム運用\■新システム\kintone 関連\ミルシート業務\取込CSV\log'
file_name = f'{new_date}.txt'
full_log_path = os.path.join(log_path, file_name)

# Mở hoặc tạo một file văn bản mới
with open(full_log_path, 'w') as file:
    # Viết dữ liệu vào file
    file.write("本日分の読み込み完了しました。\n {}件です。".format(count))
   
