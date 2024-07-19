import poplib
from email.parser import BytesParser
from email.policy import default
import os
from datetime import datetime, timedelta
import re

def sanitize_filename(filename):
    """
    Hàm này sẽ thực hiện việc xử lý chuỗi filename để tránh các ký tự không hợp lệ cho tên file.
    """
    return re.sub(r'[\\/*?:"<>|]', '_', filename)

def save_email(msg, folder_path):
    """
    Hàm này sẽ lưu nội dung email vào một file văn bản.
    """
    subject = msg.get('Subject', 'subjectless')

    if subject:
        subject_filename = sanitize_filename(subject)
    else:
        subject_filename = f'subjectless'

    file_path = os.path.join(folder_path, f'{subject_filename}.txt')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        for header, value in msg.items():
            f.write(f"{header}: {value}\n")
        
        f.write("\n")  

        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    emailbody = part.get_payload(decode=True).decode(part.get_content_charset(), 'ignore')
                    f.write(emailbody)
                    break
        else:
            emailbody = msg.get_payload(decode=True).decode('utf-8', 'ignore')
            f.write(emailbody)

def pop_mail(
    pop_server, 
    email_user, 
    email_password, 
    base_download_folder,
    processed_emails=None
):
    if processed_emails is None:
        processed_emails = set()

    mail = poplib.POP3_SSL(pop_server)
    mail.user(email_user)
    mail.pass_(email_password)

    num_messages = len(mail.list()[1])

    # Xác định ngày bắt đầu và ngày kết thúc của khoảng thời gian 2 ngày trở lại đây
    end_date = datetime.now()
    start_date = end_date - timedelta(days=2)

    for i in range(num_messages):
        response, lines, octets = mail.retr(i + 1)
        msg_bytes = b'\r\n'.join(lines)
        msg = BytesParser(policy=default).parsebytes(msg_bytes)

        email_id = msg.get('Message-ID')
        if email_id in processed_emails:
            continue

        received_date = datetime.strptime(msg.get('Date'), '%a, %d %b %Y %H:%M:%S %z')
        received_date = received_date.replace(tzinfo=None)

        if start_date <= received_date <= end_date and msg.get('From') == sender_email:
            folder_name = datetime.now().strftime('%Y%m%d_%H%M%S_') + str(i)
            folder_path = os.path.join(base_download_folder, folder_name)
            os.makedirs(folder_path, exist_ok=True)

            save_email(msg, folder_path)

            if msg.is_multipart():
                for part in msg.walk():
                    content_disposition = part.get("Content-Disposition", None)
                    if content_disposition:
                        if any(dispo in content_disposition for dispo in ['attachment', 'inline']) or part.get_content_maintype() == 'image':
                            filename = part.get_filename()
                            
                            if filename:
                                filepath = os.path.join(folder_path, sanitize_filename(filename))
                                with open(filepath, 'wb') as f:
                                    f.write(part.get_payload(decode=True))
                                print(f"Đã tải về file đính kèm: {filename}")

            processed_emails.add(email_id)
            print(f"Đã lưu email: {folder_path}")

    mail.quit()

    return processed_emails

# Thực hiện chạy thử hàm pop_mail với các tham số cần thiết
if __name__ == "__main__":
    pop_server = "union-plate.cybermail.jp"    # POPサーバのアドレスを設定
    email_user = "r-tong@union-plate.co.jp"       # メールのユーザー名を設定
    email_password = "q9EH2j4t"     # メールのパスワードを設定
    download_folder = r"C:\Users\DSP189\Desktop\test"  # ダウンロードフォルダのパスを設定
    sender_email = "r-tong@union-plate.co.jp"
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Lấy danh sách các email đã được xử lý trước đó
    processed_emails_file = os.path.join(download_folder, "processed_emails.txt")
    if os.path.exists(processed_emails_file):
        with open(processed_emails_file, "r") as f:
            processed_emails = set(f.read().splitlines())
    else:
        processed_emails = set()

    # Thực hiện tải xuống và xử lý email
    processed_emails = pop_mail(pop_server, email_user, email_password, download_folder, processed_emails)

    # Lưu danh sách các email đã được xử lý
    with open(processed_emails_file, "w") as f:
        f.write("\n".join(processed_emails))
