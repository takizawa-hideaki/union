import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Thông tin tài khoản email của bạn
sender_email = "r-tong@union-plate.co.jp"
password = "q9EH2j4t"

# Tạo một đối tượng MIMEMultipart để tạo email
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = sender_email  # Gửi cho chính bạn
message["Subject"] = "Subject of the email"

# Thêm nội dung của email
body = "Content of the email"
message.attach(MIMEText(body, "plain"))

# Kết nối đến máy chủ SMTP của nhà cung cấp email của bạn
server = smtplib.SMTP_SSL("union-plate.cybermail.jp", 465)

# Đăng nhập vào tài khoản email của bạn
server.login(sender_email, password)

# Gửi email
server.sendmail(sender_email, sender_email, message.as_string())

# Đóng kết nối
server.quit()
