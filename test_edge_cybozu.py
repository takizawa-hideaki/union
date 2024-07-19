
from selenium.webdriver import Edge
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
from selenium import webdriver


current_date = datetime.datetime.today() 
delta_date = current_date.strftime("%Y.%#m.%d")

# 利用するブラウザー
driver =Edge()
driver.get(r"https://union-plate.cybozu.com/login")
file_path = r"C:\Users\DSP189\Desktop\user1.txt"

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

 
# ログイン
submit_button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='ログイン']")
submit_button.click()
button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.service-slash[href="/o/"]'))
    )
 
   # Nhấn vào nút
button.click()
link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, f'a.event[href*="ag.cgi?page=ScheduleView&UID=942&GID=&Date=da.{delta_date}&BDate=da.{delta_date}"][title*="備忘:仕入品ミルシート添付kintone登録"]'))
    )

    # Nhấn vào link
link.click()
txt_path = f"\\\\192.168.160.6\\usbdisk3\\システム運用\\■新システム\\kintone 関連\\ミルシート業務\\取込CSV\\log\\2024_04\\240411.txt"
with open(txt_path, "r") as file:
        comment_data = file.read()
comment = driver.find_element(By.ID,"dz_NewComment")
comment.send_keys(comment_data)
file_input = driver.find_element(By.CSS_SELECTOR, 'input[type="file"][id*="filese"][name="files[]"][size="0"][multiple]')

file_input.send_keys(r"\\192.168.160.6\usbdisk3\システム運用\■新システム\kintone 関連\ミルシート業務\取込CSV\2024_04\240411.csv")
#send = WebDriverWait(driver, 10).until(
        #EC.element_to_be_clickable((By.CSS_SELECTOR, 'input#followAddButton.vr_hotButton[type="submit"][name="Submit"][value="書き込む"]'))
    #)
 
   # Nhấn vào nút
#send.click()
input("j:")
