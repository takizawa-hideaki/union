
from sqlalchemy import create_engine, text
# データベースへの接続用設定
database_uri = 'postgresql://unionplate:etalpnoinu@192.168.160.83:5432/union_hanbai'
engine = create_engine(database_uri)




    # Mở kết nối
try:
    # Mở kết nối và thực thi truy vấn
    with engine.connect() as connection:
        # --①納品データ作成要求
        query = text("""select *
from offc_thrd_nohin_seikyu_request_head
where request_date = to_char(current_timestamp,'YYYY/MM/DD')
order by transmission_serial_no"""
				)
        
        # Thực thi truy vấn
        result = connection.execute(query)
        print("*********************************")
        # Kiểm tra xem kết quả có rỗng không
        print("'①納品データ作成要求': " )
        if not result.rowcount:
            print("OK!")
        else:
            # In ra kết quả
            for row in result:
                print(row)
        print("********************************")
        #②実行中_● 前日分の正常終了を確認
        query = text("""select *
from offc_thrd_kojokan_nohin_data_request
where request_date =to_char(current_timestamp,'YYYY/MM/DD')"""
				)
        
        # Thực thi truy vấn
        result = connection.execute(query)
        print("*********************************")
        # Kiểm tra xem kết quả có rỗng không
        print("'②実行中_● 前日分の正常終了を確認': " )
        if not result.rowcount:
            print("OK!")
        else:
            # In ra kết quả
            for row in result:
                print(row)
        print("********************************")
        #③双葉発送便未入力＞ 発送便/問合せNoが未入力のデータ検索
        query = text("""select FIJ.*, SHU.*
from offc_trn_futaba_imp_juchu as FIJ 
left join offc_trn_shuka  as SHU on FIJ.juchu_no_upper=SHU.juchu_no_upper and FIJ.juchu_no_lower=SHU.juchu_no_lower and FIJ.juchu_detail_no=SHU.juchu_detail_no
where express_toiawase_no IS NULL
and SHU.juchu_no_lower IS NOT NULL
order by FIJ.juchu_no_upper,FIJ.juchu_no_lower,FIJ.juchu_detail_no"""
				)
        
        # Thực thi truy vấn
        result = connection.execute(query)
        print("*********************************")
        # Kiểm tra xem kết quả có rỗng không
        print("'③双葉発送便未入力＞ 発送便/問合せNoが未入力のデータ検索': " )
        if not result.rowcount:
            print("OK!")
        else:
            # In ra kết quả
            for row in result:
                print(row)
        print("********************************")
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
        print("********************************")
        #⑥新光データ取込
        query = text("""select *
from offc_thrd_sdk_imp
where request_date=to_char(current_timestamp,'YYYY/MM/DD')
order by request_serial_no
"""
				)
        
        # Thực thi truy vấn
        result = connection.execute(query)
        print("*********************************")
        # Kiểm tra xem kết quả có rỗng không
        print("'⑥新光データ取込': " )
        if not result.rowcount:
            print("OK!")
        else:
            # In ra kết quả
            for row in result:
                print(row)
        print("********************************")
        #⑦　FAX送信確認
        query = text("""select *
from offc_thrd_create_fax_send_file
where request_date=to_char(current_timestamp,'YYYY/MM/DD')
and complete_flag='0'
order by request_date, request_time, transmission_serial_no
"""
				)
        
        # Thực thi truy vấn
        result = connection.execute(query)
        print("*********************************")
        # Kiểm tra xem kết quả có rỗng không
        print("'⑦ FAX送信確認': " )
        if not result.rowcount:
            print("OK!")
        else:
            # In ra kết quả
            for row in result:
                print(row)
        print("********************************")
        #⑧FAX送信エラー_●
        query = text("""select *
from offc_trn_fax_err_send_mail_control
where send_date=to_char(current_timestamp,'YYYY/MM/DD') 
and send_cf='0'
order by create_date, create_time
"""
				)
        
        # Thực thi truy vấn
        result = connection.execute(query)
        print("*********************************")
        # Kiểm tra xem kết quả có rỗng không
        print("'⑧FAX送信エラー_●': " )
        if not result.rowcount:
            print("OK!")
        else:
            # In ra kết quả
            for row in result:
                print(row)
        print("********************************")
        
    input("j:")  
                
            
except Exception as e:
    print("Lỗi:", e)