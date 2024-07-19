import datetime

def chao_hoi():
    # Lấy ngày tháng năm hiện tại
    ngay_hien_tai = datetime.datetime.now()
    ngay = ngay_hien_tai.strftime("%d")
    thang = ngay_hien_tai.strftime("%m")
    nam = ngay_hien_tai.strftime("%Y")
    # Chào hỏi với ngày tháng năm hiện tại
    return f"Chào bạn! Hôm nay là ngày {ngay} tháng {thang} năm {nam}."

print(chao_hoi())
