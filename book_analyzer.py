from tkinter import ttk
import json


# Описание класса:
# Элемент класса соответствует одному абзацу книги Book
# В книге абзацы идут в строгом неизменном порядке и имеют фиксированный индекс в книге
# Разрешено менять оформление абзаца: его стиль (0..5) и индекс непосредственного абзаца-заголовка
# Каждый элемент содержит кроме текста на языке книге, его перевод на язык владельца
class Paragraph:
    def __init__(self, ind: int, text: str, translation: str = '', parent_ind: int = -1, level: int = 0):
        self.__text = text
        self.__translation = translation
        self.__ind = ind
        self.__parent_ind = parent_ind
        self.__level = level

    # Properties
    @property
    def level(self):
        return self.__level

    @level.setter
    def level(self, new_level: int):
        self.__level = new_level

    @property
    def ind(self):
        return self.__ind

    @property
    def parent_ind(self):
        return self.__parent_ind

    @parent_ind.setter
    def parent_ind(self, new_parent_ind: int):
        self.__parent_ind = new_parent_ind

    @property
    def text(self):
        return self.__text

    @property
    def translation(self):
        return self.__translation

    @translation.setter
    def translation(self, new_translation: str):
        self.__translation = new_translation

    def self_to_dict(self):
        return {
            'text': self.__text,
            'translation': self.__translation,
            'ind': self.__ind,
            'parent_ind': self.__parent_ind,
            'level': self.__level
        }

    @staticmethod
    def dict_to_paragraph(cur_dict: dict):
        return Paragraph(ind=cur_dict['ind'], text=cur_dict['text'], translation=cur_dict['translation'],
                         parent_ind=cur_dict['parent_ind'], level=cur_dict['level'])

    def get_indent(self):  # Получаем отступ для элемента
        # indent = ''
        # for i in range(5 - self.level):
        #     indent += ' '
        # return indent
        return f'({self.level})' if self.level > 0 else ''


# Описание класса Book
# содержит реквизиты книги и словарь абзацев
class Book:
    def __init__(self, book_name: str, author: str, lang: str = 'en', year: int = None):
        self.__book_name = book_name
        self.__author = author
        self.__lang = lang
        self.__year = year
        self.paragraphs = {}

    @property
    def book_name(self):
        return self.__book_name

    @property
    def author(self):
        return self.__author

    @property
    def lang(self):
        return self.__lang

    @property
    def year(self):
        return self.__year

    # Добавляет абзац в конец книги. Используется при последовательной загрузке книги из файла или текста
    def append(self, new_text: str, index: int = None, new_transl: str = '', parent_index: int = -1, level: int = 0):
        if index is None:
            ind = len(self.paragraphs)  # добавляем в конец словаря
        else:
            ind = index

        self.paragraphs[ind] = Paragraph(ind=ind, text=new_text, translation=new_transl, parent_ind=parent_index,
                                         level=level)

    def self_to_dict(self):  # возвращаем словарь реквизитов для упаковки в json
        data_par: dict[int, dict[Paragraph]] = {}
        for cur_par in self.paragraphs:
            data_par[cur_par] = self.paragraphs[cur_par].self_to_dict()

        return {
            'book_name': self.__book_name,
            'author': self.__author,
            'lang': self.__lang,
            'year': self.__year,
            'paragraphs': data_par
        }

    @staticmethod
    def dict_to_book(cur_dict: dict):
        new_book = Book(book_name=cur_dict['book_name'], author=cur_dict['author'], lang=cur_dict['lang'],
                        year=cur_dict['year'])
        for par in cur_dict['paragraphs']:
            new_book.paragraphs[int(par)] = Paragraph.dict_to_paragraph(cur_dict['paragraphs'][par])

        return new_book

    def to_json(self):
        return json.dumps(self.self_to_dict())

    @staticmethod
    def load_from_json_file(file_path: str):
        with open(file_path, 'r') as file:
            book_dict = json.load(file)
            curr_book = Book.dict_to_book(book_dict)
            return curr_book

    # Метод заполняет виджет treeview структурой документа
    def get_treeview(self, treeview: ttk.Treeview):

        self.load_list_to_treeview(treeview)

    # рекурсивный метод получает на вход виджет treeview и заполняет его данными из реквизита paragraphs
    def load_list_to_treeview(self, curr_treeview, cur_ind: int = -1,
                              stop_index: int = None, treeview_parent_id: str = ''):
        stop_index = len(self.paragraphs) - 1 if stop_index is None else stop_index

        for index in range(cur_ind + 1, stop_index):
            curr_element = self.paragraphs[index]
            new_treeview_item_id = curr_treeview.insert(
                parent=treeview_parent_id,
                index="end",
                text=curr_element.get_indent() + curr_element.text,
                values=[str(index)]
            )

    def paragraph_level_up(self, par_index: int) -> list[int]:
        """
        У текущей строки изменился уровень вверх - перепривязываем все следующие элементы с уровнем меньше текущего
        пока не встретим заголовок (level > 0)
        """
        list_of_children = []  # Используем для возврата списка дочерних элементов и перемещения их в новую группу
        curr_paragraph = self.paragraphs[par_index]
        curr_level = curr_paragraph.level
        if curr_level == 5:
            return list_of_children

        curr_paragraph.level += 1
        curr_level += 1

        # Если уровень текущего родителя равен нашему устанавливаем у нас родителем его родителя
        parent_ind = curr_paragraph.parent_ind
        if parent_ind != -1 and self.paragraphs[parent_ind].level == curr_level:
            curr_paragraph.parent_ind = self.paragraphs[parent_ind].parent_ind

        # Теперь пробегаем по следующим строкам и переподчиняем с более низким уровнем
        continue_index = None  # это нужно чтобы пропускать элементы, принадлежащие вложенным группам
        for index in range(par_index + 1, len(self.paragraphs)):
            next_par = self.paragraphs[index]
            if next_par.parent_ind == continue_index:
                continue
            else:
                continue_index = None  # Вложенная группа закончилась - продолжаем анализ

            if next_par.level == 0:
                next_par.parent_ind = par_index  # Мы новый родитель
                list_of_children.append(index)
            else:
                if next_par.level < curr_level:
                    next_par.parent_ind = par_index
                    list_of_children.append(index)

                if next_par.level < curr_level: # Это группа и у нее уровень меньше чем текущий - пропускаем
                    continue_index = index
                    continue

                else:
                    break

        return list_of_children
