import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

TASKS_FILE = 'tasks.json'

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r', encoding='utf-8') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, 'w', encoding='utf-8') as file:
        json.dump(tasks, file, ensure_ascii=False, indent=4)

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Список задач")
        self.tasks = load_tasks()
        self.filtered_tasks = self.tasks

        # Создаем интерфейс
        self.create_widgets()
        self.update_task_list()

    def create_widgets(self):
        # Кнопки фильтрации
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=5)

        self.show_all_btn = tk.Button(button_frame, text="Все задачи", command=self.show_all_tasks)
        self.show_all_btn.pack(side=tk.LEFT, padx=2)

        self.show_completed_btn = tk.Button(button_frame, text="Выполненные", command=self.show_completed_tasks)
        self.show_completed_btn.pack(side=tk.LEFT, padx=2)

        self.show_pending_btn = tk.Button(button_frame, text="Невыполненные", command=self.show_pending_tasks)
        self.show_pending_btn.pack(side=tk.LEFT, padx=2)

        # Список задач
        self.tasks_listbox = tk.Listbox(self.root, width=50, height=15)
        self.tasks_listbox.pack(pady=5)

        # Панель кнопок действий
        action_frame = tk.Frame(self.root)
        action_frame.pack(pady=5)

        self.add_btn = tk.Button(action_frame, text="Добавить задачу", command=self.add_task)
        self.add_btn.pack(side=tk.LEFT, padx=2)

        self.mark_done_btn = tk.Button(action_frame, text="Отметить выполненной", command=self.mark_task_completed)
        self.mark_done_btn.pack(side=tk.LEFT, padx=2)

        self.delete_btn = tk.Button(action_frame, text="Удалить задачу", command=self.delete_task)
        self.delete_btn.pack(side=tk.LEFT, padx=2)

    def update_task_list(self):
        self.tasks_listbox.delete(0, tk.END)
        for task in self.filtered_tasks:
            status = "✓" if task['completed'] else "✗"
            display_text = f"{status} {task['description']}"
            self.tasks_listbox.insert(tk.END, display_text)

    def show_all_tasks(self):
        self.filtered_tasks = self.tasks
        self.update_task_list()

    def show_completed_tasks(self):
        self.filtered_tasks = [t for t in self.tasks if t['completed']]
        self.update_task_list()

    def show_pending_tasks(self):
        self.filtered_tasks = [t for t in self.tasks if not t['completed']]
        self.update_task_list()

    def add_task(self):
        description = simpledialog.askstring("Добавить задачу", "Введите описание задачи:")
        if description:
            new_task = {'description': description.strip(), 'completed': False}
            self.tasks.append(new_task)
            save_tasks(self.tasks)
            self.show_all_tasks()

    def get_selected_task_index(self):
        try:
            selection = self.tasks_listbox.curselection()
            if not selection:
                messagebox.showwarning("Выбор задачи", "Пожалуйста, выберите задачу.")
                return None
            index = selection[0]
            # Поскольку filtered_tasks — это срез self.tasks, получаем индекс в основном списке
            task = self.filtered_tasks[index]
            return self.tasks.index(task)
        except IndexError:
            messagebox.showerror("Ошибка", "Некорректный выбор.")
            return None

    def mark_task_completed(self):
        index = self.get_selected_task_index()
        if index is not None:
            self.tasks[index]['completed'] = True
            save_tasks(self.tasks)
            self.show_all_tasks()

    def delete_task(self):
        index = self.get_selected_task_index()
        if index is not None:
            task_desc = self.tasks[index]['description']
            del self.tasks[index]
            save_tasks(self.tasks)
            self.show_all_tasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
