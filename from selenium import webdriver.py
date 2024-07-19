from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# Khởi tạo trình duyệt Edge WebDriver
driver = webdriver.Edge(EdgeChromiumDriverManager().install())

# URL của trang web bạn muốn đăng nhập
login_url = 'https://example.com/login'

# Tải trang web
driver.get(login_url)

# Tìm và điền thông tin đăng nhập
username_field = driver.find_element_by_id('username')  # Thay id bằng id thực tế của trường nhập tên người dùng
password_field = driver.find_element_by_id('password')  # Thay id bằng id thực tế của trường nhập mật khẩu

# Điền thông tin đăng nhập
username_field.send_keys('your_username')
password_field.send_keys('your_password')

# Gửi biểu mẫu đăng nhập
password_field.send_keys(Keys.RETURN)

# Chờ cho trang web xử lý đăng nhập (có thể cần thêm thời gian tùy thuộc vào trang web)
driver.implicitly_wait(10)

# Kiểm tra xem đăng nhập có thành công không bằng cách kiểm tra URL hoặc nội dung trang web
if 'successful_page' in driver.current_url:  # Thay successful_page bằng URL của trang web sau khi đăng nhập thành công
    print("Đăng nhập thành công!")
else:
    print("Đăng nhập không thành công.")

# Đóng trình duyệt sau khi hoàn thành
driver.quit()
