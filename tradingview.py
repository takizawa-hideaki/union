import yfinance as yf
import pandas as pd

def check_stock_price(symbol, threshold):
    # Lấy dữ liệu giá cổ phiếu từ Yahoo Finance
    stock_data = yf.download(symbol, start="2024-04-01", end="2024-04-15")

    # Lấy giá đóng cửa cuối cùng
    last_close_price = stock_data['Close'].iloc[-1]
    brent = yf.Ticker("BZ=F")
    print(f"Giá hiện tại của brent là {brent}")
    # Kiểm tra nếu giá vượt qua ngưỡng
    if last_close_price > threshold:
        print(f"Cảnh báo: Giá cổ phiếu {symbol} đã vượt qua ngưỡng {threshold}.")

# Ticker của cổ phiếu và ngưỡng cảnh báo
brent_crude = "BZ=F"  # Ví dụ: Apple
alert_threshold = 50   # Giả sử ngưỡng cảnh báo là $150

# Kiểm tra giá cổ phiếu và thông báo cảnh báo nếu cần
check_stock_price(brent_crude, alert_threshold)

