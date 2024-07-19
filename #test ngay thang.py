# Mở file 'data.txt' ở chế độ đọc ('r')
line_path = r"C:\Users\DSP189\Desktop\line1.txt"
with open(line_path, 'r', encoding='utf-8') as file:
    # Duyệt qua từng dòng trong file
    for line in file:
        # In ra từng dòng
        print(line.strip())
