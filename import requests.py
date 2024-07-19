import json
import base64
import urllib.request
count = 0
# Thông tin xác thực và cấu hình của ứng dụng Kintone
DOMAIN = 'union-plate'## kintoneのドメイン
LOGIN = "659oda"## ログイン名
PASS = "union659"## パスワード
appno = 1167## 取得したいアプリのアプリNo
uri = "https://" + DOMAIN + ".cybozu.com/k/v1/record.json"
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

# Thêm tham số vào yêu cầu DELETE
body = {
  'app': appno,
  'ids': [0,918],
  
}

# HTTP　リクエスト作成
req = urllib.request.Request(
        url=uri,
        data=json.dumps(body).encode(),# "body" :JSONに変換
        headers=headers,
        method="DELETE"
    )
 #kintoneにリクエストする
try:
                response = urllib.request.urlopen(req)
                res_dict = json.load(response)
                count+=1
                print(res_dict)  # kintone から帰還表示
except urllib.error.URLError as e:
                if hasattr(e, "reason"):
                        print("Failed to reach the server:", e.reason)
                elif hasattr(e, 'code'):
                        print('The server couldn\'t fulfill the request.', e.code)