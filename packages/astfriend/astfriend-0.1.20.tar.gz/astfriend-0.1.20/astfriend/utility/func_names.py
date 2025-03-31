import builtins
import re
from keyword import kwlist


def camel_to_snake_upper(name: str) -> str:
    """Разбивает CamelCase на слова и соединяет их в верхнем регистре с подчёркиваниями"""
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).upper()


def camel_to_snake_lower(name: str) -> str:
    """Разбивает CamelCase на слова и соединяет их в нижнем регистре с подчёркиваниями"""
    if name.isupper():
        return name.lower()
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def camel_to_snake_lower_sygma(name: str) -> str:
    """
    Разбивает CamelCase, UPPERCASE, и смешанные стили на слова,
    соединяет их в нижнем регистре с подчёркиваниями.
    """
    if name.isupper():
        return name.lower()
    name = re.sub(r"([A-Z]+)([a-z0-9][A-Z])", r"\1_\2", name)
    name = re.sub(r"([a-z])([A-Z0-9])", r"\1_\2", name)
    return name.lower()


def camel_to_snake_lower_mz(name: str) -> str:
    """Преобразует CamelCase, PascalCase и полностью заглавные строки в snake_case"""
    # Если строка полностью в верхнем регистре, преобразуем её сразу
    if name.isupper():
        return name.lower()
    # Разбиваем строку на основе заглавных букв
    name = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
    name = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", name)
    # Приводим результат к нижнему регистру
    return name.lower()


def change_keyword_name(name: str) -> str:
    """Добавляет _ для зарезервированных слов"""
    return name + "_" if name in kwlist or name in dir(builtins) else name


def snake_to_camel(snake_str: str) -> str:
    """Преобразует строку из snake_case в camelCase."""
    components = snake_str.split("_")
    return components[0].capitalize() + "".join(
        word.capitalize() for word in components[1:]
    )


def url_name_to_camel(snake_str: str) -> str:
    """Преобразует строку c дефисами в camelCase."""
    components = snake_str.split("-")
    return components[0].capitalize() + "".join(
        word.capitalize() for word in components[1:]
    )


def hyphen_camel_to_camel(snake_str: str) -> str:
    """Преобразует строку c дефисами в camelCase. Если формат CamelCase то не меняет имя"""
    if re.match(r"^[a-z]+_([a-z0-9]+)*$", snake_str):
        return snake_to_camel(snake_str)
    components = snake_str.split("-")
    return components[0].capitalize() + "".join(
        word.capitalize() for word in components[1:]
    )


def hyphen_camel_to_snake(snake_str: str) -> str:
    """Преобразовывает формат CamelCase то отрабтывает в snake_case.
    Если в строка c дефисами то  snake_case."""
    res = camel_to_snake_lower_sygma(snake_str)
    # if re.match(r"^[a-z]+_([a-z0-9]+)*$", res):
    # if re.match(r"^[a-z]+(_[a-z0-9]+)*$", res):  # было раньше так
    if re.match(r"^[a-z0-9]+(?:_[a-z0-9]+)*(\.[a-z0-9]+)?$", res):
        return res
    else:
        components = snake_str.split("-")
        return "_".join(word.lower() for word in components)


def to_pascal_case(pascal_str: str) -> str:
    # Проверяем, является ли строка уже PascalCase
    if re.match(r"^[A-Z][a-zA-Z0-9]*$", pascal_str) and not re.search(
        r"[-_\s]", pascal_str
    ):
        return pascal_str

    # Разделяем строку на слова по пробелам, тире или подчеркиваниям
    words = re.split(r"[-_\s]", pascal_str)

    # Преобразуем каждое слово, начиная с заглавной буквы
    pascal_case = "".join(word.capitalize() for word in words)

    return pascal_case


def clean_word(word: str) -> str:
    """
    Обрабатывает слово с не числовым разделителем по типу GetPayChargesParams.SortColumn
    и возвращает GetPayChargesParamsSortColumn
    если словово изначально не имеет разделителя, возвращает его не меняя
    :param word:
    :return:
    """
    if re.fullmatch(r"[^a-zA-Z0-9]+", word):
        return word
    return re.sub(r"[^a-zA-Z0-9]+", "", word)
