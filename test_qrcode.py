import qrcode
from datetime import datetime
def generate_qr_code(link, output_file):
    # Tạo đối tượng QRCode
    qr = qrcode.QRCode(
        version=1,  # Kích thước của mã QR, 1 là nhỏ nhất, tăng dần kích thước
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Mức độ sửa lỗi
        box_size=10,  # Kích thước của mỗi ô trong mã QR
        border=4,  # Độ rộng của viền
    )
    
    # Thêm dữ liệu vào mã QR
    qr.add_data(link)
    qr.make(fit=True)
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    # Tạo hình ảnh của mã QR
    img = qr.make_image(fill='black', back_color='white')
    
# Tạo tên tệp hình ảnh với ngày giờ tạo
    output_file = f"qrcode_{timestamp}.png"
    
    # Lưu hình ảnh vào tệp
    img.save(output_file)
    print(f"Mã QR đã được lưu vào {output_file}")
# Đường link cần tạo mã QR
link = "https://forms.gle/xskHyaJ6BUb4xcEF8"
# Tên tệp hình ảnh đầu ra
output_file = "qrcode.png"

# Gọi hàm để tạo mã QR
generate_qr_code(link, output_file)
