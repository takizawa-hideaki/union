
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
driver.get(r"https://rewards.bing.com/?ref=pinML2BFG&OCID=PINREW")
current_tab = driver.current_window_handle
# Chờ đến khi phần tử xuất hiện trong DOM
element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "mee-rewards-daily-set-item-content[item='$ctrl.dailySets[0][0]']"))
    )
element.click()

# Click vào phần tử
element.click()

driver.switch_to.window(current_tab)
element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "mee-rewards-daily-set-item-content[item='$ctrl.dailySets[0][1]']"))
    )
element.click()

# Click vào phần tử
element.click()

driver.switch_to.window(current_tab)
element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "mee-rewards-daily-set-item-content[item='$ctrl.dailySets[0][2]']"))
    )
element.click()

# Click vào phần tử
element.click()

driver.switch_to.window(current_tab)

