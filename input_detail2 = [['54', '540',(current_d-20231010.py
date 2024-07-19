import datetime
import openpyxl
wb = openpyxl.Workbook()
ws = wb.active
current_date = datetime.date(2023, 11, 13)
t = datetime.datetime.now()
input_detail2 = [['54', '540',(current_date.strftime("%Y/%m/%d")),(t.strftime("%Y/%m/%d")),(t.strftime("%H:%M:%S.%f")[:12]),'5000','6F', '0', '1',(t.strftime("%Y/%m/%d")),(t.strftime("%H:%M:%S")),'トムズイリン']]

row = len(input_detail2)
column = len(input_detail2[0])

for k in range(0,row):
        for j in range(0,column):
            v2=input_detail2[k][j]
            print(v2)
            #ws.cell(column=j+1, row=k+1, value=v2)
#for i in range(3):
      #ws.cell = ws.cell+1
#output_excel_path= './user.xlsx'
#wb.save(output_excel_path)