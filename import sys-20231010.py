import sys
import psycopg2
import datetime
from datetime import timedelta
import openpyxl
wb = openpyxl.Workbook()
ws = wb.active
current_date = datetime.date(2023, 11, 13)
t = datetime.datetime.now()
# Ví dụ: Tạo vòng lặp và chèn dữ liệu
input_detail =[['corporation_code','office_factory_code','yy_mm_dd','online_create_date','online_create_time','add_juchu_volume','jogai_shiyo_cf','jogai_size_block_no','jogai_flag','create_date','create_time','create_staff']]
print (input_detail)
for i in range(3):
        current_date += timedelta(days=1)

        input_detail2 = ['54', '540',(current_date.strftime("%Y/%m/%d")),(t.strftime("%Y/%m/%d")),(t.strftime("%H:%M:%S.%f")[:12]),'5000','6F', '0', '1',(t.strftime("%Y/%m/%d")),(t.strftime("%H:%M:%S")),'トムズイリン']
        print (input_detail2)
  

 

