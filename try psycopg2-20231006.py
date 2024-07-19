import psycopg2

try:
    # Kết nối đến cơ sở dữ liệu PostgreSQL
    conn = psycopg2.connect(
    host='192.168.160.83',
    database='union_hanbai',
    user='unionplate',
    password='etalpnoinu',
    port='5432'
)

    # Kiểm tra kết nối thành công
    if conn:
        print("アクセスできました。")
    
    # Đóng kết nối
    conn.close()
except Exception as e:
    print(f"アクセスできませんでした。 {str(e)}")
