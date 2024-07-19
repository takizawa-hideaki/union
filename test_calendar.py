import datetime

def get_date_range(year, month):
    # Tính toán ngày bắt đầu (1st day of the month)
    start_date = datetime.date(year, month, 1)
    
    # Tính toán ngày kết thúc (last day of the month)
    next_month = start_date.replace(month=start_date.month+1, day=1)
    end_date = next_month - datetime.timedelta(days=1)
    
    return start_date, end_date

previous_month = datetime.date.today().month-5 
previous_year = datetime.date.today().year 
if previous_month <= 0: 
    previous_month +=12
    previous_year = previous_year - 1
print( previous_month,previous_year)
# Sử dụng hàm để lấy ngày bắt đầu và ngày kết thúc
start_date, end_date = get_date_range(previous_year, previous_month)
start_date = start_date.strftime("%Y/%m/%d")
end_date = end_date.strftime("%Y/%m/%d")

# In ra ngày bắt đầu và ngày kết thúc
print("Ngày bắt đầu:", start_date)
print("Ngày kết thúc:", end_date)
