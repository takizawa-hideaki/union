from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
import json
#end_time = datetime.now().replace(hour=18, minute=43, second=0, microsecond=0)

file_path1 = "list_of_urls.json"
with open(file_path1, "r", encoding="utf-8") as file:
    data = json.load(file)
urls = data["urls"]
time_sleep_path = "time_sleep.json"
with open(time_sleep_path, "r", encoding="utf-8") as file:
    data = json.load(file)
time_sleep = data["time_sleep"]

# Khởi tạo trình duyệt
driver = webdriver.Chrome()  # hoặc Firefox(), Edge(), ...
driver.get("https://teachme.jp/87402/manuals/28240029")


# Kiểm tra nếu trang yêu cầu đăng nhập bằng cách kiểm tra phần tử input
try:
    email_or_name_field = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='email-or-name']")))
        # Nếu thấy phần tử đăng nhập, đăng nhập với thông tin từ file
    file_path = "user.json"
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    username = data["username"]
    password = data["password"]
    email_or_name_field.send_keys(username)
    password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
    password_field.send_keys(password)
    time.sleep(2)
    login_button = driver.find_element(By.CSS_SELECTOR, "button[data-tmb-analysis-value='0']")
    login_button.click()
    
except:
        # Nếu không thấy phần tử đăng nhập, tiếp tục với các URL trong danh sách
    pass
driver.maximize_window()
time.sleep(5)
# Chờ cho phần tử body trở thành click được (đã tải hoàn tất)
body_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.TAG_NAME, "body")))

# Gửi phím F11 để ẩn thanh công cụ của trình duyệt

while True :  #datetime.now() < end_time:
    for url in urls:    
    # Mở trang TeachMe.biz
        driver.get(url)
        driver.implicitly_wait(2)
    

# Đăng nhập vào tài khoản của bạn

        slide_show_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='スライドショー']")))
        slide_show_button.click()
        time.sleep(1)
# Click vào vị trí bất kỳ trên trang
# Chuyển sang tab mới
        current_tab = driver.current_window_handle
        time.sleep(2)

# Đóng tab cũ
        driver.switch_to.window(current_tab)
        driver.close()

# Chuyển lại tab mới
        new_tab = [tab for tab in driver.window_handles if tab != current_tab][0]
        driver.switch_to.window(new_tab)
# Bắt đầu điều khiển slide show
        action_chains = ActionChains(driver)
        while True:
# Sử dụng ActionChains để nhấn phím mũi tên sang phải
            slides = driver.find_elements(By.XPATH, "//div[contains(@class, 'slide-show')]//div[contains(@class, 'step-slide-show') and contains(@class, 'parallel')]")

# Lặp qua danh sách các slide
            for slide in slides:
    # Kiểm tra xem slide hiện tại có video không
                video_present = False
                try:
                    video = driver.find_element(By.TAG_NAME, "video")
                    video_present = True
                except:
                    pass
    
    # Nếu slide có video, cho video phát hết
                if video_present:
                    video_duration = driver.execute_script("return arguments[0].duration", video)
                    driver.execute_script("arguments[0].play()", video)
                    time.sleep(video_duration)
    
                action_chains.send_keys(Keys.ARROW_RIGHT).perform()
                time.sleep(int(time_sleep))  # Đợi một chút giữa các slide
            if not slides:
                break
    
    
    
        
            


  
