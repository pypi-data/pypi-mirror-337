import ast

from pydantic import BaseModel


class ImportObj(BaseModel):
    """
    Класс для хранения информации об импорте.
    module: модуль, откуда импортируем.
    objs: список имен объектов, которые нужно импортировать.
    """

    module: str
    objs: list[str] | None = None

    def gen_ast_imports(self) -> ast.ImportFrom:
        """
        Генерирует AST-структуру импорта для данного модуля и списка объектов.
        """
        if not self.objs:
            raise ValueError("Список объектов для импорта пуст")
        return ast.ImportFrom(
            module=self.module,
            names=[ast.alias(name=obj, asname=None) for obj in self.objs],
            level=0,
        )


class ImportManager:
    """
    Класс для управления импортами.
    Здесь мы храним импорты в виде списка объектов ImportObj,
    и можем динамически добавлять нужные нам импорты.
    """

    def __init__(self):
        self.imports: list[ImportObj] = []

    def add_import(self, module: str, objs: list[str]) -> None:
        """
        Добавляет новый импорт.
        module: строка с названием модуля.
        objs: список объектов, которые нужно импортировать из этого модуля.
        """
        self.imports.append(ImportObj(module=module, objs=objs))

    def get_ast_imports(self) -> list[ast.ImportFrom]:
        """
        Возвращает список AST-импортов для всех добавленных импортов.
        """
        return [imp.gen_ast_imports() for imp in self.imports]
