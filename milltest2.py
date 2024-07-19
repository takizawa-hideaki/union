



"""----------------------------------------------------------------"""





import base64
#import csv
import requests

# Thông tin về Kintone
domain = 'union-plate'
app_id = '1167'
api_token = 'dvPYLYJ8RnArbsChKQg3yHVTSK4neGSw0SIJ9x4l'
LOGIN = "659oda"
PASS = "union659"
# Xác thực bằng API Token
AUTH = base64.b64encode((LOGIN + ":" + PASS).encode())

# Đường dẫn đến file CSV
#csv_file_path = r"C:\\Users\\DSP189\\Desktop\\新しいフォルダー (2)\\240115.csv"

# Đọc dữ liệu từ file CSV
#with open(csv_file_path, 'r', newline='', encoding='cp932') as csvfile:
   # csv_reader = csv.reader(csvfile)
    
    # Bỏ qua dòng đầu tiên
    #next(csv_reader, None)
    
    # Lặp qua từng dòng và gửi dữ liệu đến Kintone
    #for row in csv_reader:
        # Xây dựng dữ liệu theo định dạng của Kintone
data = {
            "app": app_id,
            "record": {# Cot A:ラジオボタン
                "営業本部行き先": {"value": ['営業3部']},  # Thay "Field1" bằng tên trường thực tế trong Kintone
                # Cot B :"文字列__1行_" 
                #"バーコード": {"value": "24011510410601"},  # Thay "Field2" bằng tên trường thực tế trong Kintone
                # Cot C :"文字列__1行_"
                #"発送日コード" : {"value": "20240118"},
                # Cot D :"文字列__1行_"
                # "出荷日": {"value": "2024/1/18"},
                # 特記事項 : チェックボックス
                #"特記事項" : { "value": "配達品"},
                #工場 : ラジオボタン
                "ラジオボタン_0" : {"value": ['尾道工場']},
                #注番: "文字列__1行_"
                #"注番" : {"value": "104106"},
                #枝番: "文字列__1行_"
                #"枝番" : {"value":"01"},
                              
                #"工場コード"  :  ルックアップ         
                #"工場コード" : {"value": "10580"},
                #ミルシート処理 : "ラジオボタン"
               "ラジオボタン" : {"value": ['製品添付']},
                # "ミルシート得意先コード": "文字列__1行_"
                #"ミルシート得意先コード" : {"value": "29745"},
                #"製品仕様" : "文字列__1行_"
                #"製品仕様" : {"value": "SS400 53.00 * 300.00 * 300.00 = 4"},

                
                

                # ... Thêm các trường khác tương ứng
                }
            }
        
        
        # Gửi dữ liệu đến Kintone
response = requests.post(f'https://{domain}.cybozu.com/k/v1/records.json', ## ヘッダ作成
headers = {
    "Host":domain + ".cybozu.com:443",
    "X-Cybozu-Authorization":AUTH,
    "Content-Type": "application/json",
}
, json=data)
        ## body作成
        # Kiểm tra phản hồi từ Kintone
if response.status_code == 200:
            print(f"Record added successfully: ")
else:
            print(f"Failed to add record:")
            print(response.text)
