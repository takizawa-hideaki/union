import msvcrt
import time 

print("Nhập gì đó:")
start_time = time.time() # Thời điểm bắt đầu chờ

# Lặp cho đến khi người dùng nhập hoặc hết thời gian
while True:
    if time.time() - start_time >= 5: # Nếu đã hết 5 giây
        print("\nHết thời gian. Tự động kết thúc chương trình.")
        exit()
    if msvcrt.kbhit():  # Kiểm tra nếu có ký tự được nhấn từ bàn phím
        a = input()
        break # Thoát khỏi vòng lặp nếu có dữ liệu nhập từ bàn phím

# Xử lý dữ liệu đã nhập
print("Bạn đã nhập:", a)

