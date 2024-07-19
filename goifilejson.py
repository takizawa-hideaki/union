import json

# Đọc từ file JSON
with open("tokuisakies.json", "r", encoding="utf-8") as json_file:
    data = json.load(json_file)

# In ra dữ liệu
for item in data:
    if "#tokuisaki_code" in item:  # Kiểm tra xem item có phải là comment không
        print("Comment:")
        print("{")
        for key, value in item.items():
            print(f"    {key}: {value}")
        print("}")
    else:
        print("Tokuisaki:")
        print("{")
        for key, value in item.items():
            print(f"    {key}: {value}")
        print("}")
