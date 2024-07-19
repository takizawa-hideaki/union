import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from datetime import date

def save_to_file():
    # Lấy nội dung từ các ô nhập liệu
    date_text = date_entry.get()
    content_text = content_textbox.get("1.0", tk.END)

    # Tạo nội dung đầy đủ để ghi vào file
    full_text = f"<!DOCTYPE html>\
    <html lang=\"ja\">\
    <head>\
        <meta charset=\"utf-8\">\
        <title>お知らせ | PROFILE</title>\
        <style>\
            body {{\
        font-family: font-family: 'メイリオ', 'Meiryo', sans-serif;
      }}\
        \    
            .text_date {{\
                font-size: 0.9em;\
                margin-bottom: 0.5em;\
                  }}\    
            h1 {{\
                font-size: 5em;\n      margin-bottom: 1em;\n      font-family: 'メイリオ', 'Meiryo', sans-serif; /* Apply font family */\n    }}\n    h2 {{\n      font-size: 1.2em;\n      margin-top: 1em;\n      font-family: 'メイリオ', 'Meiryo', sans-serif; /* Apply font family */\n    }}\n    .text_content {{\n      font-size: 1em;\n      margin-bottom: 3em;\n      font-family: 'メイリオ', 'Meiryo', sans-serif; /* Apply font family */\n    }}\n    .attention {{\n      color: #FF0000;\n      font-family: 'メイリオ', 'Meiryo', sans-serif; /* Apply font family */\n    }}\n    .blue {{\n      color: #0000FF;\n      font-family: 'メイリオ', 'Meiryo', sans-serif; /* Apply font family */\n    }}\n    footer {{\n      margin-top: 2em;\n      font-size: 0.8em;\n      text-align: center;\n      font-family: 'メイリオ', 'Meiryo', sans-serif; /* Apply font family */\n    }}\n  </style>\n</head>\n<body>\n  <main id=\"information\">\n    <div class=\"wrapper\">\n      <h1>お知らせ</h1>\n      <article id=\"part1\">\n        <p class=\"text_date\"><time datetime=\"{date_text}\">{date_text}</time></p>\n        <h2>お知らせ</h2>\n        <p class=\"text_content\">\n{content_text}\n        </p>\n      </article>\n    </div>\n  </main>\n</body>\n</html>"

    # Ghi nội dung vào tệp tin
    try:
        print (full_text)
        # with open("output.html", "w", encoding="utf-8") as file:
        #     file.write(full_text.format(date_text=date_text, content_text=content_text))
        messagebox.showinfo("Success", "File saved successfully!")
    except Exception as e:
        #messagebox.showerror("Error", f"An error occurred: {str(e)}")
        print(full_text)

# Tạo giao diện
root = tk.Tk()
root.title("Create HTML Content")

# Tạo các widget
date_label = tk.Label(root, text="Date (YYYY.MM.DD):")
date_label.pack()

date_entry = tk.Entry(root)
date_entry.pack()

content_label = tk.Label(root, text="Content:")
content_label.pack()

content_textbox = scrolledtext.ScrolledText(root, width=50, height=10)
content_textbox.pack()

save_button = tk.Button(root, text="Save to File", command=save_to_file)
save_button.pack()

# Chạy main loop của tkinter
root.mainloop()
