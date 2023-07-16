from PIL import Image, ImageTk


def initialize_icons():
    open_icon = Image.open("icons\\OpenFile.png")
    open_icon = open_icon.resize((16, 16))
    open_icon = ImageTk.PhotoImage(open_icon)

    remember_icon = Image.open("icons\\Remember.png")
    remember_icon = remember_icon.resize((16, 16))
    remember_icon = ImageTk.PhotoImage(remember_icon)

    save_icon = Image.open("icons\\save.png")
    save_icon = save_icon.resize((16, 16))
    save_icon = ImageTk.PhotoImage(save_icon)

    logo_icon = Image.open("icons\\logo.png")
    logo_icon = logo_icon.resize((16, 16))
    logo_icon = ImageTk.PhotoImage(logo_icon)

    level_up_icon = Image.open("icons\\LevelUp.png")
    level_up_icon = level_up_icon.resize((16, 16))
    level_up_icon = ImageTk.PhotoImage(level_up_icon)

    level_down_icon = Image.open("icons\\LevelDown.png")
    level_down_icon = level_down_icon.resize((16, 16))
    level_down_icon = ImageTk.PhotoImage(level_down_icon)

    link_to_icon = Image.open("icons\\LinkToCaption.png")
    link_to_icon = link_to_icon.resize((16, 16))
    link_to_icon = ImageTk.PhotoImage(link_to_icon)

    load_icon = Image.open("icons\\LoadFromFile.png")
    load_icon = load_icon.resize((16, 16))
    load_icon = ImageTk.PhotoImage(load_icon)

    new_file_icon = Image.open("icons\\CreateNewFile.png")
    new_file_icon = new_file_icon.resize((16, 16))
    new_file_icon = ImageTk.PhotoImage(new_file_icon)

    exit_icon = Image.open("icons\\exit.png")
    exit_icon = exit_icon.resize((16, 16))
    exit_icon = ImageTk.PhotoImage(exit_icon)

    scan_doc_icon = Image.open("icons\\scan_doc.png")
    scan_doc_icon = scan_doc_icon.resize((16, 16))
    scan_doc_icon = ImageTk.PhotoImage(scan_doc_icon)

    return open_icon, remember_icon, save_icon, logo_icon, level_up_icon, level_down_icon, link_to_icon, load_icon, \
        new_file_icon, exit_icon, scan_doc_icon


TEXT_SAMPLE = '''1. Введение
Вы можете экспериментировать с «креативностью» модели и другими параметрами, тестировать, настраивать и пробовать разные комбинации.
1.1 Что такое temperature 
temperature определяет «креативность» текста, генерируемого моделью. Чем выше значение temperature, тем креативнее и разнообразнее будет сгенерированный текст. С другой стороны, более низкая температура приведет к более «консервативному» и предсказуемому завершению. В нашем случае температура настроена на 0.3;
1.2. Пример: составление списка дел
В этом примере мы попросим модель составить список дел для создания компании в США. 
Нам нужен список из пяти пунктов.В данной статье представлены наиболее полезные особенности requests. Показано, как изменить и приспособить requests к различным ситуациям, с которыми программисты сталкиваются чаще всего. Здесь также даются советы по эффективному использованию requests и предотвращению влияния сторонних служб, которые могут сильно замедлить работу используемого приложения. Мы использовали библиотек requests в уроке по парсингу html через библиотеку BeautifulSoup.
2. Open AI
OpenAI Completions API – это мощный инструмент для генерации текста в различных контекстах. При правильных параметрах и настройках он может создавать естественно звучащий текст, соответствующий задаче.
Настроив правильные значения для некоторых параметров, таких как штрафы за частоту и присутствие, можно добиться практически идеального соответствия результатов своим потребностям.
Имея возможность остановить генерацию текста в нужный момент, пользователь также может задавать нужную длину сгенерированного текста. Эта опция также пригодится для уменьшения количества генерируемых токенов и косвенного снижения затрат.
3. Заключение
3.1 ЧТо мы изучили
Пока недостаточно было изучено.
Но мы постараемся сделать больше.
3.2 ЧТо дальше?
Этого никто не знает
'''
