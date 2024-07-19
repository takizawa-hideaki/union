from selenium.webdriver import Edge, EdgeOptions
import requests

# URL để truy cập vào DevTools Protocol
devtools_url = "http://localhost:9222/json"

# Lấy danh sách các tab đang mở
response = requests.get(devtools_url)
tabs = response.json()

# In ra danh sách các tab và PID
for tab in tabs:
    print(f"Tab: {tab['title']}, URL: {tab['url']}, PID: {tab['pid']}")

# Chọn PID của tab cần điều khiển
desired_pid = 3248  # Thay PID tương ứng của tab bạn muốn điều khiển

# Tạo EdgeOptions và chỉ định port và PID
edge_options = EdgeOptions()
edge_options.use_chromium = True
edge_options.debugger_address = f"localhost:{desired_pid}"

# Khởi tạo trình duyệt Edge với EdgeOptions
driver = Edge(options=edge_options)

# Bây giờ bạn có thể sử dụng driver để điều khiển tab đã chọn
# Ví dụ:
driver.get("https://www.google.com/")
