import poplib
from datetime import datetime, timedelta
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
email_count, _ = mail_server.stat()
print("Tổng số email trong hộp thư đến:", email_count)

# Lấy thời gian hiện tại và thời gian cần kiểm tra (2 ngày trước)
current_time = datetime.now()
check_time = current_time - timedelta(days=2)

# Danh sách ID của các email đã tải xuống trong khoảng thời gian gần đây
downloaded_email_ids = []

# Duyệt qua từng email trong hộp thư đến
for i in range(email_count):
    response, message_lines, _ = mail_server.top(i + 1, 0)  # Thêm một biến _ cho dòng này để bỏ qua giá trị không cần thiết
    if response.startswith(b'+OK'):
        message_lines = [line.decode('utf-8', 'ignore') for line in message_lines]
        # Lấy thời gian gửi của email từ header
        for line in message_lines:
            if line.startswith('Date:'):
                email_time_str = line.split(': ', 1)[1].strip()
                email_time_str = clean_date_string(email_time_str)  # Loại bỏ phần không cần thiết
                email_time = datetime.strptime(email_time_str, "%a, %d %b %Y %H:%M:%S %z")
                email_time = email_time.replace(tzinfo=None)
                # Kiểm tra nếu email được gửi trong khoảng thời gian gần đây
                if email_time > check_time:
                    downloaded_email_ids.append(i + 1)  # Thêm ID email vào danh sách

# In ra danh sách ID email đã tải xuống trong khoảng thời gian gần đây
print("ID của các email đã tải xuống trong khoảng thời gian gần đây:", downloaded_email_ids)

# Đóng kết nối với server POP3
mail_server.quit()
