import tkinter as tk
import const
from tkinter import *
from tkinter.messagebox import *
from tkinter import filedialog
import book_analyzer as bi
import json
import os
import keyboard


# Событие отслеживания выделенного текста
def on_selection(event):
    global select
    # if (event.state & event.num != 1) == False:
    if text_widget.tag_ranges(tk.SEL):
        curr_selected_text = event.widget.get(tk.SEL_FIRST, tk.SEL_LAST)
        if select != curr_selected_text:
            select = curr_selected_text


def get_selected_items():
    global selected, selected_text
    selected = treeview.selection()
    selected_text.set(f'Выделено: {len(selected)}')


# Выделены должны быть несколько строк подряд
# текущий новый родитель должен иметь индекс меньше выделенных
def bind_selected_items():
    global selected
    curr_selected = treeview.selection()
    if len(curr_selected) != 1:
        print('Родитель может быть только один')
        return

    # проверяем чтобы выделенный элемент не был в списке выделенных
    index_of_new_parent = treeview.item(curr_selected)['values'][0]
    new_parent = curr_book.paragraphs[index_of_new_parent]
    for item in selected:
        if item > curr_selected[0]:
            index = treeview.item(item)['values'][0]
            paragraph = curr_book.paragraphs[index]
            treeview.move(item, curr_selected, "end")
            paragraph.parent = new_parent


# Заполнение дерева тестовыми значениями
def populate_treeview(treeview_, parent, data):
    for item in data:
        item_id = treeview_.insert(parent, 'end', text=item['text'])
        if 'children' in item:
            populate_treeview(treeview_, item_id, item['children'])


# Развертывание дерева в рекурсии
def expand_all(treeview_, item_id=None):
    # Разворачиваем все узлы
    for item in treeview_.get_children(item_id):
        treeview_.item(item, open=True)
        expand_all(treeview_, item_id)


# Создаем объект Book,
# Разбиваем текст по параграфам и заполняем объект текстом
def scan_text(selected_text_):
    global curr_book, root, treeview
    curr_book = bi.Book('Moby-Dick', 'Herman Melville', 'en', 1851)

    pars = selected_text_.split('\n')
    for item in pars:
        curr_book.append(item)

    # Теперь заполняем дерево
    # treeview.destroy()
    treeview = curr_book.get_treeview(root)
    treeview.grid(row=0, column=0, sticky='nswe', columnspan=2)
    treeview.bind("<<TreeviewSelect>>", on_treeview_select)

    setup_statusbar()

def on_treeview_select(event):
    global treeview, curr_book
    selected_items = treeview.selection()
    # Очищаем текст и заполняем его выделенными абзацами
    text_widget.delete("1.0", tk.END)  # Очистка текста
    for item in selected_items:
        text_widget.insert(tk.END, treeview.item(item)['text'] + '\n')  # Добавление значения

        for child_item in treeview.get_children(item):
            text_widget.insert(tk.END, treeview.item(child_item)['text'] + '\n')  # Добавление значения


def setup_statusbar():
    global curr_book
    status_bar.configure(text=f'Книга: {curr_book._Book__bookname}. Автор: {curr_book._Book__author}. Год: {curr_book._Book__year}')

def new_book():
    answer = askquestion("Закрываем текущую книгу...",
                         "Текущая книга будет закрыта. Вы уверены?",
                         )
    if answer:
        if answer == 'yes':
            text_widget.delete('1.0', tk.END)
            scan_text('')
            print('Starting new book? Ответ: ' + answer)

def read_book():
    new_text = text_widget.get(1.0, tk.END)
    scan_text(new_text)


def open_book():
    global treeview, curr_book
    # Получение текущего каталога
    current_dir = os.getcwd()

    # Открытие диалога выбора файла
    file_path = filedialog.askopenfilename(initialdir=current_dir)
    if file_path:
        print('Opening book: ' + file_path)
        with open(file_path, 'r') as file:
            book_dict = json.load(file)
            curr_book = bi.Book(
                book_name=book_dict['bookname'],
                author=book_dict['author'],
                lang=book_dict['lang'],
                year=book_dict['year'])

            curr_book.from_dict(book_dict)

        # Теперь заполняем дерево
        treeview.destroy()
        treeview = curr_book.get_treeview(root)
        treeview.grid(row=0, column=0, sticky='nswe', columnspan=2)
        treeview.bind("<<TreeviewSelect>>", on_treeview_select)


def save_book():
    # Получение текущего каталога
    current_dir = os.getcwd()

    # Вызов диалога сохранения файла с начальным путем в текущем каталоге
    file_path = filedialog.asksaveasfilename(initialdir=current_dir)
    if file_path:
        print('Saving book: ' + file_path)
        with open(file_path, 'w') as file:
            json.dump(curr_book.to_dict(), file, indent=2, ensure_ascii=False)
        file.close()
    # print(curr_book.to_dict())

def load_text_file():
    global curr_book
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
                # line = line.rstrip()
                text_widget.insert(tk.END, line)



def exit_app():
    root.destroy()


root_ = tk.Tk()
root_.title("Книга")

# Создаем меню File *********************************************************************************
main_menu = Menu(root_)
root_.configure(menu=main_menu)

first_item = Menu(main_menu, tearoff=0)
main_menu.add_cascade(label="File", menu=first_item)
first_item.add_command(label="New", command=new_book, accelerator="Ctrl+N")
first_item.add_command(label="Open", command=open_book, accelerator="Ctrl+O")
first_item.add_command(label="Save", command=save_book, accelerator="Ctrl+S")
first_item.add_separator()
first_item.add_command(label="Exit", command=exit_app)

# Привязка "горячих клавиш" к командам меню
keyboard.add_hotkey("Ctrl + N", new_book)
keyboard.add_hotkey("Ctrl + O", open_book)
keyboard.add_hotkey("Ctrl + S", save_book)
keyboard.add_hotkey("Ctrl + R", read_book)

# Новый Frame для кнопок панели инструментов ++++++++++++++++++++++++++++++++++++++
toolbar = Frame(root_)
toolbar.pack(side=TOP, fill=X)

# Menu
btn1 = Button(toolbar, text='Прочитать', command=read_book)
btn1.grid(row=0, column=0, padx=2, pady=2)
btn2 = Button(toolbar, text='Загрузить текст', command=load_text_file)
btn2.grid(row=0, column=2, padx=2, pady=2)

# Statusbar ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
status_bar = Label(root_, relief=SUNKEN, anchor=W, text="Mission complete")
status_bar.pack(side=BOTTOM, fill=X)

# Новый фрейм, чтобы размещать объекты в grid*********************************************
root = Frame(root_)
root.pack()

# %%%%%%%%%%%%%%%%%%%%% глобальные переменные %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
treeview = None
select = None
curr_book = None  # Ссылка на открытый файл с метаданными книги
selected = None  # выбранные в дереве строки
selected_text = tk.StringVar()  # для отображения статуса selected строк
selected_text.set("<empty>")  # значение по умолчанию

# Создаем виджет Treeview
scan_text(const.TEXT_SAMPLE)

# ------------------------------------ Создаем виджет Text
text_widget = tk.Text(root, wrap=tk.WORD)
text_widget.grid(row=0, column=2, columnspan=4)

# Привязываем обработчик события "выделение текста"
text_widget.bind("<ButtonRelease-1>", on_selection)

# Первоначальное заполнение - потом будем загружать файлы
text_widget.insert(tk.END, const.TEXT_SAMPLE)

# Добавляем кнопки на форму
btn_select = tk.Button(root, text="Запомнить выделенное...", command=get_selected_items)
btn_select.grid(row=1, column=0, padx=10, pady=10)

lab_selected = tk.Label(root, textvariable=selected_text)
lab_selected.grid(row=1, column=1, padx=10, pady=10)

btn_bind = tk.Button(root, text="Привязать к выбранному", command=bind_selected_items)
btn_bind.grid(row=1, column=2, padx=10, pady=10)

root.mainloop()
