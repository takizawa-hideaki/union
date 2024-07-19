#vao file co san 
import psycopg2
import pandas as pd
import datetime
import openpyxl
from openpyxl import load_workbook
from sqlalchemy import create_engine

# Thông tin kết nối đến cơ sở dữ liệu PostgreSQL
conn = psycopg2.connect(
    database="linh_work",
    user="linh",
    password="union4001",
    host="192.168.160.189",
    port="5432"
)
# SQL query to retrieve data
query = """select hazai_office_factory_code,count(nyushuko_cf='1' or null) as in,count(nyushuko_cf='2' or null) as out
             from offc_trn_hazai_nyushuko
               where nyushuko_date= to_char(current_timestamp+cast('-1days' as interval),'yyyy/mm/dd') 
                    and not hazai_office_factory_code in('590','101')  
                        group by hazai_office_factory_code
                          order by hazai_office_factory_code"""
# Read data from the database into a DataFrame
df = pd.read_sql_query(query, conn)
# Close the connection
conn.close()

# Load the Excel file and existing sheet
excel_file = 'example.xlsx'  # Replace with the path to your existing Excel file
sheet_name = 'Sheet1'  # Replace with the name of the existing sheet

# Load the workbook
book = load_workbook(excel_file)

db_url = f"postgresql+psycopg2://{'linh'}:{'union4001'}@{'192.168.160.189'}/{'linh_work'}"

# Tạo đối tượng kết nối
engine = create_engine(db_url)

# Select the sheet
writer = pd.ExcelWriter(excel_file, engine)
writer.book = book

# Write the DataFrame to the existing sheet
df.to_excel(writer, sheet_name=sheet_name, index=False)

# Save the changes
writer.save()

