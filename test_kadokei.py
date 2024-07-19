
from selenium.webdriver import Edge
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
from bs4 import BeautifulSoup
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


logging.basicConfig(filename=r'C:\Users\DSP189\Desktop\新しいフォルダー (9)\log_file.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
driver =Edge()
current_time = datetime.now()
driver.maximize_window()
if current_time.hour < 18:
    driver.get(r"https://union-plate.cybozu.com/k/1069/#page=0")
else:
    driver.get(r"https://union-plate.cybozu.com/k/1069/#page=1")
file_path = r"C:\Users\DSP189\Desktop\user1.txt"
try: 
    with open(file_path, "r") as file:
        lines = file.readlines()
        username = lines[0].strip()  # Line1: username
        password = lines[1].strip() # Line2: password
# ID入力フィールドを見つけて値を入力します。
    username_field = driver.find_element(By.NAME, "username")
    username_field.send_keys(username)

# パスワード入力フィールドを見つけて値を入力します。
    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys(password)

    submit_button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='ログイン']")
    submit_button.click()

    time.sleep(10)
    html = driver.page_source

# Tạo đối tượng BeautifulSoup từ mã HTML
    soup = BeautifulSoup(html, "html.parser")

# Tìm tất cả các phần tử div có class là "select-cell" trong class "select-table"
    cells = soup.select(".select-table .select-cell")

# Đếm số lượng cell
    num_cells = len(cells)
    print("Số lượng cell trong class select-table là:", num_cells)

# Vòng lặp từ cell 0 đến cell 10 và sau đó quay lại cell 0
    while True:
        for i in range(num_cells):
        # Tạo ID của cell dựa trên index i
            cell_id = f"cell{i}"
        
        # Chờ cho cell xuất hiện trước khi thực hiện click
            cell = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, cell_id)))
        
        # Thực hiện click
            cell.click()
        
        # Chờ 1 giây trước khi tiếp tục vòng lặp
            time.sleep(5)
    
    # Nhấn vào nút "refresh"
        refresh_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[actions="refresh"]')))
        refresh_button.click()
        
    
    # Chờ cho cell 0 xuất hiện trước khi tiếp tục vòng lặp
        cell_0 = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, f"cell{num_cells-1}")))
        cell_0.click()
        # So sánh thời gian hiện tại với 18:00:00
        if current_time.hour >= 18:
        # Nếu thời gian hiện tại sau hoặc bằng 18:00:00, thực hiện truy cập vào example2.com
            driver.get(r"https://union-plate.cybozu.com/k/1069/#page=1")
        else:
        # Nếu thời gian hiện tại trước 18:00:00, tiếp tục vòng lặp
            continue
except Exception as e:
    # Nếu có lỗi, ghi log lỗi và in ra thông báo lỗi
    logging.error(f'Error: {str(e)}')
    try:
    # Gửi email cảnh báo
        sender_email = "r-tong@union-plate.co.jp"
        receiver_email = "r-tong@union-plate.co.jp"
        password = "q9EH2j4t"

        subject = f"Chương trình gặp lỗi!{datetime.now()}"
        body = f"Chương trình của bạn gặp lỗi. Chi tiết: {str(e)}"

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL("union-plate.cybermail.jp", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
    except Exception as email_error:
            # Ghi log lỗi khi gửi email
            logging.error(f'Error when sending email: {str(email_error)}')
        # In ra thông báo lỗi
            print(f'Error when sending email: {str(email_error)}')
input("j:")