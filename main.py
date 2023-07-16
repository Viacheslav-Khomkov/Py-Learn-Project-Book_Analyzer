import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import *
from tkinter import filedialog

from idlelib.tooltip import Hovertip

from PIL import Image, ImageTk

import json
import os
import keyboard

import const
import book_analyzer as bi


def on_selection(event):
    global select
    if text_widget.tag_ranges(tk.SEL):
        curr_selected_text = event.widget.get(tk.SEL_FIRST, tk.SEL_LAST)
        if select != curr_selected_text:
            select = curr_selected_text


def get_selected_items():
    global selected
    selected = treeview.selection()
    selected_text.set(f'Выделено: {len(selected)}')


# Выделены должны быть несколько строк подряд
# текущий новый родитель должен иметь индекс меньше выделенных
def bind_selected_items():
    curr_selected = treeview.selection()
    if len(curr_selected) != 1:
        print('Родитель может быть только один')
        return
    new_parent_in_tree = curr_selected[0]
    par_index_of_new_parent = treeview.item(new_parent_in_tree)['values'][0]
    for item in selected:
        if item > new_parent_in_tree:  # привязываем только нижестоящие
            par_index = treeview.item(item)['values'][0]
            paragraph = curr_book.paragraphs[par_index]
            paragraph.parent_ind = par_index_of_new_parent
            treeview.move(item, new_parent_in_tree, 1000)


# Заполнение дерева тестовыми значениями
def populate_treeview(treeview_, parent, data):
    for item in data:
        item_id = treeview_.insert(parent, 'end', text=item['text'])
        if 'children' in item:
            populate_treeview(treeview_, item_id, item['children'])


# Развертывание дерева в рекурсии
def expand_all(treeview_, item_id=None):
    for item in treeview_.get_children(item_id):
        treeview_.item(item, open=True)
        expand_all(treeview_, item_id)


def load_new_treeview():
    global treeview
    treeview = ttk.Treeview(root_frame)
    treeview.heading("#0", text="Абзац")

    curr_book.get_treeview(treeview)
    treeview.grid(row=0, column=0, sticky='nsew', columnspan=2)
    treeview.bind("<<TreeviewSelect>>", on_treeview_select)

    setup_statusbar()

def feel_book_attr():
    book_name.set(curr_book.book_name)
    book_author.set(curr_book.author)

# Создаем объект Book, разбиваем текст по параграфам и заполняем объект текстом
def scan_text(selected_text_):
    global curr_book
    curr_book = bi.Book('Moby-Dick', 'Herman Melville', 'en', 1851)

    paragraphs_list = selected_text_.split('\n')
    for item in paragraphs_list:
        curr_book.append(new_text=item)

    load_new_treeview()


def on_treeview_select(event):
    selected_items = treeview.selection()
    # Очищаем текст и заполняем его выделенными абзацами
    text_widget.delete("1.0", tk.END)  # Очистка текста
    for item in selected_items:
        text_widget.insert(tk.END, treeview.item(item)['text'] + '\n')  # Добавление значения

        for child_item in treeview.get_children(item):
            text_widget.insert(tk.END, treeview.item(child_item)['text'] + '\n')  # Добавление значения

            for new_child_item in treeview.get_children(child_item):
                text_widget.insert(tk.END, treeview.item(new_child_item)['text'] + '\n')  # Добавление значения


def setup_statusbar():
    status_bar.configure(
        text=f'Книга: {curr_book.book_name}. Автор: {curr_book.author}. Год: {curr_book.year}')


def new_book():
    answer = askquestion("Закрываем текущую книгу...",
                         "Текущая книга будет закрыта. Вы уверены?")
    if answer:
        if answer == 'yes':
            text_widget.delete('1.0', tk.END)
            scan_text('')
            status_bar.configure(
                text=f'Книга: <>. Автор:<>. Год: <>')

            print('Starting new book? Ответ: ' + answer)


def read_book():
    new_text = text_widget.get(1.0, tk.END)
    scan_text(new_text)


def open_book():
    global curr_book
    current_dir = os.getcwd()

    file_path = filedialog.askopenfilename(initialdir=current_dir)
    if file_path:
        print('Opening book: ' + file_path)
        curr_book = bi.Book.load_from_json_file(file_path)

        load_new_treeview()
        feel_book_attr()


def save_book():
    current_dir = os.getcwd()

    # Вызов диалога сохранения файла с начальным путем в текущем каталоге
    file_path = filedialog.asksaveasfilename(initialdir=current_dir)
    if file_path:
        print('Saving book: ' + file_path)
        with open(file_path, 'w') as file:
            json.dump(curr_book.self_to_dict(), file, indent=2, ensure_ascii=False)


def load_text_file():
    current_dir = os.getcwd()

    # Открытие диалога выбора файла
    file_path = filedialog.askopenfilename(initialdir=current_dir)
    if file_path:
        print('Opening book: ' + file_path)
        text_widget.delete('1.0', tk.END)
        with open(file_path, 'r') as file:
            for line in file:
                if line == '\n':
                    continue
                text_widget.insert(tk.END, line)


def exit_app():
    root.destroy()

def on_enter_book_name(event):
    book_name.set(entry_book_name.get())

def on_enter_book_author(event):
    book_author.set(entry_book_author.get())

def bind_level_up():
    pass

def bind_level_down():
    pass

root = tk.Tk()
root.title("Помощник чтения книг")

# %%%%%%%%%%%%%%%%%%%%% глобальные переменные %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
treeview: ttk.Treeview = None
select: str = None
curr_book: bi.Book = None  # Ссылка на открытый файл с метаданными книги
selected: list = None  # выбранные в дереве строки
selected_text = tk.StringVar()  # для отображения статуса selected строк
selected_text.set("<empty>")  # значение по умолчанию
book_name = tk.StringVar()  # для отображения и смены названия книги
book_name.set("<empty>")  # значение по умолчанию
book_author = tk.StringVar()  # для отображения и смены автора книги
book_author.set("<empty>")  # значение по умолчанию

# ***************** Создаем меню File и его команды *******************************************************



main_menu = tk.Menu(root)
root.configure(menu=main_menu)

# Инициализируем иконки
open_icon, remember_icon, save_icon, logo_icon, level_up_icon, level_down_icon, \
    link_to_icon, load_icon, new_file_icon, exit_icon, scan_doc_icon = const.initialize_icons()

first_item = tk.Menu(main_menu, tearoff=0)
main_menu.add_cascade(label="File", menu=first_item)
first_item.add_command(label="(New) Создать новую книгу", command=new_book,
                       accelerator="Ctrl+N", image=new_file_icon, compound=tk.LEFT)
first_item.add_command(label="(Open) Открыть книгу", command=open_book,
                       accelerator="Ctrl+O", image=open_icon, compound=tk.LEFT)
first_item.add_command(label="(Save as) Сохранить текущую книгу как", command=save_book,
                       accelerator="Ctrl+S", image=save_icon, compound=tk.LEFT)
first_item.add_command(label="(Load) Загрузить текст из файла", command=save_book,
                       accelerator="Ctrl+S", image=load_icon, compound=tk.LEFT)
first_item.add_separator()
first_item.add_command(label="(Exit) Завершить приложение", command=exit_app, image=exit_icon, compound=tk.LEFT)

# Привязка "горячих клавиш" к командам меню
keyboard.add_hotkey("Ctrl + N", new_book)
keyboard.add_hotkey("Ctrl + O", open_book)
keyboard.add_hotkey("Ctrl + S", save_book)
keyboard.add_hotkey("Ctrl + R", read_book)
keyboard.add_hotkey("Ctrl + L", load_text_file)

# Новый Frame для кнопок панели инструментов ++++++++++++++++++++++++++++++++++++++
toolbar = tk.Frame(root)
toolbar.pack(side=tk.TOP, fill=tk.X)

# Menu
btn1 = tk.Button(toolbar, command=read_book, image=scan_doc_icon, compound=tk.LEFT)
Hovertip(btn1, 'Прочитать загруженный текст и заполнить книгу!')
btn1.grid(row=0, column=0, padx=2, pady=2)

btn2 = tk.Button(toolbar, command=get_selected_items, image=remember_icon, compound=tk.LEFT)
Hovertip(btn2, 'Запомнить список выделенных строк!')
btn2.grid(row=0, column=1, padx=2, pady=2)

btn3 = tk.Button(toolbar, command=bind_selected_items, image=link_to_icon, compound=tk.LEFT)
Hovertip(btn3, 'Привязать выделенные к текущей строке')
btn3.grid(row=0, column=2, padx=2, pady=2)

btn4 = tk.Button(toolbar, command=bind_level_up, image=level_up_icon, compound=tk.LEFT)
Hovertip(btn4, 'Заголовок уровнем выше')
btn4.grid(row=0, column=3, padx=2, pady=2)

btn5 = tk.Button(toolbar, command=bind_level_down, image=level_down_icon, compound=tk.LEFT)
Hovertip(btn5, 'Заголовок уровнем ниже')
btn5.grid(row=0, column=4, padx=2, pady=2)

lab = tk.Label(toolbar, textvariable=selected_text)
lab.grid(row=0, column=5, padx=10, pady=2)

label_book_name = tk.Label(toolbar, text="Книга:")
label_book_name.grid(row=0, column=6, padx=10, pady=2)

entry_book_name = tk.Entry(toolbar, width=50, textvariable=book_name)
entry_book_name.grid(row=0, column=7, padx=10, pady=2)
entry_book_name.bind("<Return>", on_enter_book_name)

label_book_author = tk.Label(toolbar, text="Автор:")
label_book_author.grid(row=0, column=8, padx=10, pady=2)

entry_book_author = tk.Entry(toolbar, width=50, textvariable=book_author)
entry_book_author.grid(row=0, column=9, padx=10, pady=2)
entry_book_author.bind("<Return>", on_enter_book_author)

# Statusbar ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
status_bar = tk.Label(root, relief=tk.SUNKEN, anchor=tk.W, text="Mission complete")
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# Новый фрейм, чтобы размещать объекты в grid*********************************************
root_frame = tk.Frame(root)
root_frame.pack(fill=tk.BOTH, expand=True)

# Создаем и заполняем виджет Treeview
scan_text(const.TEXT_SAMPLE)

# ------------------------------------ Создаем виджет Text
text_widget = tk.Text(root_frame, wrap=tk.WORD)
text_widget.grid(row=0, column=2, sticky='NSEW', columnspan=2)

text_widget.bind("<ButtonRelease-1>", on_selection)

root_frame.update_idletasks()

# Настройка расширения строк и столбцов
root_frame.grid_rowconfigure(0, weight=1)
root_frame.grid_columnconfigure(0, weight=0, minsize=400)
root_frame.grid_columnconfigure(2, weight=1)

root.mainloop()
