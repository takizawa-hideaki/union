import json

# Tạo một dictionary chứa thông tin đăng nhập
login_info = {
    "username": "your_username",
    "password": "your_password"
}

# Đường dẫn tới file JSON mà bạn muốn tạo
json_file_path = "login_info.json"

# Ghi dictionary vào file JSON
with open(json_file_path, "w") as json_file:
    json.dump(login_info, json_file)

print("Đã tạo file JSON chứa thông tin đăng nhập.")
