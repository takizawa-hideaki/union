#ver 0.0.1: CC追加

import os
import shutil
from datetime import datetime, timedelta
# coding: utf-8
#import sys
import win32com.client
import pythoncom
import json
from sqlalchemy import create_engine, text
# データベースへの接続用設定
database_uri = 'postgresql://unionplate:etalpnoinu@192.168.160.83:5432/union_hanbai'
engine = create_engine(database_uri)


pythoncom.CoInitialize()
outlook = win32com.client.Dispatch("Outlook.Application")

mapi = outlook.GetNamespace("MAPI")
    # draft_box = mapi.GetDefaultFolder(16) # 16が下書きフォルダの番号らしい
    

current_date = datetime.now().date()
formatted_date = current_date.strftime("%y%m%d")
class Tokuisaki:
    def __init__(self, a,b,c):
        self.tokuisaki_code = a
        self.folder_name = b
        self.kyaku = c
        
# Thông tin xác thực
#username = 'administrator'
#password = 'Fdomain100'
# Đường dẫn đến thư mục chứa các file PDF
path1=f'\\\\192.168.160.65\\d$\\UP-EZCENS\\得意先'
# Thực hiện xác thực bằng cách sử dụng quyền truy cập của người dùng hiện tại
#os.system(f"net use {source_folder} /user:{username} {password}")
# Lấy danh sách các tệp tin trong thư mục
file_list = os.listdir(path1)

with open("tokuisakies.json", "r", encoding="utf-8") as json_file:
    data = json.load(json_file)
destination_folder = r"C:\\Users\\DSP189\\Desktop\\新しいフォルダー (5)"

for item in data:
    tokuisaki_code = item["tokuisaki_code"]
    folder_name = item["folder_name"]
    kyaku = item["kyaku"]

    
    #print(tokuisaki_code.tokuisaki_code, tokuisaki_code.folder_name)  
    source_folder = f"{path1}\\{tokuisaki_code}\\PDF"
    # Thực hiện kiểm tra trong một thư mục cụ thể
    directory1 = f"{destination_folder}\\{folder_name}"
    destination_directory = f"{destination_folder}\\{folder_name}\\old"
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    # Duyệt qua tất cả các tập tin trong thư mục nguồn
    for filename in os.listdir(directory1):
        # Tạo đường dẫn đầy đủ đến tập tin
        filepath = os.path.join(directory1, filename)
        # Kiểm tra xem tập tin có phải là PDF không
        if os.path.isfile(filepath) and filename.lower().endswith(".pdf"):
            try:
                if os.path.exists(filepath):
            # Di chuyển tập tin PDF vào thư mục đích
                    shutil.move(filepath, destination_directory)
                    print(f"Đã di chuyển {filename} vào thư mục đích.")
            except:
                print(f"Đã  ko di chuyển {filename} vào thư mục đích.")
                continue
            
 


    
        


# Đường dẫn đến thư mục mà chúng ta muốn sao chép file PDF đến
    
    previous_date = datetime.now() - timedelta(days=1)
    

# Định dạng lại ngày thành chuỗi "ddmmyyyy"
    previous_date_str = previous_date.strftime("%Y%m%d")[2:]

# Tên file PDF cần tìm
    #pdf_filename_format = f"納品書{previous_date_str}_10001_{tokuisaki_code}_"

    for filename in os.listdir(source_folder):
        if filename.endswith(".pdf") and filename.startswith(f"納品書{previous_date_str}_10001_"):
        # Lấy số phần sau dấu gạch dưới cuối cùng trong tên file
                #print(f"Tìm thấy tệp: {filename}")
        # Tạo đường dẫn đầy đủ đến file PDF trong thư mục nguồn
            pdf_source_path = os.path.join(source_folder,filename)
                
            #folder_name = filename.split("_")[-2]
            #folder_name = folder_name.lstrip('0')
               
# Tạo đường dẫn đầy đủ đến thư mục đích
            destination_path = os.path.join(destination_folder, folder_name)
            destination_file = shutil.copy(pdf_source_path, destination_path)
            print(destination_file)
            
    

            title_send_day = f"{formatted_date}"
            corporate_name = kyaku
            send_day = current_date.strftime("%m/%d")

            if destination_file is not None:
                # Mở kết nối và thực thi truy vấn
                with engine.connect() as connection:

                    query = text(f"""select tokuisaki_code, task_name, destination_cf, 
	                                email_address, delete_flag
                                    from offc_mst_destination_email_address
                                    where tokuisaki_code = {tokuisaki_code}
                                    and task_name = '納品書'
                                    and delete_flag = 0
                                    order by create_date, task_name""")
                    result = connection.execute(query)
                    query_result = result.fetchall()
                    # Tạo danh sách để lưu các địa chỉ email
                    to_addresses = []
                    cc_addresses = []
                    bcc_addresses = []
                    for row in query_result:
                        destination_cf = row[2]
                        email_address = row[3]
                        if destination_cf == '0':
                            to_addresses.append(email_address)
                        elif destination_cf == '1':
                            cc_addresses.append(email_address)
                        elif destination_cf == '2':
                            bcc_addresses.append(email_address)
                    connection.close()
                           
                    draft_box = mapi.Folders("r-tong@union-plate.co.jp").Folders("下書き")
                    mail = outlook.CreateItem(0)
                    mail.To = '; '.join(to_addresses) if to_addresses else ""  # To
                    mail.CC = '; '.join(cc_addresses) if cc_addresses else ""  # Cc
                    mail.BCC = '; '.join(bcc_addresses) if bcc_addresses else ""  # Bcc                      
                    mail.Subject = '{}_Union_納品書添付について'.format(title_send_day)
                    mail.Attachments.Add(destination_file)
                    mail.Body = """{}　御中 
　　　　　　　　　　　　　　　　　　
 
拝啓
　平素は、格別のお引立てを賜り、厚くお礼申し上げます。 
 
 
{}  に送信されました納品書ファイルを再送致しますので、
御確認宜しくお願いします。
　
 
以上、宜しくお願い申し上げます。
 

　　　　　　　　　　　　　　　　　　　　　　　　　敬具

 
 
□□□□□□□□□□□□□□□□□□□□
  〒389-0802　長野県千曲市大字内川622-1
  株式会社ユニオンプレート
  TEL：026-275-4001　FAX：026-275-4002
□□□□□□□□□□□□□□□□□□□□

""".format(corporate_name, send_day)
                mail.Move(draft_box)

            


