import datetime
from openpyxl import Workbook
from openpyxl import load_workbook
import pandas as pd
from openpyxl.styles import Font
import openpyxl as xl
from selenium.webdriver import Edge
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
previous_day = datetime.date.today()-datetime.timedelta(days=1)
current_month = datetime.date.today().month
month = previous_day.month
day = previous_day.day


# #----------------------------------------------------------------
driver =Edge()
driver.get(r"https://union-plate.cybozu.com/o/ag.cgi?page=MyFolderMessageView&mDBID=7&mEID=112&mDID=17951&cp=ml&sp=&tp=")
file_path = r"C:\Users\DSP189\Desktop\user1.txt"
excel_path = r"\\192.168.160.6\usbdisk3\システム運用\■新システム\端材管理システム関連\工場別端材入出庫数_2024.xlsx"
excel_path_1 = r"\\192.168.160.6\usbdisk3\システム運用\■新システム\端材管理システム関連\工場別月末端材重量.xlsx"
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
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.commentAreaWrapper textarea.resizeTarget"))
    )
 
   # ボタンをクリックする
button.click()
if month < current_month:
    comment_data = f"""{month}月{day}日までの工場別端材入出庫数、工場別月末端材重量を添付します。
御確認宜しくお願い致します。"""
    try:
        comment = driver.find_element(By.ID,"Data-m112")
        comment.send_keys(comment_data) #コメントの所に書き込み
        file_input = driver.find_element(By.CSS_SELECTOR, 'input[type="file"][id*="filesm112_1"][name="files[]"][size="0"][multiple]')
        file_input.send_keys(excel_path)#CSVファイル添付する
        file_input = driver.find_element(By.CSS_SELECTOR, 'input[type="file"][id*="filesm112_1"][name="files[]"][size="0"][multiple]')
        file_input.send_keys(excel_path_1)#CSVファイル添付する
        # all_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@type="button" and @class="mentionAllMemberButton" and contains(text(), "@ 宛先全員を指定")]')))
        # all_button.click()#書き込みボタンをクリックする。
        submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//input[@class="vr_hotButton" and @type="submit" and @value="書き込む" and @name="Submit"]')))
        submit_button.click()#書き込みボタンをクリックする。
	
    except: 
	    input("コメントできませんでした。")
else:
    comment_data = f"""{month}月{day}日までの工場別端材入出庫数を添付します。
御確認宜しくお願い致します。"""
    try:
        comment = driver.find_element(By.ID,"Data-m112")
        comment.send_keys(comment_data) #コメントの所に書き込み
        file_input = driver.find_element(By.CSS_SELECTOR, 'input[type="file"][id*="filesm112_1"][name="files[]"][size="0"][multiple]')
        file_input.send_keys(excel_path)#CSVファイル添付する
        # all_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@type="button" and @class="mentionAllMemberButton" and contains(text(), "@ 宛先全員を指定")]')))
        # all_button.click()#書き込みボタンをクリックする。
        submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//input[@class="vr_hotButton" and @type="submit" and @value="書き込む" and @name="Submit"]')))
        submit_button.click()#書き込みボタンをクリックする。
	
    except: 
	    input("コメントできませんでした。")

