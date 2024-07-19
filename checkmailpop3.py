import poplib
from datetime import datetime, timedelta
import email
from email.parser import Parser
import re

# Hàm loại bỏ phần không cần thiết trong chuỗi thời gian
def clean_date_string(date_str):
    # Loại bỏ các chuỗi trong dấu ngoặc đơn ()
    date_str = re.sub(r'\([^)]*\)', '', date_str)
    return date_str.strip()
# Thay đổi thông tin tài khoản email của bạn
pop3_server = "union-plate.cybermail.jp"
username = "r-tong@union-plate.co.jp"
password = "q9EH2j4t"

# Kết nối tới server POP3
mail_server = poplib.POP3_SSL(pop3_server)
mail_server.user(username)
mail_server.pass_(password)

# Lấy danh sách các email trong hộp thư đến
email_count, email_size = mail_server.stat()
print("Tổng số email trong hộp thư đến:", email_count)

# Lấy thời gian hiện tại
current_time = datetime.now()

# Thời gian cần kiểm tra (2 ngày trước)
check_time = current_time - timedelta(days=2)

# Duyệt qua từng email trong hộp thư đến
for i in range(email_count):
    response, message_lines, bytes_lines = mail_server.retr(i+1)
    # Chuyển đổi từ bytes thành văn bản
    message_content = b'\n'.join(message_lines).decode('utf-8')
# Parse email
    msg = email.message_from_string(message_content)
    email_time_str = clean_date_string(msg["Date"])
    email_time = datetime.strptime(email_time_str, "%a, %d %b %Y %H:%M:%S %z") 
    email_time = email_time.replace(tzinfo=None)  
    # Kiểm tra nếu email được gửi trong vòng 2 ngày gần đây
    if email_time > check_time:
        print("Email từ:", msg["From"])
        print("Chủ đề:", msg["Subject"])
        print("Thời gian gửi:", msg["Date"])
        print("-" * 50)

# Đóng kết nối với server POP3
mail_server.quit()
