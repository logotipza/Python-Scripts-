import os
import hashlib
import zlib
import xlwt
import tkinter as tk
from tkinter import filedialog

def generate_xls(data):
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('output')
    worksheet.write(0, 0, "Level")
    worksheet.write(0, 1, "Type")
    worksheet.write(0, 2, "Name")
    worksheet.write(0, 3, "File name")
    worksheet.write(0, 4, "File Extension")
    worksheet.write(0, 5, "Size (bytes)")
    worksheet.write(0, 6, "CRC-32")
    for i, item in enumerate(data):
        file_name, file_extension = os.path.splitext(item[2])
        item[3], item[4] = file_name, file_extension.replace('.','')
        item[5] = "{:,} байт".format(item[5]).replace(',', ' ')
        item[6] = item[6].replace("0x", "")
        for j, val in enumerate(item[:-1]):  # удалил последний элемент "N/A"
            worksheet.write(i+1, j, val)
    workbook.save("output.xls")
    print("XLS file generated successfully!")

def calculate_crc32(file_path):
    buf = open(file_path, 'rb').read()
    crc32 = format(zlib.crc32(buf) & 0xffffffff, 'x')
    return crc32.zfill(8).upper()

def explore_directory(path, level=0):
    data = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            data.append([level, "directory", item, "N/A", "N/A", os.path.getsize(item_path), "N/A", "N/A"])
            data += explore_directory(item_path, level + 1)
        else:
            data.append([level, "file", item, "N/A", "N/A", os.path.getsize(item_path), calculate_crc32(item_path), "N/A"])
    return data

def select_directory():
    directory = filedialog.askdirectory()
    return directory

def run_script():
    directory = select_directory()
    if directory:
        data = explore_directory(directory)
        generate_xls(data)

def create_gui():
    root = tk.Tk()
    root.title("Directory Explorer")

    select_button = tk.Button(root, text="Select Folder", command=run_script)
    select_button.pack(padx=20, pady=10)

    quit_button = tk.Button(root, text="Quit", command=root.quit)
    quit_button.pack(padx=20, pady=10)

    root.mainloop()

create_gui()
