import tkinter as tk
from tkinter import filedialog
import json

def submit(urls_entry, time_sleep_value_entry, result_label, urls_filename, time_sleep_filename):
    urls_values = urls_entry.get("1.0", tk.END).strip().split("\n")
    time_sleep_value = time_sleep_value_entry.get()
    
    if urls_values and time_sleep_value:
        with open(urls_filename, "w", encoding="utf-8") as file:
            json.dump({"urls": urls_values}, file, indent=4)
        with open(time_sleep_filename, "w", encoding="utf-8") as file:
            json.dump({"time_sleep": int(time_sleep_value)}, file, indent=4)
        result_label.config(text="Submitted successfully!")
    else:
        result_label.config(text="Please fill in all fields.")

def browse_urls_file(entry):
    filename = filedialog.askopenfilename(defaultextension=".json", filetypes=(("JSON files", "*.json"), ("All files", "*.*")))
    if filename:
        entry.delete(0, tk.END)
        entry.insert(0, filename)

def browse_time_sleep_file(entry):
    filename = filedialog.askopenfilename(defaultextension=".json", filetypes=(("JSON files", "*.json"), ("All files", "*.*")))
    if filename:
        entry.delete(0, tk.END)
        entry.insert(0, filename)

def create_window():
    window = tk.Tk()
    window.title("URL and Time Sleep Editor")
    
    urls_label = tk.Label(window, text="URLs:")
    urls_label.grid(row=0, column=0, padx=10, pady=5)
    urls_entry = tk.Text(window, width=50, height=5)
    urls_entry.grid(row=0, column=1, padx=10, pady=5)
    
    urls_filename_label = tk.Label(window, text="URLs File:")
    urls_filename_label.grid(row=1, column=0, padx=10, pady=5)
    urls_filename_entry = tk.Entry(window, width=50)
    urls_filename_entry.grid(row=1, column=1, padx=10, pady=5)
    browse_urls_button = tk.Button(window, text="Browse", command=lambda: browse_urls_file(urls_filename_entry))
    browse_urls_button.grid(row=1, column=2, padx=10, pady=5)
    
    time_sleep_value_label = tk.Label(window, text="Time Sleep (seconds):")
    time_sleep_value_label.grid(row=2, column=0, padx=10, pady=5)
    time_sleep_value_entry = tk.Entry(window, width=50)
    time_sleep_value_entry.grid(row=2, column=1, padx=10, pady=5)
    
    time_sleep_filename_label = tk.Label(window, text="Time Sleep File:")
    time_sleep_filename_label.grid(row=3, column=0, padx=10, pady=5)
    time_sleep_filename_entry = tk.Entry(window, width=50)
    time_sleep_filename_entry.grid(row=3, column=1, padx=10, pady=5)
    browse_time_sleep_button = tk.Button(window, text="Browse", command=lambda: browse_time_sleep_file(time_sleep_filename_entry))
    browse_time_sleep_button.grid(row=3, column=2, padx=10, pady=5)
    
    submit_button = tk.Button(window, text="Submit", command=lambda: submit(urls_entry, time_sleep_value_entry, result_label, urls_filename_entry.get(), time_sleep_filename_entry.get()))
    submit_button.grid(row=4, column=1, padx=10, pady=10)
    
    result_label = tk.Label(window, text="")
    result_label.grid(row=5, column=0, columnspan=2, padx=10, pady=5)
    
    window.mainloop()

if __name__ == "__main__":
    create_window()
