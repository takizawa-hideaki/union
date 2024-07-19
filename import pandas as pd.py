import pandas as pd
import psycopg2
from datetime import datetime, timedelta
import os

def kiem_tra_ngay_moi(ngay_cuoi_cung):
    ngay_hien_tai = datetime.now().date()
    return ngay_hien_tai > ngay_cuoi_cung

def ghi_vao_excel(ten_tep_excel, df, cot_ghi, dong_ghi):
    with pd.ExcelWriter(ten_tep_excel, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        df.to_excel(writer, index=False, sheet_name='Ten_Bang')
        writer.sheets['Ten_Bang'][f'{cot_ghi}{dong_ghi}'] = gia_tri_can_lay

def main():
    ten_bang = 'offc_trn_hazai_nyushuko'
    dieu_kien = "nyushuko_date= to_char(current_timestamp+cast('-1days' as interval),'yyyy/mm/dd')--where nyushuko_date = '2023/12/02' and not hazai_office_factory_code in('590','101') group by hazai_office_factory_code order by hazai_office_factory_code"
    ten_tep_excel = '工場別端材入出庫数_2023 .xlsx - ショートカット.xlsx'
    cot_ghi = 'C'

    # Kiểm tra xem đã sang ngày mới chưa
    if os.path.exists(ten_tep_excel):
        df_cu = pd.read_excel(ten_tep_excel, sheet_name='12月')
        ngay_cuoi_cung = pd.to_datetime(df_cu['Ngay']).max().date()
        if not kiem_tra_ngay_moi(ngay_cuoi_cung):
            print("Chưa sang ngày mới. Không cần ghi dữ liệu mới.")
            return
        else:
            dong_ghi_moi = len(df_cu) + 1  # Lấy số dòng hiện có và tăng thêm 1 để ghi vào dòng tiếp theo
    else:
        dong_ghi_moi = 11  # Nếu tệp Excel chưa tồn tại, bắt đầu từ dòng 11

    # Kết nối đến cơ sở dữ liệu
    conn = psycopg2.connect(host ="192.168.160.83",
                         database="union_hanbai",
                         user = "unionplate",
                         password = "etalpnoinu")
    query = f"SELECT hazai_office_factory_code,count(nyushuko_cf='1' or null) as in,count(nyushuko_cf='2' or null) as out FROM {ten_bang} WHERE dieu_kien = '{dieu_kien}'"
    
    # Đọc dữ liệu từ cơ sở dữ liệu vào DataFrame
    df_moi = pd.read_sql_query(query, conn)

    # Lấy giá trị từ dòng đầu tiên của DataFrame
    gia_tri_can_lay = df_moi.iloc[0]['in']  # thay 'ten_cot_muon_lay' bằng tên cột bạn muốn lấy giá trị

    # Đặt ngày mới và dòng ghi mới vào DataFrame mới
    df_moi['Ngay'] = datetime.now().date()
    dong_ghi_moi_df = pd.DataFrame({'Dong_Ghi': [dong_ghi_moi]})
    df_moi = pd.concat([df_moi, dong_ghi_moi_df], axis=1)

    # Ghi vào Excel
    ghi_vao_excel(ten_tep_excel, df_moi, cot_ghi, dong_ghi_moi)

    # Đóng kết nối đến cơ sở dữ liệu
    conn.close()

if __name__ == "__main__":
    main()
