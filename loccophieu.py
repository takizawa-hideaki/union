import yfinance as yf
import pandas as pd
import time

# Bước 1: Đọc danh sách mã cổ phiếu từ file Excel
tickers_df = pd.read_excel(r'C:\Users\DSP189\Downloads\stock.xlsx')
tickers = tickers_df['Ticker'].tolist()

# Bước 2: Lấy dữ liệu cổ phiếu từ Yahoo Finance
def fetch_stock_data(tickers, max_retries=3, delay=2):
    stock_data = {}
    for ticker in tickers:
        attempts = 0
        while attempts < max_retries:
            try:
                stock = yf.Ticker(ticker)
                stock_info = stock.info
                
                # Kiểm tra nếu dữ liệu hợp lệ
                if 'marketCap' in stock_info and stock_info['marketCap'] is not None:
                    stock_data[ticker] = stock
                break
            except Exception as e:
                attempts += 1
                print(f"Error fetching data for {ticker}: {e}. Attempt {attempts} of {max_retries}.")
                time.sleep(delay)
    return stock_data

# Bước 3: Lọc dữ liệu theo các tiêu chí
def filter_stocks(stock_data):
    filtered_stocks = []
    
    for ticker, stock in stock_data.items():
        info = stock.info
        
        # Tiêu chí 1: Vốn hóa thị trường > 50 triệu USD
        if info.get("marketCap", 0) < 126e12:
            continue
        
        # Tiêu chí 2: Lợi nhuận từ hoạt động kinh doanh dương trong 5 năm liên tiếp
        financials = stock.financials
        if financials.empty or (financials.loc['Operating Income'] <= 0).sum() > 0:
            continue
        
        # Tiêu chí 3: ROE lớn hơn 15% trong 2 năm gần nhất và lũy kế 12 tháng
        roe = info.get("Return on Equity", 0)
        if roe is None or roe < 0.15:
            continue
        
        # Tiêu chí 4: Tỷ lệ P/FCF trong top 30% thấp nhất toàn thị trường
        cash_flow = stock.cashflow
        free_cash_flow = cash_flow.loc['Free Cash Flow'].iloc[0] if not cash_flow.empty else 0
        if free_cash_flow <= 0:
            continue
        p_fcf = info["marketCap"] / free_cash_flow
        
        # Tiêu chí 5: Operating income margin > Operating income margin Median
        revenue = financials.loc['Total Revenue'].iloc[0] if not financials.empty else 0
        operating_income_margin = financials.loc['Operating Income'].iloc[0] / revenue if revenue > 0 else 0
        
        # Tiêu chí 6: Net income margin > Net income margin Median
        net_income = financials.loc['Net Income'].iloc[0] if not financials.empty else 0
        net_income_margin = net_income / revenue if revenue > 0 else 0
        
        # Thêm vào danh sách lọc nếu tất cả các tiêu chí đều đạt
        filtered_stocks.append({
            'Ticker': ticker,
            'Market Cap': info['marketCap'],
            'Operating Income Margin': operating_income_margin,
            'Net Income Margin': net_income_margin,
            'P/FCF': p_fcf,
            'ROE': roe
        })
    
    return filtered_stocks

# Bước 4: Chạy các bước lọc
stock_data = fetch_stock_data(tickers)
filtered_stocks = filter_stocks(stock_data)

# Chuyển đổi kết quả sang DataFrame để dễ dàng thao tác và hiển thị
filtered_stocks_df = pd.DataFrame(filtered_stocks)
print(filtered_stocks_df)
