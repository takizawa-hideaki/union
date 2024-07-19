## kintoneのアプリにレコードを1件登録する
## https://cybozu.dev/ja/kintone/docs/rest-api/records/add-record/
import base64
import urllib.request
import json
import csv
from datetime import datetime
import zlib
#import chardet
DOMAIN = 'union-plate'## kintoneのドメイン
LOGIN = "659oda"## ログイン名
PASS = "union659"## パスワード
appno = 1167## 取得したいアプリのアプリNo

uri = "https://" + DOMAIN + ".cybozu.com/k/v1/record.json"

## https://developer.cybozu.io/hc/ja/articles/201941754-kintone-REST-API%E3%81%AE%E5%85%B1%E9%80%9A%E4%BB%95%E6%A7%98
## パスワード認証　の部分
## LOGIN と PASSを「：」でつないでbase64でエンコード
AUTH = base64.b64encode((LOGIN + ":" + PASS).encode())

## ヘッダ作成
headers = {
    "Host":DOMAIN + ".cybozu.com:443",
    "X-Cybozu-Authorization":AUTH,
    "Content-Type": "application/json",
    "Content-Encoding": "deflate" ,
}

# Đường dẫn đến file CSV
csv_file_path = r"C:\\Users\\DSP189\\Desktop\\新しいフォルダー (2)\\2401115.csv"

# Đọc dữ liệu từ file CSV
with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
    csv_reader = csv.reader(csvfile)
    body_fields = []
    
    # Bỏ qua dòng đầu tiên
    next(csv_reader, None)
    
    # Lặp qua từng dòng và gửi dữ liệu đến Kintone
    #print (csv_reader) 
    
    for row in csv_reader:
       # print(row)
## body作成




## フィールド部分のbodyのリスト

        
        temp_body = {
    "営業本部行き先":{"value":row[0]}
}
        body_fields.append(temp_body)
## バーコード
        temp_body = {
    "バーコード":{"value":row[1]}
}
        body_fields.append(temp_body)
## 発送日コード
        temp_body = {
    "発送日コード":{"value":row[2]}
}
        body_fields.append(temp_body)
## 出荷日
        temp_body = {
    "出荷日":{"value":datetime.strptime(row[3], '%Y/%m/%d').strftime('%Y-%m-%d')}
}
        body_fields.append(temp_body)
## 特記事項　:(チェックボックス)
        checkbox_labels = ["配達品", "仕入れ品", "工場差戻し", "FAX＆製品添付", "メール＆添付", "熱処理検査表あり"]

        checkbox_values = [label for label, value in zip(checkbox_labels, row[4:10]) if value == '1']

        temp_body = {
    "特記事項": {"value": checkbox_values},
}
        temp_body.update({label: value for label, value in zip(checkbox_labels, checkbox_values)})
        body_fields.append(temp_body)
## 工場
        temp_body = {
    "ラジオボタン_0":{"value":row[10]}
}
        body_fields.append(temp_body)
## 注番
        temp_body = {
    "注番":{"value":row[11]}
}
        body_fields.append(temp_body)
## 枝番
        temp_body = {
   "枝番":{"value":row[12]}
}
        body_fields.append(temp_body)
## 工場コード
        temp_body = {
    "工場コード":{"value":row[13]}
}
        body_fields.append(temp_body)

## ミルシート処理
        temp_body = {
    "ラジオボタン":{"value":row[14]}
}
        body_fields.append(temp_body)
## ミルシート得意先コード
        temp_body = {
   "ミルシート得意先コード":{"value":row[15]}
}
        body_fields.append(temp_body)
        ## 製品仕様
        temp_body = {
            "製品仕様":{"value":row[16]}
}
        body_fields.append(temp_body)

#print("atama:",body_fields)
body_field = {}
for item_dict in body_fields:
    print (item_dict)
    body_field = {**body_field, **item_dict}
    
         


    #print("loop;", body_field)
    
#print (body_field)

#print(body_field)
## record部分のbody　フィールドの内容を辞書型で結合
body_record = {"record":body_field}

## アプリ番号部分のbody
body_app = {
    "app":appno,
    

}


## body全体を辞書型として作成する
body = {**body_app, **body_record}
print(body)
json_data = json.dumps(body).encode()
#print(json_data)
# Nén dữ liệu
#compressed_data = zlib.compress(json_data)
#decompressed_data = zlib.decompress(compressed_data)
#decoded_data = decompressed_data.decode()
#detected_encoding = chardet.detect(decoded_data)['encoding']







## リクエスト作成
req = urllib.request.Request(
            url=uri,
            data=json_data, ## body 
            headers=headers, ## header
            method="POST", ## POST
            )
## リクエスト送信　結果受け取り
try:
    response = urllib.request.urlopen(req)
    
    #received_data = response.read()
    
    #decompressed_data = zlib.decompress(received_data)
    #print(decompressed_data )
    # Xử lý dữ liệu giải nén
    #res_dict = json.loads(decompressed_data)
    #print(res_dict)
except urllib.error.URLError as e:## エラーが生じた場合は補足する
    # https://docs.python.org/ja/3/howto/urllib2.html tryの参考
        if hasattr(e, "reason"):
            res_error = (
                "We failed to reach a server." + "\n" +
                "Reason: " + e.reason + "\n"
            )
            print(res_error)
        elif hasattr(e, 'code'):
            res_error = (
                'The server couldn\'t fulfill the request.' + "\n" +
                'Error code: ', e.code + "\n"
            )
            print(res_error)
else:
    res_dict = json.load(response)
    print(res_dict)
  