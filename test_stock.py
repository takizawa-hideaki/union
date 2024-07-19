import requests

def get_btc_price():
    # Đường dẫn API của CoinGecko
    api_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    
    # Gửi yêu cầu GET đến API của CoinGecko
    response = requests.get(api_url)
    
    # Kiểm tra xem yêu cầu có thành công không
    if response.status_code == 200:
        # Chuyển đổi dữ liệu JSON nhận được thành một đối tượng Python
        data = response.json()
        
        # Lấy giá hiện tại của BTC từ dữ liệu JSON
        current_price = data['bitcoin']['usd']
        
        return current_price
    else:
        print("Failed to fetch BTC price.")
        return None

# Lấy giá hiện tại của Bitcoin
current_price = get_btc_price()

if current_price is not None:
    print("Giá hiện tại của Bitcoin (BTC):", current_price)
