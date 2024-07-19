import datetime


# Lấy thời gian hiện tại
thoi_gian_hien_tai = datetime.datetime.now()

# Lấy giờ, phút và giây
gio = thoi_gian_hien_tai.hour
phut = thoi_gian_hien_tai.minute
giay = thoi_gian_hien_tai.second

# In ra giờ, phút và giây
print("Bây giờ là {}:{}:{}".format(gio, phut, giay))


dt1 = datetime.date(2023, 11, 13).strftime("%Y/%m/%d")
#print(dt1)
print(dt1)
print(type(dt1))