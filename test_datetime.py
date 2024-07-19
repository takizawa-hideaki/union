import psutil
import os

# Lấy danh sách các quy trình đang chạy
for proc in psutil.process_iter(['pid', 'name']):
    if 'cmd.exe' in proc.info['name']:
        # Tắt quy trình
        os.system(f"taskkill /PID {proc.info['pid']} /F")
