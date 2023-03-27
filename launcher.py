import tkinter as tk
from tkinter import messagebox
import script1
import script2
import script3

def run_script1():
    script1.app = tk.Toplevel()
    script1.app.title("Изменение даты создания и модификации")
    script1.frame = tk.Frame(script1.app)
    script1.frame.pack(padx=10, pady=10)
    script1.init_ui()

def run_script2():
    script2.root = tk.Toplevel()
    script2.root.title("Сравнение папок")
    script2.frame = tk.Frame(script2.root, padx=10, pady=10)
    script2.frame.pack()
    script2.init_ui()

def run_script3():
    script3.root = tk.Toplevel()
    script3.root.title("Directory Explorer")
    script3.init_ui()

def main():
    root = tk.Tk()
    root.title("Выбор скрипта")

    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack()

    button1 = tk.Button(frame, text="Поменять дату", command=run_script1, width=25)
    button1.pack(padx=5, pady=5)

    button2 = tk.Button(frame, text="Сравнить 2 папки", command=run_script2, width=25)
    button2.pack(padx=5, pady=5)

    button3 = tk.Button(frame, text="Выгрузить статистику", command=run_script3, width=25)
    button3.pack(padx=5, pady=5)

    root.mainloop()

if __name__ == '__main__':
    main()
