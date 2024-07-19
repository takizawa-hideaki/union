
'''
    sheet_font.py
    purpose: read xlsx and set font automatically
'''

import openpyxl as xl
from openpyxl.styles import Font


# set input file name
inputfile = r'C:\Users\DSP189\Desktop\test\営業本部明細入力数_202403.xlsx'

# read input xlsx
wb1 = xl.load_workbook(filename=inputfile)


# set font
font = Font(name='游ゴシック')

for ws1 in wb1.worksheets:
    for row in ws1:
        for cell in row:
            ws1[cell.coordinate].font = font

# save xlsx file
wb1.save(inputfile)
