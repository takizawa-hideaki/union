import win32com.client
import os
import imaplib
import email
from email.header import decode_header
from datetime import datetime

# Outlook情報取得：
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
inbox = outlook.GetDefaultFolder(6)  # 受信トレイをみる（デフォルトが受信トレイは　No.6）
messages = inbox.Items

# 自分のメールをIMAPで接続する：
mail_server = "union-plate.cybermail.jp"
username = "r-tong@union-plate.co.jp"
password = "q9EH2j4t"
#ログイン、受信トレイ見る：
mail = imaplib.IMAP4_SSL(mail_server)
mail.login(username, password)
mail.select("inbox")

# どこからのメールを処理するか：
target_email_address = "r-tong@union-plate.co.jp"
# 取り出した添付ファイルをどこに保存するか：
folder_path = r"\\192.168.160.6\Union-FileSV\共通ファイル_Ⅱ\営業本部\システム\test"

#IMAP4サーバーでメールボックスを検索し、すべてのメールのIDを取得：
#result, data = mail.search(None, "UNSEEN")
#email_ids = data[0].split()
result, data = mail.search(None, "UNSEEN")
if result == "OK":
    email_ids = data[0].split()
    for email_id in email_ids:
        # Xử lý các email chưa đọc ở đây
        pass
else:
    print("Không thể tìm thấy email chưa đọc.")


for email_id in email_ids:
    result, data = mail.fetch(email_id, "(RFC822)") #電子メールIDに基づいて電子メールデータを取得する。
    raw_email = data[0][1]
    msg = email.message_from_bytes(raw_email) #、電子メールデータをバイトから EmailMessage オブジェクトに変換する。

    sender = msg["From"] #電子メールの送信者情報を取得する。
    if target_email_address not in sender: #送信者が目標の電子メールアドレスでないかどうかをチェックします。もしそうでなければ、次の電子メールに進みる。
        continue

    subject = decode_header(msg["Subject"])[0][0] #電子メールの件名をデコードする（エンコードされている場合）。
    if isinstance(subject, bytes):
        subject = subject.decode()

    print("Subject:", subject) #電子メールの件名を出力する。

    for part in msg.walk(): #添付ファイルあるかどうか：
        if part.get_content_maintype() == "multipart": # 各パート（メッセージの一部）が multipart (複数の異なる部分) でなく、
            continue
        if part.get("Content-Disposition") is None: #Content-Disposition(HTTPやMIMEのヘッダーで使用されるフィールド) が設定されている場合にのみ
            continue
        
        filename = part.get_filename()

        if filename:
            current_day =datetime.now().strftime("%Y%m%d%H%M%S") #取り出したフィルに日付、時間付ける。
            name, ext = os.path.splitext(filename) #ファイル名分解する。
            new_filename = f"{name}_{current_day}{ext}" #新しいファイル名を生成し、そのファイルパスを使用して、添付ファイルを指定されたフォルダに保存します。
            if not os.path.exists(folder_path):#もしフォルダーなければパースによって作る：
                os.mkdir(folder_path)
            filepath = os.path.join(folder_path, new_filename)
            open(filepath, "wb").write(part.get_payload(decode=True))
    # Đánh dấu email này là đã xử lý
    mail.store(email_id, '+FLAGS', '\\Seen')

mail.close()
mail.logout()
