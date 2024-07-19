
from selenium.webdriver import Edge
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
 
# 利用するブラウザー
driver = Edge()
driver.get(r"http://192.168.231.167/unionPlateMulti/login.do")
file_path = r"C:\Users\DSP189\Desktop\user.txt"
driver.maximize_window()

with open(file_path, "r") as file:
    lines = file.readlines()
    username = lines[0].strip()  # Line1: username
    password = lines[1].strip() # Line2: password
# ID入力フィールドを見つけて値を入力します。
username_field = driver.find_element(By.NAME, "loginId")
username_field.send_keys(username)

# パスワード入力フィールドを見つけて値を入力します。
password_field = driver.find_element(By.NAME, "password")
password_field.send_keys(password)

 
# ログイン
submit_button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='ログイン']")
submit_button.click()
# JavaScriptを使用して「switchSubMenu('2')」（受注業務）ボタンをクリックします。
switch_submenu_button1 = driver.find_element(By.XPATH, "//a[@onclick=\"switchSubMenu('2')\"]")
driver.execute_script("arguments[0].click();", switch_submenu_button1)
#ＣＳＶ取込受注ボタンをクリックします。
switch_submenu_button2 = driver.find_element(By.XPATH, "//a[@onclick=\"selectMenuItem('JUCHU1001','ＣＳＶ取込受注','/inputCsvloadFile/inputCsvloadFile',false)\"]")
driver.execute_script("arguments[0].click();", switch_submenu_button2)
#ドロップダウン（得意先）で選ぶ
select_element = driver.find_element(By.ID, "tokuisakiCode")
dropdown = Select(select_element)
dropdown.select_by_value("24009")  # 値は： "29453：大同ＤＭソリューション㈱ 生産本部　生産管理室（奈良）"
# CSVフィルアップロード
file_input = driver.find_element(By.ID, "orderFile")
file_input.send_keys(r"C:\Users\DSP189\Downloads\ユニオンプレート向け注文書_24009_20240509.csv")  # Nhập đường dẫn tệp vào trường nhập

# 取り込みボタンをクリック、WebDriverWait と Expected_conditions を使用してこの操作を実行する前に、ページ上の要素が完全に読み込まれていることを確認
import_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "headButtonImport")))
import_button.click()
#ログアウト
# logout_button = driver.find_element(By.ID, "subMenu_LOGOUT")
# logout_button.click()

input("j:")