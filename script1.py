# Смена даты

import os
import datetime
import tkinter as tk
from tkinter import filedialog
from tkcalendar import DateEntry
from tkinter import messagebox

def change_timestamps(path, new_date):
    new_timestamp = datetime.datetime(new_date.year, new_date.month, new_date.day).timestamp()
    os.utime(path, (new_timestamp, new_timestamp))

def browse_directory():
    folder_path = filedialog.askdirectory()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder_path)

def run_script():
    folder_path = folder_entry.get()
    new_date = datetime.datetime.strptime(calendar.get(), "%d.%m.%Y").date()

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            change_timestamps(file_path, new_date)

        for dir in dirs:
            dir_path = os.path.join(root, dir)
            change_timestamps(dir_path, new_date)

    messagebox.showinfo("Информация", "Даты создания и изменения файлов и папок успешно изменены.")

app = tk.Tk()
app.title("Изменение даты создания и модификации")

frame = tk.Frame(app)
frame.pack(padx=10, pady=10)

folder_label = tk.Label(frame, text="Путь к папке:")
folder_label.grid(row=0, column=0, sticky=tk.W)

folder_entry = tk.Entry(frame, width=50)
folder_entry.grid(row=1, column=0, columnspan=2, padx=5)

browse_button = tk.Button(frame, text="Обзор...", command=browse_directory)
browse_button.grid(row=1, column=2, padx=5)

date_label = tk.Label(frame, text="Выберите дату:")
date_label.grid(row=2, column=0, pady=10, sticky=tk.W)

calendar = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd.mm.yyyy')
calendar.grid(row=3, column=0, columnspan=2, padx=5)

run_button = tk.Button(frame, text="ОК", command=run_script)
run_button.grid(row=3, column=2, padx=5)

app.mainloop()
