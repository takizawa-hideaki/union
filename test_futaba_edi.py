from sqlalchemy import create_engine, text
# データベースへの接続用設定
database_uri = 'postgresql://unionplate:etalpnoinu@192.168.160.83:5432/union_hanbai'
engine = create_engine(database_uri)




    # Mở kết nối
try:
    # Mở kết nối và thực thi truy vấn
    with engine.connect() as connection:
        #④双葉伝送取込
        query = text("""select *
from offc_thrd_futaba_imp
where request_date=to_char(current_timestamp,'YYYY/MM/DD')
order by request_serial_no"""
				)
        
        # Thực thi truy vấn
        result = connection.execute(query)
        print("*********************************")
        # Kiểm tra xem kết quả có rỗng không
        print("'④双葉伝送取込': " )
        all_values_equal_one = True

        for row in result:
            if row[4] != 1 or row[5] != 1:
                all_values_equal_one = False
                row_with_non_one_value = row
                break

        if all_values_equal_one:
            print("OK!")
        else:
            print(row_with_non_one_value )
        #⑤双葉送信要求
        query = text("""select *
from offc_thrd_futaba_exp
where request_date=to_char(current_timestamp,'YYYY/MM/DD')
order by request_serial_no"""
				)
        
        # Thực thi truy vấn
        result = connection.execute(query)
        print("*********************************")
        # Kiểm tra xem kết quả có rỗng không
        print("'⑤双葉送信要求': " )
        all_values_equal_one = True

        for row in result:
            if row[3] != 1 or row[4] != 1:
                all_values_equal_one = False
                row_with_non_one_value = row
                break

        if all_values_equal_one:
            print("OK!")
        else:
            print(row_with_non_one_value)
        
except Exception as e:
    print("Lỗi:", e)