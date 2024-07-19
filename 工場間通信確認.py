import psycopg2
import time
# Tạo từ điển ánh xạ giữa host và tên đại diện
host_mapping = {
    '192.168.162.51': '本社工場',
    '192.168.162.61': '本社FC工場',
    '192.168.161.51': '上田工場',
    '192.168.10.51': 'INステンレス',
    '192.168.11.51': '藤精工',
    '192.168.13.51': 'サンテック',
    '192.168.14.51': 'MK精工',
    '192.168.15.51': '渡辺製作所',
    '192.168.16.51': 'UPM',
    '192.168.17.51': '尾道工場',
    '192.168.17.61': '尾道アルミ',
    '192.168.18.51': '厚木工場',
    '192.168.19.51': 'MTS',
    '192.168.20.51': 'AUK',
    '192.168.20.61': 'AUKアルミ',
    '192.168.22.61': '峰岸商会',
    '192.168.23.51': 'メカニックメタル',
    '192.168.24.51': '鈴木鋼管鋼業',
    '192.168.28.51': '千曲工場',
    '192.168.25.51': '小牧工場',
    '192.168.22.51': '峰岸加工工場',
    
    # Thêm các ánh xạ khác nếu cần thiết
}

def ket_noi_database(host, database, user, password, port):
    try:
        ten_dai_dien = host_mapping.get(host, host)
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
        print(f"工場間通信： {host} : {ten_dai_dien} . アクセスできました。")
        return conn
    except psycopg2.Error as e:
        print(f"アクセスできませんでした。: {e}")
        return None

def thuc_hien_thao_tac(conn, ten_dai_dien):
    
    if conn:
        try:
            # Thực hiện các thao tác với cơ sở dữ liệu ở đây
            cursor = conn.cursor()
            cursor.execute("""SELECT request_date, transmission_serial_no, upper_request_code, lower_request_code, key_item, request_type, execute_flag, complete_flag, datafile_name, staff_code, create_date, create_time, update_date, update_time
                            FROM fact_thrd_transmission_request where request_date= to_char(current_timestamp,'YYYY/MM/DD') 
                           order by (transmission_serial_no, create_date, create_time, update_date, update_time) desc  
                           limit 10""")
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        finally:
            # Đóng kết nối
            conn.close()

def main():
    # Thông tin kết nối đến các PostgreSQL hosts
    hosts = [
        {'host': '192.168.162.51', 'database': 'union_factory', 'user': 'unionfactory', 'password': 'yrotcafnoinu', 'port': '5432'},
        {'host': '192.168.162.61', 'database': 'union_factory', 'user': 'unionfactory', 'password': 'yrotcafnoinu', 'port': '5432'},
        {'host': '192.168.161.51', 'database': 'union_factory', 'user': 'unionfactory', 'password': 'yrotcafnoinu', 'port': '5432'},
        {'host': '192.168.10.51', 'database': 'union_factory', 'user': 'unionfactory', 'password': 'yrotcafnoinu', 'port': '5432'},
        {'host': '192.168.11.51', 'database': 'union_factory', 'user': 'unionfactory', 'password': 'yrotcafnoinu', 'port': '5432'},
        {'host': '192.168.13.51', 'database': 'union_factory', 'user': 'unionfactory', 'password': 'yrotcafnoinu', 'port': '5432'},
        {'host': '192.168.14.51', 'database': 'union_factory', 'user': 'unionfactory', 'password': 'yrotcafnoinu', 'port': '5432'},
        {'host': '192.168.15.51', 'database': 'union_factory', 'user': 'unionfactory', 'password': 'yrotcafnoinu', 'port': '5432'},
        {'host': '192.168.16.51', 'database': 'union_factory', 'user': 'unionfactory', 'password': 'yrotcafnoinu', 'port': '5432'},
        {'host': '192.168.17.51', 'database': 'union_factory', 'user': 'unionfactory', 'password': 'yrotcafnoinu', 'port': '5432'},
        {'host': '192.168.17.61', 'database': 'union_factory', 'user': 'unionfactory', 'password': 'yrotcafnoinu', 'port': '5432'},
        {'host': '192.168.18.51', 'database': 'union_factory', 'user': 'unionfactory', 'password': 'yrotcafnoinu', 'port': '5432'},
        {'host': '192.168.19.51', 'database': 'union_factory', 'user': 'unionfactory', 'password': 'yrotcafnoinu', 'port': '5432'},
        {'host': '192.168.20.51', 'database': 'union_factory', 'user': 'unionfactory', 'password': 'yrotcafnoinu', 'port': '5432'},
        {'host': '192.168.20.61', 'database': 'union_factory', 'user': 'unionfactory', 'password': 'yrotcafnoinu', 'port': '5432'},
        {'host': '192.168.22.61', 'database': 'union_factory', 'user': 'unionfactory', 'password': 'yrotcafnoinu', 'port': '5432'},
        {'host': '192.168.23.51', 'database': 'union_factory', 'user': 'unionfactory', 'password': 'yrotcafnoinu', 'port': '5432'},
        {'host': '192.168.24.51', 'database': 'union_factory', 'user': 'unionfactory', 'password': 'yrotcafnoinu', 'port': '5432'},
        {'host': '192.168.28.51', 'database': 'union_factory', 'user': 'unionfactory', 'password': 'yrotcafnoinu', 'port': '5432'},
        {'host': '192.168.25.51', 'database': 'union_factory', 'user': 'unionfactory', 'password': 'yrotcafnoinu', 'port': '5432'},
        {'host': '192.168.22.51', 'database': 'union_factory', 'user': 'unionfactory', 'password': 'yrotcafnoinu', 'port': '5432'},
        # Thêm các thông tin kết nối khác nếu cần
        
    ]

    while True:
        for host_info in hosts:
            conn = ket_noi_database(**host_info)
            thuc_hien_thao_tac(conn, host_info['host'])

            # Ngủ 5s trước khi thực hiện kết nối tiếp theo
            time.sleep(5)


if __name__ == "__main__":
    main()
