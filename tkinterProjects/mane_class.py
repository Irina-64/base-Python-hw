import tkinter as tk

def add_task():
    task = task_entry.get() # здесь мы получаем слова из поля для ввода
    if task:
        task_listBox.insert(tk.END, task) # здесь с помощью константы END вставляем полученное слово в конец списка
        task_entry.delete(0, tk.END) # здесь очищаем поле для ввода, от нулевого индекса и до конца

def delete_task():
    selected_task = task_listBox.curselection() # с помощью функции **curselection** элемент, на который мы нажмём, будет передавать свой ID, индекс, в переменную  selected_task
    if selected_task:
        task_listBox.delete(selected_task) # удаляем выбранный элемент из списка

def mark_task():
    selected_task = task_listBox.curselection()
    if selected_task:
        task_listBox.itemconfig(selected_task, bg="slate blue")  # с помощью функции **itemconfig** выполненная задача изменит цвет заливки

root = tk.Tk()
root.title("Task list")
root.configure(background="HotPink")
text1 = tk.Label(root, text="Введите вашу задачу:", bg="HotPink")
text1.pack(pady=5)

task_entry = tk.Entry(root, width=30, bg="DeepPink1")
task_entry.pack(pady=10)

add_task_button = tk.Button(root, text="Добавить задачу", command=add_task)
add_task_button.pack(pady=5)

delete_button = tk.Button(root, text="Удалить задачу", command=delete_task)
delete_button.pack(pady=5)

mark_button = tk.Button(root, text="Отметить выполненную задачу", command=mark_task)
mark_button.pack(pady=5)

text2 = tk.Label(root, text="Список задач:", bg="HotPink")
text2.pack(pady=5)

task_listBox = tk.Listbox(root, height=10, width=50, bg="LightPink1")

task_listBox.pack(pady=10)

root.mainloop()