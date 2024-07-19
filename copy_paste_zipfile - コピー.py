import zipfile
import os
import datetime
import shutil


class Log :
    def __init__(self,a,b,c,d,e):
        self.host = a
        self.driver = b
        self.folder_name = c
        self.soft = d
        self.ip =e
previous_month = datetime.datetime.today().month - 1
previous_year = datetime.date.today().year  
if previous_month <= 0: 
    previous_month +=12
    previous_year = previous_year - 1
zip_date = f"{previous_year}_{previous_month}"
apache_logs = [
    Log('192.168.160.94', "D_Program Files", "Apache Software Foundation", "Tomcat 6.0","160.94"),
    Log('192.168.160.94', "D_Program Files", "Apache Software Foundation", "Apache2.2","160.94"),
    Log('192.168.160.94', "union", "officeBatBase", "exportCsv","160.94"),
    Log('192.168.160.94', "union", "officeBatBase", "officeMqReceiver","160.94"),

    
]
                
                
        
def zip_files_in_month(folder_path, zip_path, previous_month):
    files_found = False
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                # Lấy thông tin về ngày sửa đổi của tệp
                modification_date = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                # Kiểm tra xem ngày sửa đổi có trong tháng đích đến không
                if modification_date.month == previous_month:
                    zipf.write(file_path, os.path.relpath(file_path, folder_path))
                    files_found = True
    return files_found              
def delete_files_in_month(folder_path, previous_month):
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            # Lấy thông tin về ngày sửa đổi của tệp
            modification_date = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
            # Kiểm tra xem ngày sửa đổi có trong tháng đích đến không
            if modification_date.month == previous_month:
                    os.remove(file_path)
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            try:
                os.rmdir(dir_path)
            except OSError:
                pass
for log in apache_logs:
    username = 'administrator'
    password = 'Fdomain100'
# Đường dẫn đến thư mục chứa các tệp cần nén
    if log.soft == "Apache2.2" :
        destination_folder = f'\\\\192.168.160.6\\usbdisk1\\{log.ip}\\{log.driver}\\{log.folder_name}\\{log.soft}\\logs'
        folder_to_zip = f'\\\\{log.host}\\d$\\Program Files (x86)\\{log.folder_name}\\{log.soft}\\logs'
    elif log.soft == "Tomcat 6.0" : 
        folder_to_zip = f'\\\\{log.host}\\d$\\Program Files (x86)\\{log.folder_name}\\{log.soft}\\logs'
        destination_folder = f'\\\\192.168.160.6\\usbdisk1\\{log.ip}\\{log.driver}\\{log.folder_name}\\{log.soft}\\logs'        
    elif log.soft == "exportCsv" :
        destination_folder = f'\\\\192.168.160.6\\usbdisk1\\{log.ip}\\{log.soft}'
        folder_to_zip = f'\\\\{log.host}\\d$\\{log.driver}\\{log.folder_name}\\logs\\{log.soft}'
    elif log.soft == "officeMqReceiver" : 
        destination_folder = f'\\\\192.168.160.6\\usbdisk1\\{log.ip}\\{log.soft}'
        folder_to_zip = f'\\\\{log.host}\\d$\\{log.driver}\\{log.folder_name}\\logs\\{log.soft}'    
    
    if zip_files_in_month(folder_to_zip, "đường_dẫn_đến_tệp_zip", previous_month):
        os.system(f"net use {folder_to_zip} /user:{username} {password}")
        zip_name = f'{zip_date}.zip'
        zip_output_path = os.path.join(folder_to_zip, zip_name)
        zip_files_in_month(folder_to_zip, zip_output_path, previous_month)
        print("Đã nén các tệp trong cùng một tháng thành công!")
            #destination_folder = f'\\\\192.168.160.6\\usbdisk1\\{log.ip}\\test1'
       
# Sao chép tệp tin zip đến thư mục đích
        shutil.copy(zip_output_path, destination_folder)

        print(f"Đã sao chép và dán tệp tin zip vào thư mục {destination_folder}\\{zip_name}")

        # Gọi hàm để xóa các tệp trong cùng một tháng
        delete_files_in_month(folder_to_zip, previous_month)  
   
        try:
            os.remove(zip_output_path)
        except OSError as e:
            print(f"Không thể xóa tệp tin: {e.filename} - {e.strerror}")

            
        print("Đã xóa các tệp trong cùng một tháng và tệp nén zip thành công!")
    else:
        print(f"Không có tệp nào trong tháng {previous_month}.")   
