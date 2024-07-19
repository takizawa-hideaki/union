import poplib
from email.parser import BytesParser
from email.policy import default
import os
from datetime import datetime, timedelta
import re
from email.utils import parseaddr
import pandas as pd
from email.errors import HeaderParseError

def sanitize_filename(filename):
    """
    ファイル名に使用できない文字を安全な文字に置換する（サニタイズする）。
    
    Args:
        filename (str): サニタイズする前のファイル名。
    
    Returns:
        str: サニタイズ後のファイル名。
    """
    # ファイル名に使用できない文字をアンダースコアに置換
    return re.sub(r'[\\/*?:"<>|]', '_', filename)

def save_email(msg, folder_path):
    """
    メールの内容をテキストファイルに保存する。
    
    Args:
        msg (email.message.EmailMessage): メールオブジェクト。
        folder_path (str): 保存先フォルダのパス。
        index (int): メールのインデックス番号。
    """
    # メールの件名を取得し、ファイル名に使用。件名がない場合は無題とする
    subject = msg.get('Subject', 'subjectless')
    # メールの件名が存在するかどうかを確認
    if subject:
        subject_filename = sanitize_filename(subject)
    else:# 件名が存在しない場合、「subjectless.txt」とする。
        subject_filename = f'subjectless'
    # ファイルのフルパスを設定する
    file_path = os.path.join(folder_path, f'{subject_filename}.txt')
    # メールの内容をファイルに書き込み
    with open(file_path, 'w', encoding='utf-8') as f:
        for header, value in msg.items():
            f.write(f"{header}: {value}\n")
        # ヘッダと本文の間に空行を挿入
        f.write("\n")  
        # メールの本文を書き込み
        if msg.is_multipart():
            # マルチパートのメールの場合、各パートを処理
            for part in msg.walk():
                # 最初のテキストパートの内容を書き込み
                if part.get_content_type() == 'text/plain':
                    emailbody = part.get_payload(decode=True).decode(part.get_content_charset(), 'ignore')
                    f.write(emailbody)
                    break   # 最初のテキストパートのみを処理
        else:
            # シングルパートのメールの場合、直接内容を書き込み
            emailbody = msg.get_payload(decode=True).decode('utf-8', 'ignore')
            f.write(emailbody)

def pop_mail(
    pop_server, 
    email_user, 
    email_password, 
    base_download_folder,
    processed_emails=None
):
    """
    POP3を使ってメールを受信し、メールと添付ファイルをダウンロードする。
    
    Args:
        pop_server (str): POPサーバのアドレス。
        email_user (str): メールのユーザー名。
        email_password (str): メールのパスワード。
        base_download_folder (str): ダウンロードの基本フォルダパス。
        delete_mail (bool): ダウンロード後にメールを削除するかどうか。
    """
    #POP3 サーバへの接続: poplib.POP3_SSL を使用し
    #処理済みメールの処理: processed_emails を空のセットとして初期化します。これは、処理済みメールの ID を格納するためのものです。
    if not isinstance(processed_emails, (set, list)):
        processed_emails = set()
    mail = poplib.POP3_SSL(pop_server)
    mail.user(email_user)
    mail.pass_(email_password)
    # メールボックス内のメッセージ数を取得
    num_messages = len(mail.list()[1])

    # 先週の開始日と終了日を確認
    end_date = datetime.now()
    start_date = end_date - timedelta(days=1)
    # ファイルが存在しない場合は作成します
    if not os.path.exists(processed_emails_file):
        with open(processed_emails_file, 'w') as f:
            pass  # 必要に応じてファイルを空にするか、初期コンテンツを書き込みます
#'processed_emails_file' というファイルを読み込み、その内容を processed_emails というセットに追加します。ファイル内の各行は、.strip() を使用して先頭および末尾の空白を取り除いた後、セットに追加されます。
    else:
        with open(processed_emails_file, "r") as f:
            processed_emails.update(line.strip() for line in f.readlines())  # ファイル内の行からコレクションを作成する
#num_messages 回の反復処理を行います。各メッセージについて、mail.retr() を使用してメッセージを取得し、BytesParser() を使用してバイト列をパースし、メッセージオブジェクト msg を作成します。
    for i in range(num_messages):
        response, lines, octets = mail.retr(i + 1)
        msg_bytes = b'\r\n'.join(lines)
        
        msg = BytesParser(policy=default).parsebytes(msg_bytes)
        block_emails = {'@email.bing.com'}
        # 特定の送信元ドメイン'Microsoft'に関連するメールをブロックするためのドメインのセットを作成します。
        sender_name, sender_email = parseaddr(msg.get('From'))
        if any(domain in sender_email for domain in block_emails):
        # block_emails セット内のドメインのいずれかに一致する場合は、そのメールを処理せずに次のメールに進みます。
            continue
        # メールアドレスから不正な文字（<>,[]）を削除し、有効なメールアドレスを取得します
        valid_email = re.sub(r'[<>\[\]]', '', sender_email)

# メールアドレスが有効かどうかを確認
        if '@' in valid_email:
            obs_local_part = valid_email.split('@')[0]
            if obs_local_part and obs_local_part[0] == '.':
        # obs_local_part の最初の要素の token_type が「dot」の場合、電子メールを無視します
                continue
        else:
    # 電子メール アドレスが無効です。この電子メールの処理をスキップします
                continue
        date_str = msg.get('Date')
        if date_str:     
        #メッセージの受信日時を取得し、タイムゾーン情報を削除してローカル時刻として扱うための処理を行っています。
            received_date = datetime.strptime(msg.get('Date'), '%a, %d %b %Y %H:%M:%S %z')
            received_date = received_date.replace(tzinfo=None)
        else:
            received_date = datetime.now()


        # メールが先週以内に受信されたかどうかを確認する
        if start_date <= received_date <= end_date:
            
            #メールのヘッダーから、メールのID（Message-ID）を取得します。このIDは、メールを一意に識別するためのものであり、通常はメールサーバーが生成します。
            email_id = msg.get('Message-ID')
            #取得したメールのIDが processed_emails セットに含まれている場合は、そのメールはすでに処理されているため、次のメッセージに進みます。
            if email_id in processed_emails:
                
                continue
            
            #メッセージが複数の部分から構成されているかどうかをチェックします。メールが複数の部分（たとえば、本文と添付ファイル）から構成されている場合は True を返します。
            if msg.is_multipart():
                has_attachment = False 

                for part in msg.walk():  
                    # コンテントディスポジションを確認（ファイルをWEBページとして表示するか、ダウンロードさせるかを指定するためのheader）                  
                    content_disposition = part.get("Content-Disposition", None)
                    if content_disposition:
                        # 添付ファイルまたはインライン画像の場合、ファイルをダウンロード 
                        if any(dispo in content_disposition for dispo in ['attachment', 'inline']) or part.get_content_maintype() == 'image':
                            # 添付ファイルのファイル名を取得
                            filename = part.get_filename()
                            sender_name, sender_email = parseaddr(msg.get('From'))#送信先取得
                            txt_save_folder = r"C:\Users\DSP189\Downloads\test"#保存フォルダーへ
                            if filename:#'excel file'だけ処理する
                                excel_file = {'.xlsx','.xls','.xlsm'}
                                if any(extension in filename for extension in excel_file):
                                    folder_name = datetime.now().strftime('%Y%m%d_%H%M%S_') + sender_email
                                    folder_path = os.path.join(base_download_folder, folder_name)
                                    os.makedirs(folder_path, exist_ok=True)
                                    has_attachment = True
                                    received_time = received_date.strftime("%Y%m%d%H%M%S")
                                    name, ext = os.path.splitext(filename) #ファイル名分解する。
                                    new_filename = f"{name}_{received_time}{ext}"
                                    
                                    # 親ディレクトリが存在しない場合は作成する
                                    filepath = os.path.join(folder_path, sanitize_filename(new_filename))
                                

                                    with open(filepath, 'wb') as f:
                                        f.write(part.get_payload(decode=True))
                                    print(f"添付ファイル保存しました。: {filepath}")
# 保存したいシートの名前
                                    sheet_name = 'CSV'

# シートからデータを DataFrame に読み取ります
                                    df = pd.read_excel(filepath, sheet_name=sheet_name)
                                    value_c2 = df.iloc[0, 2] 
                                    txt_filename = f"{value_c2}_{received_time}.txt"                            
                                
# 保存したいCSVファイルへ
                                    
                                    txt_folder_name = received_date.strftime("%Y_%m")
                                    txt_folder_path = os.path.join(os.getcwd(), txt_save_folder  , txt_folder_name)		
                                    if not os.path.exists(txt_folder_path):								#月のフォルダーなければ作成
                                        os.makedirs(txt_folder_path)
                                        print("フォルダー作成しました:", txt_folder_path)
                                    full_path = os.path.join(txt_save_folder , txt_folder_path, txt_filename)

# データフレームをCSVファイルに書き込み
                                    df.to_csv(full_path, sep='\t', index=False, encoding='cp932')

                                    print(f"シート '{sheet_name}'{txt_filename}ファイルに正常に保存されました.")
                                else:
                                    
                                    continue
                    
    
                # 処理されたメールのリストを保存する             
                if has_attachment: 
                    save_email(msg, folder_path)
                    processed_emails.add(email_id)
            os.makedirs(os.path.dirname(processed_emails_file), exist_ok=True)
            with open(processed_emails_file, "w") as f:
                f.write("\n".join(processed_emails))
                
           
           

            
            
            
           

    mail.quit()
    return processed_emails
    


if __name__ == "__main__":

    # テスト用のパラメータを設定
    pop_server = "union-plate.cybermail.jp"    # POPサーバのアドレスを設定
    email_user = "r-tong@union-plate.co.jp"       # メールのユーザー名を設定
    email_password = "q9EH2j4t"     # メールのパスワードを設定
    download_folder = r"C:\Users\DSP189\Desktop\test"  # ダウンロードフォルダのパスを設定
    
    # ベースとなるダウンロードフォルダが存在しない場合は作成
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # 以前に処理されたメールのリストを取得する
    processed_emails_file = os.path.join(download_folder, "processed_emails.txt")
    if os.path.exists(processed_emails_file):
        with open(processed_emails_file, "r") as f:
            processed_emails = set(f.read().splitlines())
    else:
        processed_emails = set()
    

    processed_emails = pop_mail(pop_server, email_user, email_password, download_folder, False)


 