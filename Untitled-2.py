import base64
import urllib.request
import json
import csv

# Thay đổi thông tin của bạn
DOMAIN = 'union-plate'
LOGIN = "659oda"
PASS = "union659"
appno = '1167'

uri = f"https://{DOMAIN}.cybozu.com/k/v1/records.json"

# Xác thực bằng API Token
AUTH = base64.b64encode((LOGIN + ":" + PASS).encode())

# Tạo header
headers = {
    "Host": f"{DOMAIN}.cybozu.com:443",
    "X-Cybozu-Authorization": AUTH,
    "Content-Type": "application/json",
}

# Đọc dữ liệu từ file CSV
csv_path = r'C:\\Users\\DSP189\\Desktop\\新しいフォルダー (2)\\240112.csv'  # Thay đổi đường dẫn tới file CSV của bạn
with open(csv_path, 'r') as csv_file:
    csv_data = list(csv.DictReader(csv_file))

# Gửi dữ liệu từ file CSV lên Kintone
payload = {
    "app": appno,
    "records": csv_data,
}

# Tạo request
req = urllib.request.Request(
    url=uri,
    data=json.dumps(payload).encode(),
    headers=headers,
    method="POST",
)

# Gửi request và nhận response
try:
    response = urllib.request.urlopen(req)
    res_dict = json.load(response)
    print(res_dict)
except urllib.error.URLError as e:
    if hasattr(e, "reason"):
        res_error = (
            "We failed to reach a server." + "\n" +
            "Reason: " + str(e.reason) + "\n"
        )
        print(res_error)
        
    elif hasattr(e, 'code'):
        res_error = (
            'The server couldn\'t fulfill the request.' + "\n" +
            'Error code: ', str(e.code) + "\n"
        )
        print(res_error)


        # In ra nội dung chi tiết của lỗi nếu có
        if hasattr(e, 'read'):
            error_content = e.read().decode('utf-8')
            print("Error content:", error_content)
        
