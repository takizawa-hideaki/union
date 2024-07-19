import datetime
from datetime import timedelta
import openpyxl

def add_data_to_excel(worksheet, data, start_row, start_column):
    for i, row in enumerate(data, start_row):
        for j, value in enumerate(row, start_column):
            worksheet.cell(column=j, row=i, value=value)

wb = openpyxl.Workbook()
ws = wb.active

current_date = datetime.date(2023, 11, 13)
t = datetime.datetime.now()

input_detail = [['corporation_code', 'office_factory_code', 'yy_mm_dd', 'online_create_date', 'online_create_time', 'add_juchu_volume', 'jogai_shiyo_cf', 'jogai_size_block_no', 'jogai_flag', 'create_date', 'create_time', 'create_staff']]

row = len(input_detail)
column = len(input_detail[0])

def for_loop(a, b, c):
    input_detail2 = a
    jogai_shiyo_cf = b
    jogai_size_block_no = c

    for i in range(2):
        for j in range(len(jogai_size_block_no[i])):
            input_detail2[6] = jogai_shiyo_cf[i]
            input_detail2[7] = jogai_size_block_no[i][j]
            print(input_detail2)
            add_data_to_excel(ws, input_detail2, i + 1, 1)

for i in range(3):
    current_date += timedelta(days=1)
    
    input_detail2 = ['54', '540', current_date.strftime("%Y/%m/%d"), t.strftime("%Y/%m/%d"), t.strftime("%H:%M:%S.%f")[:12], '5000', '6F', '0', '1', t.strftime("%Y/%m/%d"), t.strftime("%H:%M:%S"), 'トムズイリン']
    jogai_shiyo_cf = ['6G', 'SG']
    jogai_size_block_no = [[11, 10, 12], [10]]

    for_loop(input_detail2, jogai_shiyo_cf, jogai_size_block_no)
    print("#########")

    input_detail2 = ['54', '540', current_date.strftime("%Y/%m/%d"), t.strftime("%Y/%m/%d"), t.strftime("%H:%M:%S.%f")[:12], '5000', '6F', '0', '1', t.strftime("%Y/%m/%d"), t.strftime("%H:%M:%S"), 'トムズイリン']
    jogai_shiyo_cf = ['6G', 'SG']
    jogai_size_block_no = [[8, 9, 10, 11], [6, 7, 8, 9, 10]]

    for_loop(input_detail2, jogai_shiyo_cf, jogai_size_block_no)

    for k in range(0, row):
        for j in range(0, column):
            v2 = input_detail2
            print(v2, end=", ")
        print("")

# Lưu lại file Excel
output_excel_path = 'C:\\Users\\DSP189\\Downloads\\user.xlsx'
wb.save(output_excel_path)
