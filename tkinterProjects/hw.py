import tkinter as tk
from tkinter import messagebox

def greet():
    name = entry.get()
    messagebox.showinfo("Приветствие", f"Привет, {name}!")

# Создаем главное окно
root = tk.Tk()
root.title("Ввод имени")

# Создаем метку
label = tk.Label(root, text="Введите ваше имя:")
label.pack(padx=10, pady=5)

# Создаем поле для ввода
entry = tk.Entry(root)
entry.pack(padx=10, pady=5)

# Создаем кнопку
greet_button = tk.Button(root, text="Поздороваться", command=greet)
greet_button.pack(padx=10, pady=10)

# Запускаем главный цикл
root.mainloop()