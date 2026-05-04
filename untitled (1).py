import tkinter as tk
from tkinter import messagebox
import requests
import json

# Файл для сохранения избранных пользователей
FAVORITES_FILE = 'favorites.json'

# Функция для поиска пользователей на GitHub
def search_user():
    username = entry.get()
    if not username:
        messagebox.showwarning("Warning", "Поле поиска не должно быть пустым!")
        return
    
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)

    if response.status_code == 200:
        user_info = response.json()
        display_user_info(user_info)
    else:
        messagebox.showerror("Error", "Пользователь не найден!")

# Функция для отображения информации о пользователе
def display_user_info(user_info):
    result_text.delete(1.0, tk.END)  # Очистка области результата
    result_text.insert(tk.END, f"Имя: {user_info['name']}\n")
    result_text.insert(tk.END, f"Логин: {user_info['login']}\n")
    result_text.insert(tk.END, f"Ссылка: {user_info['html_url']}\n")
    add_to_favorites_button['state'] = tk.NORMAL

# Функция для добавления пользователя в избранное
def add_to_favorites():
    username = entry.get()
    if username:
        favorites = load_favorites()
        if username not in favorites:
            favorites.append(username)
            save_favorites(favorites)
            messagebox.showinfo("Success", f"Пользователь {username} добавлен в избранное!")
        else:
            messagebox.showinfo("Info", "Этот пользователь уже в избранном.")

# Функция для загрузки избранных пользователей из файла
def load_favorites():
    try:
        with open(FAVORITES_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Функция для сохранения избранных пользователей в файл
def save_favorites(favorites):
    with open(FAVORITES_FILE, 'w') as f:
        json.dump(favorites, f)

# Создаем главное окно
root = tk.Tk()
root.title("GitHub User Finder")

# Поле ввода
entry = tk.Entry(root)
entry.pack(pady=10)

# Кнопка поиска
search_button = tk.Button(root, text="Поиск", command=search_user)
search_button.pack(pady=10)

# Область для отображения результатов
result_text = tk.Text(root, height=10, width=50)
result_text.pack(pady=10)

# Кнопка добавления в избранное
add_to_favorites_button = tk.Button(root, text="Добавить в избранное", command=add_to_favorites, state=tk.DISABLED)
add_to_favorites_button.pack(pady=10)

# Запуск главного цикла
root.mainloop()