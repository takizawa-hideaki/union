#import csv
import requests



"""----------------------------------------------------------------"""


# Thông tin của Kintone
domain = 'union-plate'
app_id = '1167'
api_token = 'dvPYLYJ8RnArbsChKQg3yHVTSK4neGSw0SIJ9x4l'
#full_path = r"C:\\Users\\DSP189\\Desktop\\新しいフォルダー (2)\\240115.csv"



# Gửi dữ liệu lên Kintone
url = f'https://{domain}.cybozu.com/k/v1/records.json'
headers = {
    'Content-Type': 'application/json',
    'X-Cybozu-API-Token': api_token,
}

## フィールド部分のbodyのリスト
body_fields = []

## 文字列１行
temp_body = {
    "文字列__1行_":{"value":"1件登録"}
}
body_fields.append(temp_body)

## 文字列複数行
temp_body = {
    "文字列__複数行_":{"value":"1行目\n2行目"}
}
body_fields.append(temp_body)

## 数値
temp_body = {
    "数値":{"value":"17"}
}
body_fields.append(temp_body)

## 日時 日本の時刻にするには9時間プラスする
temp_body = {
    "日時":{"value":"2023-02-11T18:08:24+09:00"}
}
body_fields.append(temp_body)

## チェックボックス
temp_body = {
    "チェックボックス":{"value":["sample1", "sample2"]}
}
body_fields.append(temp_body)

## ドロップボックス
temp_body = {
    "ドロップダウン":{"value":"sample1"}
}
body_fields.append(temp_body)

## リンク　web
temp_body = {
    "リンク":{"value":"https://cybozu.co.jp/"}
}
body_fields.append(temp_body)

## テーブル
temp_body = {
    "テーブル":{"value":
            [
                {"value":
                    {"文字列__1行__0":{"value":"1行目"},
                    "数値_0":{"value":1}
                    }
                },
                {"value":
                    {"文字列__1行__0":{"value":"2行目"},
                    "数値_0":{"value":2}
                    }
                }
            ]
            }
}
body_fields.append(temp_body)

## 全てのフィールドを辞書型として結合する
body_field = {}
for item_dict in body_fields:
     body_field = {**body_field, **item_dict}

## record部分のbody　フィールドの内容を辞書型で結合
body_record = {"record":body_field}

## アプリ番号部分のbody
body_app = {
    "app":app_id
}

## body全体を辞書型として作成する
body = {**body_app, **body_record}
print(body)


response = requests.post(url, headers=headers, json=body)

if response.status_code == 200:
    print("Dữ liệu đã được tải lên Kintone thành công.")
else:
    print(f"Lỗi khi tải lên Kintone. Mã lỗi: {response.status_code}")
    print(response.text)


