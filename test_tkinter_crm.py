import tkinter as tk
from tkinter import ttk
import psycopg2
from tkinter import messagebox

# Kết nối tới cơ sở dữ liệu PostgreSQL
def db_connect():
    conn = psycopg2.connect(
        host="192.168.160.189",
        database="linh_work",
        user="linh",
        password="union4001"
    )
    return conn

# Hàm thực thi câu lệnh SQL SELECT
def run_query(query):
    conn = db_connect()
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    return rows

# Hàm thực thi câu lệnh SQL INSERT, UPDATE, DELETE
def run_commit(query, values):
    conn = db_connect()
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()
    conn.close()

# Hàm xử lý khi bấm nút "Thêm khách hàng"
def add_customer():
    name = name_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()
    address = address_entry.get(1.0, tk.END)
    
    query = "INSERT INTO customers (name, email, phone, address) VALUES (%s, %s, %s, %s)"
    values = (name, email, phone, address)
    run_commit(query, values)
    messagebox.showinfo("Thông báo", "Thêm khách hàng thành công")

# Hàm xử lý khi bấm nút "Hiển thị danh sách khách hàng"
def show_customers():
    customers = run_query("SELECT * FROM customers")
    customer_listbox.delete(0, tk.END)
    for customer in customers:
        customer_listbox.insert(tk.END, f"{customer[0]} - {customer[1]} - {customer[2]}")

# Tạo giao diện ứng dụng
root = tk.Tk()
root.title("Ứng dụng CRM")

# Frame chứa các entry và label
frame_customer = ttk.Frame(root)
frame_customer.pack(pady=10)

name_label = ttk.Label(frame_customer, text="Tên khách hàng:")
name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
name_entry = ttk.Entry(frame_customer, width=40)
name_entry.grid(row=0, column=1, padx=10, pady=5)

email_label = ttk.Label(frame_customer, text="Email:")
email_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
email_entry = ttk.Entry(frame_customer, width=40)
email_entry.grid(row=1, column=1, padx=10, pady=5)

phone_label = ttk.Label(frame_customer, text="Điện thoại:")
phone_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
phone_entry = ttk.Entry(frame_customer, width=40)
phone_entry.grid(row=2, column=1, padx=10, pady=5)

address_label = ttk.Label(frame_customer, text="Địa chỉ:")
address_label.grid(row=3, column=0, padx=10, pady=5, sticky="nw")
address_entry = tk.Text(frame_customer, width=30, height=5)
address_entry.grid(row=3, column=1, padx=10, pady=5, sticky="nw")

# Button để thêm khách hàng
add_btn = ttk.Button(frame_customer, text="Thêm khách hàng", command=add_customer)
add_btn.grid(row=4, column=1, padx=10, pady=10)

# Frame chứa Listbox để hiển thị danh sách khách hàng
frame_customer_list = ttk.Frame(root)
frame_customer_list.pack(pady=20)

# Listbox để hiển thị danh sách khách hàng
customer_listbox = tk.Listbox(frame_customer_list, width=50)
customer_listbox.pack(padx=10, pady=10)

# Button để hiển thị danh sách khách hàng
show_customers_btn = ttk.Button(frame_customer_list, text="Hiển thị danh sách khách hàng", command=show_customers)
show_customers_btn.pack(padx=10, pady=10)

# Main loop
root.mainloop()
