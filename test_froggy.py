
from selenium.webdriver import Edge
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains


current_date = datetime.datetime.today() 
delta_date = current_date.strftime("%Y.%#m.%d")

# 利用するブラウザー
driver =Edge()
driver.get(r"https://froggy.smbcnikko.co.jp/")
file_path = r"C:\Users\DSP189\Desktop\user3.txt"

login_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'l-header__btn--login')))

# Thực hiện click vào nút
login_button.click()

with open(file_path, "r") as file:
    lines = file.readlines()
    username = lines[0].strip()  # Line1: username
    password = lines[1].strip() # Line2: password
# ID入力フィールドを見つけて値を入力します。
input_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "js-first-focus")))

# Điền thông tin vào trường input
input_field.send_keys(username)

# パスワード入力フィールドを見つけて値を入力します。
password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "login-form-password")))

# Điền thông tin vào trường password
password_field.send_keys(password)

 
# ログイン
# Chờ cho nút login xuất hiện
login_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input.btn--primary.btn--large.form__submit[value="ログインする"]')))

# Click vào nút login
login_button.click()
# Tìm tất cả các phần tử có class là "articleSlim articleCardSlim"
element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'a.articleSlim.articleCardSlim'))
)

# Click vào phần tử đầu tiên nếu có
element.click()
# Sử dụng JavaScript để cuộn trang web xuống cuối

input("j:")
