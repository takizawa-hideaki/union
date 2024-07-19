# Tạo từ điển ánh xạ giữa host và tên đại diện
host_mapping = {
    '192.168.162.51': '本社工場',
    # Thêm các ánh xạ khác nếu cần thiết
}

# Giá trị host cần chuyển đổi
host = '192.168.162.51'

# Sử dụng từ điển để lấy tên đại diện
ten_dai_dien = host_mapping.get(host, host)

# In kết quả
print(ten_dai_dien)
