import requests

# Thông tin tài khoản Cybozu
DOMAIN = 'union-plate'
USERNAME = '835linh'
PASSWORD = 'union4001'

# ID của sự kiện đã tồn tại trên Cybozu
event_id = '942'

# Nội dung bình luận bạn muốn thêm
comment = "本日分の読み込み完了しました。"

# Đường dẫn đến tệp tin cần đính kèm
attachment_path = r'C:\Users\DSP189\Desktop\新しいフォルダー (2)\2401151.csv'

# URL của API Cybozu để thêm bình luận vào sự kiện
add_comment_url = f'https://{DOMAIN}.cybozu.com/k/api/1/events/{event_id}/comments/add'

# Tạo bình luận
comment_data = {'content': comment}
response = requests.post(add_comment_url, auth=(USERNAME, PASSWORD), json=comment_data)

# Kiểm tra xem yêu cầu thêm bình luận có thành công không
if response.status_code == 200:
    # Kiểm tra xem có tệp tin cần đính kèm không
    if attachment_path:
        with open(attachment_path, 'rb') as f:
            files = {'file': f}
            attach_file_url = f'https://{DOMAIN}.cybozu.com/k/api/1/events/{event_id}/comments/{response.json()["id"]}/attachments/add'
            attachment_response = requests.post(attach_file_url, auth=(USERNAME, PASSWORD), files=files)
            if attachment_response.status_code == 200:
                print("Bình luận và đính kèm tệp tin thành công.")
            else:
                print("Bình luận đã được thêm nhưng không thể đính kèm tệp tin.")
    else:
        print("Bình luận đã được thêm thành công.")
else:
    print("Không thể thêm bình luận vào sự kiện trên Cybozu.")
