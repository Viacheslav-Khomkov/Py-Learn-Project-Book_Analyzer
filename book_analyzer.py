import uuid
import tkinter as tk
from tkinter import ttk
import json


class Paragraph:
    def __init__(self, text, translation=None, parent=None, prev=None):
        self.__text = text
        self.__translation = translation
        self.__id = str(uuid.uuid4())
        self.__parent = parent
        self.__prev = prev

    def to_dict(self, ind_parent, ind_prev):
        return {
            'text': self.__text,
            'translation': self.__translation,
            'id': self.__id,
            'parent': ind_parent,
            'prev': ind_prev
        }

    @property
    def level(self):
        count = 0
        parent = self.__parent
        while parent != None:
            parent = parent.parent
            count += 1
        return count

    @property
    def id(self):
        return self.__id

    @property
    def parent(self):
        return self.__parent

    @parent.setter
    def parent(self, new_parent=None):
        self.__parent = new_parent

    @property
    def prev(self):
        return self.__prev

    @prev.setter
    def prev(self, value):
        self.__prev = value

    @property
    def text(self):
        return self.__text

    @property
    def translation(self):
        return self.__translation


class Book:
    def __init__(self, book_name, author, lang='en', year=None):
        self.__bookname = book_name
        self.__author = author
        self.__lang = lang
        self.__year = year
        self.paragraphs = []

    # Добавляет абзац после заданного параграфа (before_item
    # или в конец книги, если предыдущий не задан
    def append(self, new_text, new_translation=None, before_item=None):
        if before_item == None:
            # Ищем последний элемент и создаем новый на его основании
            list_length = len(self.paragraphs)
            if list_length == 0:
                new_par = Paragraph(text=new_text, translation=new_translation)  # первый абзац
            else:
                last_par = self.paragraphs[list_length - 1]
                new_par = Paragraph(text=new_text, translation=new_translation, parent=last_par.parent, prev=last_par)
            self.paragraphs.append(new_par)
        else:
            # создаем новый параграф перед  на его основании а в старом заменяем ссылку на новый
            new_par = Paragraph(text=new_text, translation=new_translation, parent=before_item.parent,
                                prev=before_item.prev)
            # Ищем индекс элемента before_item
            ind = 0
            while ind < len(self.paragraphs):
                if self.paragraphs[ind].id == before_item.id:
                    break
                else:
                    ind += 1
            self.paragraphs.insert(ind, )
            before_item.prev = new_par

    # Метод заполняет виджет treeview структурой документа
    def get_treeview(self, root):
        treeview = ttk.Treeview(root)
        treeview.heading("#0", text="Абзац")

        self.load_list_to_treeview(treeview)

        return treeview

    def to_dict(self):

        # Сначала создаем словарь индексов по ID
        dict_indexes = {}
        index = 0
        for item in self.paragraphs:
            # print(item.__id, '-->', index)
            dict_indexes[item.id] = index
            index += 1

        data_par = []
        for item in self.paragraphs:
            parent_index = '' if item.parent == None else dict_indexes[item.parent.id]
            prev_index = '' if item.prev == None else dict_indexes[item.prev.id]
            data_par.append(item.to_dict(ind_parent=parent_index, ind_prev=prev_index))

        return {
            'bookname': self.__bookname,
            'author': self.__author,
            'lang': self.__lang,
            'year': self.__year,
            'paragraphs': data_par
        }

    def from_dict(self, book_dict):

        dict_indexes = {}
        list_paragraph = []
        ind = 0
        for item in book_dict['paragraphs']:
            parent = None if item['parent'] == '' else dict_indexes[item['parent']]
            prev = None if item['prev'] == '' else dict_indexes[item['prev']]
            new_paragraph = Paragraph(item['text'], item['translation'], parent, prev)
            list_paragraph.append(new_paragraph)
            dict_indexes[ind] = new_paragraph
            ind += 1

        self.paragraphs = list_paragraph

    def to_json(self):
        return json.dumps(self.__dict__)

    # рекурсивный метод получает на вход виджет treeview и заполняет его данными из реквизита paragraphs
    def load_list_to_treeview(self, curr_treeview, parent=None, start_index=None, stop_index=None, parent_id=None):

        start_index = 0 if start_index is None else start_index
        stop_index = len(self.paragraphs) - 1 if stop_index is None else stop_index

        for index in range(start_index, stop_index):
            curr_element = self.paragraphs[index]
            if curr_element.parent == parent:
                item_id = curr_treeview.insert(
                    parent=parent_id if parent_id != None else '',
                    index="end",
                    text=curr_element.text,  # в название элемента грузим первые 25 символов абзаца
                    values=[index]
                    # values = [index, curr_element]
                )
                self.load_list_to_treeview(curr_treeview=curr_treeview, parent=curr_element, start_index=index + 1,
                                           stop_index=stop_index, parent_id=item_id)

    @staticmethod
    def load_from_json_file(file):
        book_dict = json.load(file)

        curr_book = Book(
            book_name=book_dict['bookname'],
            author=book_dict['author'],
            lang=book_dict['lang'],
            year=book_dict['year'])

        curr_book.from_dict(book_dict)
        return curr_book
