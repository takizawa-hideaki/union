
import csv

output_csv_file = r'C:\\Users\\DSP189\\Downloads\\union-plate.co.jp(2).csv'

input_csv_file = r'C:\\Users\\DSP189\\Downloads\\union-plate.co.jp.csv'

# Mở tệp CSV để đọc với mã hóa cp932
with open(input_csv_file, 'r', encoding='cp932') as csvfile:
    csv_reader = csv.reader(csvfile)

    # Xử lý từng hàng trong tệp CSV
    for row in csv_reader:
        print(row)

# Data to be written to the CSV file

# Open the CSV file for writing with UTF-8 encoding
with open(output_csv_file, 'w', newline='', encoding='cp932') as csvfile2:
    csv_writer = csv.writer(csvfile2)

    # Write the data to the CSV file
    csv_writer.writerows(csvfile)

print(f"CSV file '{output_csv_file}' written successfully.")
