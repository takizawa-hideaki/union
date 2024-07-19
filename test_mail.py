#ver 0.0.1: CC追加

import os
import shutil
from datetime import datetime, timedelta
# coding: utf-8
#import sys
import win32com.client
import pythoncom

pythoncom.CoInitialize()
outlook = win32com.client.Dispatch("Outlook.Application")

mapi = outlook.GetNamespace("MAPI")
    # draft_box = mapi.GetDefaultFolder(16) # 16が下書きフォルダの番号らしい
    

current_date = datetime.now().date()
formatted_date = current_date.strftime("%y%m%d")
class Tokuisaki:
    def __init__(self, a,b,c,d,e= None):
        self.tokuisaki_code = a
        self.folder_name = b
        self.kyaku = c
        self.mail_address = d
        self.mail_cc = e
# Thông tin xác thực
#username = 'administrator'
#password = 'Fdomain100'
# Đường dẫn đến thư mục chứa các file PDF
path1=f'\\\\192.168.160.65\\d$\\UP-EZCENS\\得意先'
# Thực hiện xác thực bằng cách sử dụng quyền truy cập của người dùng hiện tại
#os.system(f"net use {source_folder} /user:{username} {password}")
# Lấy danh sách các tệp tin trong thư mục
file_list = os.listdir(path1)

tokuisakies = [
	Tokuisaki('029007', "29007_粟井鋼商事㈱福岡営業所_____●", "粟井鋼商事㈱福岡営業所", "awaifax@yacht.ocn.ne.jp"),
	Tokuisaki('029267', "29267_協伸メタル㈱_____●", "協伸メタル㈱", "matsumoto@kyosi-n.com"),	
	Tokuisaki('029494', "29494_㈱鉄鋼社　長野営業所_____●", "㈱鉄鋼社　長野営業所","nagano@tekkosha.co.jp"),
	Tokuisaki('029495', "29495_㈱鉄鋼社_____●", "㈱鉄鋼社", "arakik@tekkosha.co.jp","watanabem@tekkosha.co.jp"),
	Tokuisaki('029498', "29498_㈱鉄鋼社　北関東営業所_____●", "㈱鉄鋼社　北関東営業所", "kitakanto@tekkosha.co.jp"),
	Tokuisaki('029506', "29506_㈱鉄鋼社　東北営業所_____●", "㈱鉄鋼社　東北営業所", "touhoku@tekkosha.co.jp"),
	Tokuisaki('029554', "29554_アイケーメタル㈱　狭山営業所___●", "アイケーメタル㈱　狭山営業所", "sayama@ikmetal.co.jp"),
	#Tokuisaki('029571', "29571_協同組合　島根県鐵工会　出雲営業所_____●", "協同組合　島根県鐵工会　出雲営業所", "k-fujihara@tekkokai.or.jp"),
	Tokuisaki('029698', "29698_㈱林角本店　非鉄金属部___●", "㈱林角本店　非鉄金属部", "takeuchi@hayashikaku.co.jp"),
	Tokuisaki('029806', "29806_富源商事㈱　上越支店____●", "富源商事㈱　上越支店","y-itou@fugen-corp.co.jp"),
	#Tokuisaki('029879', "29879_萬世興業㈱　本社_____●", "萬世興業㈱　本社","okada@vansei.co.jp"),
	Tokuisaki('029886', "29886_萬世興業㈱　日光営業所_____●29879本社へ", "萬世興業㈱　日光営業所","okada@vansei.co.jp"),
	Tokuisaki('029896', "29896_保田特殊鋼㈱本社_____●", "保田特殊鋼㈱本社","yasuda_osaka@yasutoku1931.com"),
    
]
destination_folder = r"C:\\Users\\DSP189\\Desktop\\新しいフォルダー (5)"

for tokuisaki_code in tokuisakies:
    #print(tokuisaki_code.tokuisaki_code, tokuisaki_code.folder_name)  
    source_folder = f"{path1}\\{tokuisaki_code.tokuisaki_code}\\PDF"
    # Thực hiện kiểm tra trong một thư mục cụ thể
    directory1 = f"{destination_folder}\\{tokuisaki_code.folder_name}"
    destination_directory = f"{destination_folder}\\{tokuisaki_code.folder_name}\\old"
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
            destination_path = os.path.join(destination_folder, tokuisaki_code.folder_name)
            destination_file = shutil.copy(pdf_source_path, destination_path)
            print(destination_file)
            
    

            title_send_day = f"{formatted_date}"
            corporate_name = tokuisaki_code.kyaku
            send_day = current_date.strftime("%m/%d")
    
            if destination_file is not None:
                draft_box = mapi.Folders("r-tong@union-plate.co.jp").Folders("下書き")
                mail = outlook.CreateItem(0)
                mail.To = tokuisaki_code.mail_address
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
                if tokuisaki_code.mail_cc:
                    mail.CC = tokuisaki_code.mail_cc
                mail.Move(draft_box)

            


