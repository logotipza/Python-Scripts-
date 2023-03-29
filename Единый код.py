import os
import datetime
import binascii
import hashlib
import zlib
import xlwt
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox, ttk
from tkcalendar import Calendar

def run_change_date():
    def change_timestamps(path, new_date):
        new_timestamp = datetime.datetime(new_date.year, new_date.month, new_date.day).timestamp()
        os.utime(path, (new_timestamp, new_timestamp))

    def browse_directory():
        folder_path = filedialog.askdirectory()
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder_path)

    def run_script():
        folder_path = folder_entry.get()
        new_date = calendar.selection_get()

        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                change_timestamps(file_path, new_date)

            for dir in dirs:
                dir_path = os.path.join(root, dir)
                change_timestamps(dir_path, new_date)

        messagebox.showinfo("Информация", "Даты создания и изменения файлов и папок успешно изменены.")

    app = tk.Toplevel()
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

    calendar = Calendar(frame, selectmode='day', year=2023, month=3, day=27)
    calendar.grid(row=3, column=0, columnspan=2, padx=5)

    run_button = tk.Button(frame, text="ОК", command=run_script)
    run_button.grid(row=3, column=2, padx=5)

    app.mainloop()

def run_compare_folders():
    def get_crc32(file_path):
        with open(file_path, 'rb') as f:
            buf = f.read()
            crc32 = format(binascii.crc32(buf), '08X')
        return crc32

    def get_files_data(folder):
        result = {}
        for root, _, files in os.walk(folder):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, folder)
                size = os.path.getsize(file_path)
                crc32 = get_crc32(file_path)
                result[relative_path] = (size, crc32)
        return result

    def save_xls(file_data1, file_data2, output_path):
        wb = xlwt.Workbook()
        ws = wb.add_sheet('output')

        headers = ["Папка 1", "Размер 1", "CRC-32 1", "Папка 2", "Размер 2", "CRC-32 2"]
        for j, header in enumerate(headers):
            ws.write(0, j, header)

        row = 1
        for key in sorted(set(file_data1.keys()) | set(file_data2.keys())):
            data1_raw = file_data1.get(key, ('-', '-'))
            data1 = (data1_raw[0], "{:,} байт".format(data1_raw[0]).replace(',', ' ') if isinstance(data1_raw[0], int) else data1_raw[0], data1_raw[1])

            data2_raw = file_data2.get(key, ('-', '-'))
            data2 = (data2_raw[0], "{:,} байт".format(data2_raw[0]).replace(',', ' ') if isinstance(data2_raw[0], int) else data2_raw[0], data2_raw[1])

            if data1 != data2:
                style = xlwt.easyxf('pattern: pattern solid, fore_colour yellow;')
            else:
                style = xlwt.XFStyle()

            row_data = [key, data1[1], data1[2], key, data2[1], data2[2]]
            for j, cell_value in enumerate(row_data):
                ws.write(row, j, cell_value, style)

            row += 1

        wb.save(output_path)

    def run_comparison(folder1, folder2):
        if folder1 and folder2:
            file_data1 = get_files_data(folder1)
            file_data2 = get_files_data(folder2)

            output_path = 'Сравнение папок - результат.xls'
            save_xls(file_data1, file_data2, output_path)

            print(f'Файл {output_path} успешно сохранен.')
        else:
            print("Вы не выбрали папки. Завершение работы.")

    def select_folder(entry):
        folder = filedialog.askdirectory()
        if folder:
            entry.delete(0, tk.END)
            entry.insert(0, folder)

    app = tk.Toplevel()
    app.title("Сравнение папок")

    frame = ttk.Frame(app, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    folder1_label = ttk.Label(frame, text="Папка 1:")
    folder1_label.grid(row=0, column=0, sticky=tk.W)

    folder1_entry = ttk.Entry(frame, width=50)
    folder1_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))

    folder1_button = ttk.Button(frame, text="Выбрать", command=lambda: select_folder(folder1_entry))
    folder1_button.grid(row=0, column=2, sticky=tk.W)

    folder2_label = ttk.Label(frame, text="Папка 2:")
    folder2_label.grid(row=1, column=0, sticky=tk.W)

    folder2_entry = ttk.Entry(frame, width=50)
    folder2_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))

    folder2_button = ttk.Button(frame, text="Выбрать", command=lambda: select_folder(folder2_entry))
    folder2_button.grid(row=1, column=2, sticky=tk.W)

    compare_button = ttk.Button(frame, text="Сравнить", command=lambda: run_comparison(folder1_entry.get(), folder2_entry.get()))
    compare_button.grid(row=2, column=0, columnspan=3, pady=(10, 0))

    app.mainloop()

def run_directory_explorer():
    def generate_xls(data):
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('output')
        worksheet.write(0, 0, "Вложенность")
        worksheet.write(0, 1, "Файл/папка")
        worksheet.write(0, 2, "Название файла с расширением")
        worksheet.write(0, 3, "Название файла")
        worksheet.write(0, 4, "Расширение")
        worksheet.write(0, 5, "Размер (Байт)")
        worksheet.write(0, 6, "CRC-32")
        for i, item in enumerate(data):
            file_name, file_extension = os.path.splitext(item[2])
            item[3], item[4] = file_name, file_extension.replace('.','')
            item[5] = "{:,} байт".format(item[5]).replace(',', ' ')
            item[6] = item[6].replace("0x", "")
            for j, val in enumerate(item[:-1]):  # удалил последний элемент "N/A"
                worksheet.write(i+1, j, val)
        workbook.save("Выгрузка данных - результат.xls")
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
                data.append([level, "Папка", item, "N/A", "N/A", os.path.getsize(item_path), "N/A", "N/A"])
                data += explore_directory(item_path, level + 1)
            else:
                data.append([level, "Файл", item, "N/A", "N/A", os.path.getsize(item_path), calculate_crc32(item_path), "N/A"])
        return data

    def select_directory():
        directory = filedialog.askdirectory()
        return directory

    def run_script():
        directory = select_directory()
        if directory:
            data = explore_directory(directory)
            generate_xls(data)

    app = tk.Toplevel()
    app.title("Directory Explorer")

    select_button = tk.Button(app, text="Выбрать папку", command=run_script)
    select_button.pack(padx=20, pady=10)

    quit_button = tk.Button(app, text="Выход", command=app.destroy)
    quit_button.pack(padx=20, pady=10)

    app.mainloop()

def main():
    root = tk.Tk()
    root.title("Для ведомости и спецфикации")

    change_date_button = tk.Button(root, text="Смена даты", command=run_change_date)
    change_date_button.pack(padx=20, pady=10)

    compare_folders_button = tk.Button(root, text="Сравнение папок", command=run_compare_folders)
    compare_folders_button.pack(padx=20, pady=10)

    directory_explorer_button = tk.Button(root, text="Выгрузка данных", command=run_directory_explorer)
    directory_explorer_button.pack(padx=20, pady=10)

    quit_button = tk.Button(root, text="Выход", command=root.quit)
    quit_button.pack(padx=20, pady=10)

    root.mainloop()

if __name__ == '__main__':
    main()

