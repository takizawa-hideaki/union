import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(subject, message):
    # Thông tin email của bạn
    email_address = "your_email@gmail.com"
    email_password = "your_password"

    # Địa chỉ email mà Google Form sẽ gửi dữ liệu đến
    google_form_email = "your_google_form_email@googlegroups.com"

    # Tạo một email mới
    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = google_form_email
    msg['Subject'] = subject

    # Thêm nội dung email
    msg.attach(MIMEText(message, 'plain'))

    # Kết nối tới máy chủ SMTP của Google
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(email_address, email_password)

    # Gửi email
    server.send_message(msg)

    # Đóng kết nối
    server.quit()

# Sử dụng hàm send_email để gửi dữ liệu vào Google Sheets
def add_to_google_sheet(noidung, giatri, ngay):
    subject = "New Entry"
    message = f"Nội dung Khoản thu: {noidung}\nGiá trị: {giatri}\nNgày phát sinh: {ngay}"
    send_email(subject, message)

# Sử dụng hàm add_to_google_sheet để thêm dữ liệu vào Google Sheets
add_to_google_sheet("Thuê nhà", "5000000", "2024-05-15")
