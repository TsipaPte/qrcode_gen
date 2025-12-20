"""Модуль с функциями, выполняющие всю работу"""

from re import fullmatch
import colorama
import qrcode

colorama.init(autoreset=True)

HINT = colorama.Fore.BLUE
ERROR = colorama.Fore.RED

def run():
    """Функция, приветствующая пользователя и запускающая меню"""

    print(colorama.Fore.MAGENTA + "Добро пожаловать в QR-Code Generator!")
    print(colorama.Fore.YELLOW + "v. 1.0.0 Release")
    print("-" * 15)

    menu()

def save_to_path(qr_obj, path):
    """Сохранить полученный QR-Код на диск"""

    print(HINT + "[NOTE] Доступные расширения: png/jpg/jpeg")

    if fullmatch(r"[a-zA-Z0-9а-яА-ЯёЁ]+\.(png|jpg|jpeg)", path):
        qr_obj.save(path)

        print(colorama.Fore.CYAN + f"Сохранено успешно. Путь: {path}")
    else:
        print(ERROR + "[!] Неправильный файл. Попробуйте другое имя файла")

def detect_text_type(text):
    """Определить разновидность введённого пользователем текст (site, email, text, card)"""

    if text == "/card":
        return create_card()

    universal = "[a-zA-Z0-9а-яА-ЯёЁ]"
    email_pattern = rf"[a-zA-Z0-9а-яА-ЯёЁ.-]+@({universal}+\.)+{universal}+"
    base_site_pattern = rf"({universal}+\.)+{universal}+(/([a-zA-Z0-9а-яА-ЯёЁ.]+)*)*"  # Без протокола
    protocol_pattern = rf"(http|https)://{base_site_pattern}" # С протоколом http:// или https://

    if fullmatch(email_pattern, text): # Проверка на почту:
        return f"mailto:{text}"

    if fullmatch(base_site_pattern, text): # Проверка на site.domain или site.domain/
        return f"https://{text}"

    if fullmatch(protocol_pattern, text): # Проверка на protocol://site.domain или protocol://site.domain/
        return text

    return text

def create_card():
    """Функция, создающая карточку сотрудника по стандарту MECARD"""

    print(HINT + "[INFO] Если вы не хотите заполнять поле, то просто ничего не вводите и нажмите Enter")
    user_card_data = {}
    mecard_string = "MECARD:"

    user_card_data["N:"] = input("[?] Введите Имя / Имя Фамилию / Фамилию / Или как Вам удобно: ")
    user_card_data["SOUND:"] = input("[?] Введите фонетическое произношение имени: ")
    user_card_data["TEL:"] = input("[?] Введите номер телефона: ")
    user_card_data["TEL-AV"] = ";" # Видео звонок, поле практически нигде не используется
    user_card_data["EMAIL:"] = input("[?] Введите email: ")
    user_card_data["NOTE:"] = input("[?] Введите доп. информацию?: ")
    user_card_data["BDAY"] = ";"
    user_card_data["ADR:"] = input("[?] Введите адрес проживания: ")
    user_card_data["URL"] = input("[?] Введите Ваш сайт: ")
    user_card_data["NICKNAME:"] = input("[?] Введите nick-name: ")
    user_card_data["ORG:"] = input("[?] Введите название организации: ")

    for key, value in user_card_data.items():
        if value == ";":
            mecard_string += value
            continue

        if not value:
            mecard_string += ";"
        else:
            mecard_string += key + value + ";"

    mecard_string += ";" # По стандарту MECARD, в конце должна стоять ещё одна ";" для обозначения конца MECARD

    return mecard_string

def correction():
    """Функция, позволяющая пользователю выбрать уровень коррекция QR-Кода"""

    correction_data = {"L": 0, "M": 1, "Q": 2, "H": 3}

    print(HINT + "[INFO]: Подсказка:")
    print(HINT + "[INFO]: L - самый компактный, но самый не устойчивый (царапины, мелкие повреждения) к износу")
    print(HINT + "[INFO]: M - средний, золотой середина, чуть устойчивей, чем L")
    print(HINT + "[INFO]: Q - более большой, устойчив также не только у царапинам но и к грязи/помятости")
    print(HINT + "[INFO]: H - самый большой по размеру, выдержит всё что угодно, даже логотип по центру (перекрывающий часть QR)")

    choice_of_correction = input("[?] Выберите тип устойчивости QR-Кода (L/M/Q/H): ").upper()

    if choice_of_correction in correction_data:
        return correction_data[choice_of_correction]

    print(ERROR + "Некорректно введены данные. Выбрано M")

    return correction_data["M"] # Золотая середина

def menu():
    """Функция, запускающая меню"""

    while True:
        choice = input("[MENU] Выберите, что вы хотите сделать (1 - генерация, 2 - выход): ")

        match choice:
            case "1":
                data = input("[GENERATE] Введите данные (наш сервис сам подстроится под вас или напишите /card - создать карточку сотрудника): ")
                data = detect_text_type(data)
                type_of_correction = correction()

                qr = qrcode.make(data, error_correction=type_of_correction) # type: ignore

                while True:
                    action = input("[?] Что сделать (1 - показать, 2 - сохранить, 3 - удалить): ")

                    match action:
                        case "1":
                            qr.show()
                            break
                        case "2":
                            file_name = input("[?] Имя файла с расширением: ")
                            save_to_path(qr, file_name)
                            break
                        case "3":
                            print(ERROR + "Файл удалён")
                            del qr
                            break
            case "2":
                break
