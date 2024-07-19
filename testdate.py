from datetime import datetime

# Lấy ngày tháng hiện tại
current_date = datetime.now()

# Định dạng ngày tháng thành chuỗi "YYYY.M.D" nếu tháng < 10
formatted_date = current_date.strftime("%Y.%m")

print(formatted_date)
