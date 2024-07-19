from datetime import datetime

target_date = datetime.now()
target_day ="_" + target_date.strftime("%Y%m%d%H%M%S")
print(target_day)