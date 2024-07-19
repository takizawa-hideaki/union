import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Cấu hình logging
logging.basicConfig(filename='logfile.log', level=logging.ERROR)

try:
    # Thử thực hiện một thao tác có thể gây lỗi
    # Ví dụ:
    result = 1 / 0
except ZeroDivisionError as e:
    # Ghi log lỗi
    logging.error(f'Error: {str(e)}')
    # In ra thông báo lỗi
    print(f'Error: {str(e)}')

    try:
    # Gửi email cảnh báo
        sender_email = "r-tong@union-plate.co.jp"
        receiver_email = "r-tong@union-plate.co.jp"
        password = "q9EH2j4t"

        subject = "Chương trình gặp lỗi!"
        body = f"Chương trình của bạn gặp lỗi. Chi tiết: {str(e)}"

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL("union-plate.cybermail.jp", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
    except Exception as email_error:
            # Ghi log lỗi khi gửi email
            logging.error(f'Error when sending email: {str(email_error)}')
        # In ra thông báo lỗi
            print(f'Error when sending email: {str(email_error)}')

# Xử lý các lỗi phát sinh trong khối try
except Exception as outer_exception:
    # Ghi log lỗi
    logging.error(f'Unhandled error: {str(outer_exception)}')
    # In ra thông báo lỗi
    print(f'Unhandled error: {str(outer_exception)}')


