
from selenium.webdriver import Edge
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import string
driver = Edge()
# Hàm để thêm một ký tự ngẫu nhiên vào chuỗi
def add_char_and_digit(s):
    # Chuyển chuỗi thành danh sách các ký tự
    s_list = list(s)
    # Xáo trộn danh sách các ký tự
    random.shuffle(s_list)
    # Chuyển danh sách đã xáo trộn thành chuỗi
    shuffled_s = ''.join(s_list)
    # Chọn một vị trí ngẫu nhiên trong chuỗi
    random_index = random.randint(0, len(shuffled_s))
    # Lấy một ký tự ngẫu nhiên từ chuỗi ascii_lowercase (a-z)
    random_char = random.choice(string.ascii_lowercase)
    digit = random.choice(string.digits)
    # Thêm ký tự ngẫu nhiên vào chuỗi tại vị trí ngẫu nhiên và trả về
    return shuffled_s[:random_index] + random_char + digit + shuffled_s[random_index:]
# Mở trang đăng nhập Microsoft
driver.get("https://login.live.com/")
time.sleep(5)
# Google検索のURLを開きます
for _ in range(45):
    driver.get("https://www.bing.com/")
    s = "あｂｊだ"
    search_text = add_char_and_digit(s) + " とは"
# Googleの検索バーを取得
    search_box = driver.find_element(By.NAME, "q")
# Googleの検索バーへ文字を入力
    search_box.clear()
    search_box.send_keys(search_text)
# エンターキーを押すの同義
    search_box.submit()
    time.sleep(5)

