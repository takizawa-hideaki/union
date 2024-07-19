from openpyxl import Workbook





excel_path = r"C:\Users\DSP189\Desktop\test\example.xlsx"
 # Tạo một đối tượng Workbook mới
wb = Workbook()
# Chọn sheet đầu tiên (active)
ws = wb.active

# Ghi dữ liệu vào ô A2
ws['A2'] = 'juuchu'
ws.title = "name1"
    # Lưu file Excel vào đường dẫn được chỉ định
wb.save(excel_path)


print(f"Đã tạo file Excel mới thành công tại '{excel_path}'.")