import psycopg2
import pandas as pd
import datetime
import openpyxl

# Thông tin kết nối đến cơ sở dữ liệu PostgreSQL
conn = psycopg2.connect(
    database="linh_work",
    user="linh",
    password="union4001",
    host="192.168.160.189",
    port="5432"
)
# Truy vấn SQL để lấy dữ liệu
query = """select hazai_office_factory_code,count(nyushuko_cf='1' or null) as in,count(nyushuko_cf='2' or null) as out
             from offc_trn_hazai_nyushuko
               where nyushuko_date= to_char(current_timestamp+cast('-1days' as interval),'yyyy/mm/dd') 
                    and not hazai_office_factory_code in('590','101')  
                        group by hazai_office_factory_code
                          order by hazai_office_factory_code"""
# Đọc dữ liệu từ cơ sở dữ liệu và đưa vào DataFrame
df = pd.read_sql(query, conn)
# Đóng kết nối
conn.close()
# Xuất dữ liệu ra tệp Excel
df.to_excel('example4.xlsx', index=False)