import pyautogui

try:
    while True:
        # Lấy vị trí hiện tại của con trỏ chuột
        current_mouse_position = pyautogui.position()

        # Hiển thị hộp thoại thông báo ở vị trí của con trỏ chuột
        pyautogui.alert(f"Tọa độ hiện tại của con trỏ chuột: {current_mouse_position}")

        # Đợi một khoảng thời gian ngắn trước khi cập nhật lại vị trí con trỏ chuột
        pyautogui.sleep(0.5)

except KeyboardInterrupt:
    # Khi nhấn Ctrl+C, thoát khỏi vòng lặp
    pass
