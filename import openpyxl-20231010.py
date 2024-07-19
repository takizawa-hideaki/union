import openpyxl

# Tạo một tệp Excel mới
wb = openpyxl.Workbook()
# Chọn một trang tính (sheet) mặc định
sheet = wb.active

# Ghi dữ liệu vào các ô
sheet["A1"] = "Hello"
sheet["B1"] = "World"

# Lưu tệp Excel
wb.save("example.xlsx")     