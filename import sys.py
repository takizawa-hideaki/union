import os
import shutil
from datetime import datetime, timedelta

class Tokuisaki:
	def __init__(self, a,b):
		self.tokuisaki_code = a
		self.folder_name = b
# Thông tin xác thực
#username = 'administrator'
#password = 'Fdomain100'
# Đường dẫn đến thư mục chứa các file PDF
path=r'C:\\Users\\DSP189\Desktop\\新しいフォルダー (5)\\新しいフォルダー (2)'
# Thực hiện xác thực bằng cách sử dụng quyền truy cập của người dùng hiện tại
#os.system(f"net use {source_folder} /user:{username} {password}")
# Lấy danh sách các tệp tin trong thư mục
file_list = os.listdir(path)

tokuisakies = [
	Tokuisaki('029007', "29007_粟井鋼商事㈱福岡営業所_____●"),
	Tokuisaki('029267', "29267_協伸メタル㈱_____●"),
	Tokuisaki('029289', "29289_㈱サンコー"),
	Tokuisaki('029494', "29494_㈱鉄鋼社　長野営業所_____●"),
	Tokuisaki('029495', "29495_㈱鉄鋼社_____●"),
	Tokuisaki('029498', "29498_㈱鉄鋼社　北関東営業所_____●"),
	Tokuisaki('029506', "29506_㈱鉄鋼社　東北営業所_____●"),
	Tokuisaki('029554', "29554_アイケーメタル㈱　狭山営業所___●"),
	Tokuisaki('029571', "29571_協同組合　島根県鐵工会　出雲営業所_____●"),
	Tokuisaki('029698', "29698_㈱林角本店　非鉄金属部___●"),
	Tokuisaki('029806', "29806_富源商事㈱　上越支店____●"),
	Tokuisaki('029879', "29879_萬世興業㈱　本社_____●"),
	Tokuisaki('029886', "29886_萬世興業㈱　日光営業所_____●29879本社へ"),
	Tokuisaki('029896', "29896_保田特殊鋼㈱本社_____●"),
]
for tokuisaki_code in tokuisakies:
    #print(tokuisaki_code.tokuisaki_code, tokuisaki_code.folder_name)  
    
    source_folder = f"C:\\Users\\DSP189\Desktop\\新しいフォルダー (5)\\新しいフォルダー (2)\\{tokuisaki_code.tokuisaki_code}\\PDF"
    print(source_folder)    
    
        


# Đường dẫn đến thư mục mà chúng ta muốn sao chép file PDF đến
    destination_folder = r"C:\\Users\\DSP189\\Desktop\\新しいフォルダー (5)\\新しいフォルダー"
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
            shutil.copy(pdf_source_path, destination_path)
            print(f"Sao chép {filename} vào {destination_path}")