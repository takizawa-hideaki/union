from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time 

file_path = r"C:\Users\DSP189\Desktop\python\user5.json"
with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)
email = data["username"]
password = data["password"]
file_path1 = r"C:\Users\DSP189\Desktop\hoa_sen.txt"
with open(file_path1, "r",encoding="utf-8") as file:
    post_content = file.read()
file_path1 = "list_of_urls - コピー.json"
with open(file_path1, "r", encoding="utf-8") as file:
    data = json.load(file)
urls = data["urls"]


image_paths = [
    "C:\\Users\\DSP189\\Downloads\\cuc1.jpg",
    "C:\\Users\\DSP189\\Downloads\\cuc2.jpg",
    "C:\\Users\\DSP189\\Downloads\\cuc3.jpg",
    "C:\\Users\\DSP189\\Downloads\\sen3.jpg",
    "C:\\Users\\DSP189\\Downloads\\sen5.jpg",
    "C:\\Users\\DSP189\\Downloads\\sen6.jpg"
]

# Cấu hình Edge để cho phép nhận thông báo
edge_options = webdriver.EdgeOptions()
prefs = {
    "profile.default_content_setting_values.notifications": 1  # 1: Allow, 2: Block
}
edge_options.add_experimental_option("prefs", prefs)

# Khởi tạo trình duyệt với cấu hình
driver = webdriver.Edge(options=edge_options) # Cần phải có Chrome WebDriver

# Mở trang đăng nhập Facebook
driver.get("https://www.facebook.com")

# Điền thông tin đăng nhập
email_elem = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "email"))
)
email_elem.send_keys(email)

password_elem = driver.find_element(By.NAME, "pass")
password_elem.send_keys(password)

# Submit form
password_elem.send_keys(Keys.RETURN)
time.sleep(3)
for url in urls:
    driver.get(url)

    time.sleep(3)
    # Tìm và nhấp vào phần tử tạo bài viết mới
    composer_span = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Bạn viết gì đi...')]"))
    )
    composer_span.click()

    # Tìm phần tử contenteditable và nhập nội dung bài viết
# Tìm phần tử <span> có data-offset-key="da5l-0-0"
    post_div = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true'][aria-label='Tạo bài viết công khai...']"))
    )
    post_div.click()
# Sử dụng JavaScript để nhập nội dung chứa ký tự ngoài BMP
    post_div.send_keys(post_content)


    # Chờ một lát để đảm bảo nội dung được nhập
    driver.implicitly_wait(2)
    photo_video_button = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Ảnh/video']"))
    )
    photo_video_button.click()

    # Tải lên ảnh từ máy tính
    upload_input = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, "//input[@accept='image/*,image/heif,image/heic,video/*,video/mp4,video/x-m4v,video/x-matroska,.mkv']"))
    )
    upload_input.send_keys('\n'.join(image_paths))

    time.sleep(3)
 # Đăng bài
    post_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Đăng' and @role='button']"))
    )
    post_button.click()
    time.sleep(10)
# driver.get("https://www.facebook.com/groups/142910156194812/my_removed_content")
# edit_post_button = WebDriverWait(driver, 20).until(
#         EC.element_to_be_clickable((By.XPATH, "//span[text()='Chỉnh sửa bài viết']"))
#     )
# edit_post_button.click()
# #  # Tìm phần tử contenteditable
# # span_element = WebDriverWait(driver, 20).until(
# #         EC.presence_of_element_located((By.CSS_SELECTOR, "span[data-offset-key]"))
# #     )
    
# #     # Nhập nội dung mới
# # with open(file_path1, "r",encoding="utf-8") as file:
# #     new_content = file.read()
# # driver.execute_script("arguments[0].innerHTML = arguments[1];", span_element, new_content)


# # # Nhấn nút "Lưu"
# # save_button = WebDriverWait(driver, 20).until(
# #         EC.element_to_be_clickable((By.XPATH, "//span[text()='Lưu']"))
# #     )
# # save_button.click()
# input("j:")


