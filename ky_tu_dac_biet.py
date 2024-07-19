import unicodedata
def convert_to_unicode(text):
    # Hàm chuyển đổi ký tự đặc biệt thành Unicode
    result = []
    for char in text:
        if ord(char) > 127 or unicodedata.category(char)[0] == 'M':  # Kiểm tra xem ký tự có thuộc về bảng mã ASCII không
            result.append(f"\\u{ord(char):04x}")  # Chuyển đổi sang dạng Unicode
        else:
            result.append(char)
    return ''.join(result)

# Chuỗi đầu vào chứa các ký tự đặc biệt
input_text = "Chào bạn 👋, hôm nay là thứ 4!"

# Chuyển đổi thành chuỗi Unicode
unicode_text = convert_to_unicode(input_text)

print("Chuỗi đầu vào:", input_text)
print("Chuỗi Unicode:", unicode_text)
