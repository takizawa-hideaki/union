import pandas as pd
from sqlalchemy import create_engine
import re
from openpyxl import load_workbook
from openpyxl.styles import Font

# Database connection setup (adjust the connection string as needed)
engine = create_engine('postgresql://unionplate:etalpnoinu@192.168.160.83:5432/union_hanbai')


# Extracted values from the table (manual extraction for demonstration purposes)
wkugai_shiyo_values = [
'川中様　　　　　　　',
'田中様　　　　　　　',
'大西様　　　　　　　',
'太陽工業　　　　　　',
'資材管理課　　　　　',
'安田　　　　　　　　',
'川口様　　　　　　　',
'時本様　　　　　　　',
'３１３３佐藤様　　　',
'ＫＳ１３０５澤村様　',
'ＬＢ　齋藤様　　　　',
'馬場様　　　　　　　',
'武本様　　　　　　　',
'谷口様　　　　　　　',
'宇高様　　　　　　　',
'大川様　　　　　　　',
'ＫＳ１３０５　澤村様',
'藤崎様　　　　　　　',
'金型開発課　　　　　',
'正木様　　　　　　　',
'上村　　　　　　　　',
'柿本様　　　　　　　',
'ＫＯ－ＩＳ　　　　　',
'調達　南様　　　　　',
'溝口　　　　　　　　',
'ＳＭ－ＭＧ９　　　　',
'専務様　　　　　　　',
'樋上様　　　　　　　',
'社長様　　　　　　　',
'橋本　　　　　　　　',
'３１３３＊佐藤様　　',
'Ｓ５７　　　　　　　',
'ＳＡＩ　　　　　　　',
'ＹＳＩ　　　　　　　',
'佐々木　　　　　　　',
'ＫＵＷＡＮＡ　　　　',
'石井　　　　　　　　',
'Ｌ７－オキトミ　　　',
'内田様　　　　　　　',
'東北電子様　　　　　',
'ピーアンドエー　　　',
'レイテック　　　　　',
'浅倉様　　　　　　　',
'藤井　　　　　　　　',
'治工具係　小野様　　',
'生技　手塚様　　　　',
'Ｋ２，Ａ０１　　　　',
'ＣＥ茂木製作所様より',
'ＳＣホルダ－　　　　',
'1233173871',
'ＬＣ　平野様　　　　',
'プレスセンター　　　',
'マエダ　　　　　　　',
'傷注意願います。　　',
'桑名様　　　　　　　',
'生技　梶原様　　　　',
'1233162976',
'1233163098',
'ＥＵＲ２３９０７ＡＴ',
'ＫＯＵＫＥ　　　　　',
'ＳＥＩＫＯ　　　　　',
'ロッキング　　　　　',
'橋本様　　　　　　　',
'生技　山本亮　　　　',
'青木昌一　　　　　　',
'牟田様　　　　　　　',
'阿比留　　　　　　　',
'高橋様　　　　　　　',
'松浦　　　　　　　　',
'ＳＭ－ＫＦ－ＭＧ９　',
'ザ鈴木　　　　　　　',
'三美テックス　　　　',
'内海様　　　　　　　',
'加藤　　　　　　　　',
'ＬＤ　堀田様　　　　',
'イマムラ　　　　　　',
'水谷　　　　　　　　',
'猪狩様　　　　　　　',
'生産技術　三浦様　　',
'田中秀　　　　　　　',
'画像選別機　　　　　',
'菅原　　　　　　　　',
'製設ー森田　　　　　',
'45292',
'ＥＵＲ２３９０７０Ｐ',
'ＩＨＩ　　　　　　　',
'Ｋ１８７１　　　　　',
'ＬＡ　齋藤様　　　　',
'藤原様　　　　　　　',
'４４０＿５８１　　　',
'Ｍ７６－００９７　　',
'原田　　　　　　　　',
'川西様　　　　　　　',
'ＭＩＤＲ　　　　　　',
'ＳＴ－Ｐ＆ランナー板',
'リンナイ－ウチヤマ　',
'小川様　　　　　　　',
'３３１３佐藤様　　　',
'吉野　　　　　　　　',
'小野様　　　　　　　',
'英田　　　　　　　　',
'金型課　梛木様　　　',
'飯塚様　　　　　　　',
'３１３２佐藤様　　　',
'3727',
'ＬＡ　岩坂様　　　　',
'ワイヤー在庫　　　　',
'京　　　　　　　　　',
'鈴木好啓様　　　　　',
'６２１０５２－５１　',
'シールドカバーＵＦＳ',
'リフティング　　　　',
'内藤様　　　　　　　',
'木村　　　　　　　　',
'田中　　　　　　　　',
'伸栄工作所様　　　　',
'坂田様　　　　　　　',
'川端様　　　　　　　',
'政岡　　　　　　　　',
'0',
'1233158359',
'Ｋ　　　　　　　　　',
'ＮＵＴ　　　　　　　',
'ＰＫＳ２３０８４ＦＥ',
'ＳＵＧＩＫＩ　　　　',
'レ－ル　　　　　　　',
'今井社長様マル本岩崎',
'寺本様　　　　　　　',
'治具　　　　　　　　',
'溶接治具　　　　　　',
'金型製造課　斉木様　',
'釣様　　　　　　　　',
'井上　　　　　　　　',
'倉茂様　　　　　　　',
'小林　　　　　　　　',
'巴里　　　　　　　　',
'曙ブレーキ藤原様　　',
'竹村様　　　　　　　',
'船曳様　　　　　　　',
'1233168116',
'１６／１８　　　　　',
'２４－０２０２７　　',
'Ａ０７７１７　　　　',
'Ｂ　　　　　　　　　',
'ＭＵＲＡＴ－ＤＳ０１',
'ＮＫＴ　　　　　　　',
'ザイウケ　　　　　　',
'マリエイト　　　　　',
'井上様　　　　　　　',
'実験課　　　　　　　',
'川島　　　　　　　　',
'市川　　　　　　　　',
'永田様　　　　　　　',
'＃１２１９８クメダ様',
'ＬＡ　内藤様　　　　',
'ＰＬＡＴＥ　　　　　',
'ＳＣホルダーＣ　　　',
'＿ＳＡＮＳＯ　　　　',

]


# Create a new Excel writer object
excel_writer = pd.ExcelWriter('お客様記事.xlsx', engine='openpyxl')

# Loop through each value and execute the query, saving each result to a new sheet
for idx, wkugai_shiyo in enumerate(wkugai_shiyo_values):
    query = f"""
    select fij.sofusaki_code, fis.sofusaki_name, fij.futaba_office_code, fth.tokuisaki_ryaku_name, count(*)
from offc_trn_futaba_imp_juchu as fij

join offc_trn_futaba_imp_juchu_hosoku as fih
on fij.futaba_juchu_no = fih.futaba_juchu_no
and fij.konyu_hachu_no = fih.konyu_hachu_no

join offc_trn_futaba_imp_juchu_sofusaki as fis
on fij.request_date = fis.request_date
and fij.request_serial_no = fis.request_serial_no
and fij.sofusaki_code = fis.sofusaki_code

join offc_mst_futaba_tokuisaki_henkan as fth
on fij.futaba_office_code = fth.futaba_office_code

where fij.user_comment = '{wkugai_shiyo}'
and fij.request_date >= '2024/01/01'

group by fij.sofusaki_code, fis.sofusaki_name, sofusaki_name, fij.futaba_office_code, fth.tokuisaki_ryaku_name
order by count desc, fij.sofusaki_code, fis.sofusaki_name, sofusaki_name, fij.futaba_office_code
    """
   
    df = pd.read_sql(query, engine)
    
    # Sử dụng tên sheet cố định với số thứ tự
    sheet_name = f'Sheet_{idx+1}'
    
    # Lưu DataFrame vào một sheet mới trong file Excel
    df.to_excel(excel_writer, sheet_name=sheet_name, index=False)

# Đóng đối tượng ghi Excel và lưu file tạm thời
excel_writer.close()

# Mở lại file Excel để thêm giá trị wkugai_shiyo vào đầu mỗi sheet
workbook = load_workbook('お客様記事.xlsx')
bold_red_font = Font(bold=True, color="FF0000")

for idx, wkugai_shiyo in enumerate(wkugai_shiyo_values):
    sheet_name = f'Sheet_{idx+1}'
    sheet = workbook[sheet_name]
    sheet.insert_rows(1)
    cell = sheet['A1']
    cell.value = wkugai_shiyo
    cell.font = bold_red_font

# Lưu lại file Excel sau khi đã thêm giá trị wkugai_shiyo
workbook.save('お客様記事.xlsx')
