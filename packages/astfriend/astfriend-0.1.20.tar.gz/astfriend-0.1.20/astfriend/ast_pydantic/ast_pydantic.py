import ast
from enum import Enum
from typing import Dict, List, NamedTuple, Optional

from astfriend.ast_python.ast_simpl_obj import AstSimpleObj, _AstObjMixin
from astfriend.objs.keywords.python_keywords import TypeKeyWords
from astfriend.utility.func_names import (camel_to_snake_lower_mz,
                                          change_keyword_name)


class PydanticKeyWords(str, _AstObjMixin, Enum):
    """
    Enum, содержащий стандартные ключевые слова для Pydantic.

    Наследуется от _AstObjMixin, чтобы для каждого члена можно было получить
    AST-объекты (например, для генерации вызовов методов или атрибутов) через свойства.
    """

    model_validate_ = "model_validate"
    base_model_ = "BaseModel"
    root_model_ = "RootModel"
    field_ = "Field"
    validation_error_ = "ValidationError"
    pydantic_ = "ast_pydantic"
    alias_ = "alias"
    description_ = "description"
    model_dump = "model_dump"
    by_alias = "by_alias"
    model_dump_by_alias_true = "model_dump(by_alias=True)"

    @classmethod
    def get_dump_by_alias_true(cls) -> Dict[str, ast.NameConstant]:
        """
        Создает словарь для передачи в качестве ключевого аргумента при вызове метода model_dump.

        Возвращает:
            Dict[str, ast.NameConstant]: Словарь вида {'by_alias': ast.NameConstant(value=True)}.
        """
        return {cls.by_alias: ast.NameConstant(value=True)}


class CorrectName(NamedTuple):
    """
    NamedTuple для хранения измененного имени атрибута и его оригинального alias-а.

    Атрибуты:
        name_change (Optional[str]): Измененное имя (например, в snake_case) или None.
        alias (str): Исходное имя, которое может быть использовано в качестве alias-а.
    """

    name_change: Optional[str]
    alias: str


class AstCreateBaseModel:
    """
    Класс, предоставляющий набор статических методов для создания AST-структур,
    необходимых для формирования моделей Pydantic.
    """

    @staticmethod
    def create_class_standart_padantic_model(
        class_name: str,
        body: List[ast.AST],
        bases: List[ast.Name] = [PydanticKeyWords.base_model_.ast_name_obj],
    ) -> ast.ClassDef:
        """
        Создает AST-узел класса для стандартной модели Pydantic.

        Параметры:
            class_name (str): Имя создаваемого класса.
            body (List[ast.AST]): Список AST-узлов, представляющих тело класса.
            bases (List[ast.Name], optional): Список базовых классов для наследования.
                По умолчанию используется базовый класс, полученный через PydanticKeyWords.base_model_.

        Возвращает:
            ast.ClassDef: AST-узел определения класса.
        """
        return ast.ClassDef(
            name=class_name,
            bases=bases,
            keywords=[],
            body=body,
            decorator_list=[],
        )

    @staticmethod
    def get_class_model_dump(name_model: str) -> ast.Call:
        """
        Создает AST-вызов для выражения: name_model().model_dump(by_alias=True)

        Здесь создается вызов метода model_dump у экземпляра класса, созданного вызовом name_model().

        Параметры:
            name_model (str): Имя модели, для которой будет вызван метод model_dump.

        Возвращает:
            ast.Call: AST-узел вызова метода model_dump с ключевым аргументом by_alias=True.
        """
        return AstSimpleObj.call_alfa(
            func_=AstSimpleObj.attribute_value(
                value_=AstSimpleObj.call_(func_=AstSimpleObj.name_(name_model)),
                attr_=PydanticKeyWords.model_dump,
            ),
            keywords_=[PydanticKeyWords.get_dump_by_alias_true()],
        )

    @staticmethod
    def get_class_model_dump_not_call(name_model: str) -> ast.Attribute:
        """
        Создает AST-выражение для доступа к методу model_dump без вызова конструктора:
        name_model.model_dump(by_alias=True)

        Параметры:
            name_model (str): Имя модели, для которой будет получен метод model_dump.

        Возвращает:
            ast.Attribute: AST-узел доступа к атрибуту model_dump с by_alias=True.
        """
        return AstSimpleObj.attribute_value(
            value_=AstSimpleObj.name_(name_model),
            attr_=PydanticKeyWords.model_dump_by_alias_true,
        )

    @staticmethod
    def create_name_attribute(prop_name: str) -> CorrectName:
        """
        Преобразует имя свойства в корректное имя для использования в модели.

        Если имя записано в нижнем регистре, то оно остается без изменений.
        Если имя не в нижнем регистре, оно преобразуется в snake_case с помощью
        camel_to_snake_lower_mz и дополнительно корректируется функцией change_keyword_name.

        Параметры:
            prop_name (str): Исходное имя свойства.

        Возвращает:
            CorrectName: Кортеж с измененным именем и оригинальным alias-ом.
        """
        if prop_name.islower():
            # Если имя уже в нижнем регистре, оставляем его без изменений.
            return CorrectName(prop_name, prop_name)
        else:
            # Приведение имени к snake_case и корректировка, если необходимо.
            name_change: str = camel_to_snake_lower_mz(prop_name)
            name_change = change_keyword_name(name_change)
            return CorrectName(name_change, prop_name)

    @staticmethod
    def create_attribute_standard_pydantic_model(
        field_name: str,
        field_type: str,
        is_nullable: bool = False,
        alias: Optional[str] = None,
        description: Optional[str] = None,
    ) -> ast.AnnAssign:
        """
        Создает AST-узел для аннотированного присваивания (AnnAssign), представляющего
        стандартное поле модели Pydantic.

        Параметры:
            field_name (str): Имя поля или атрибута модели.
            field_type (str): Тип данных данного атрибута.
            is_nullable (bool, optional): Флаг, указывающий, может ли поле быть пустым (nullable).
            alias (Optional[str], optional): Альтернативное имя (alias) для поля, если исходное имя
                не соответствует стилю snake_case или является зарезервированным.
            description (Optional[str], optional): Описание поля, которое может быть использовано
                для документации.

        Возвращает:
            ast.AnnAssign: AST-узел аннотированного присваивания, который может включать вызов
            функции Field с соответствующими параметрами (alias и/или description), либо None,
            если alias не указан и поле не nullable.
        """
        _field_name: ast.AST = AstSimpleObj.name_(id_=field_name, ctx_="s")
        _field_name_none: ast.AST = AstSimpleObj.name_(
            id_=f"{field_type} | {TypeKeyWords.none_.value}", ctx_="s"
        )
        field_value: Optional[ast.expr] = (
            ast.Call(
                func=PydanticKeyWords.field_.ast_name_obj,
                args=[ast.Constant(value=None)] if is_nullable else [],
                keywords=[
                    *(PydanticKeyWords.alias_.get_keyword(alias) if alias else []),
                    *(
                        PydanticKeyWords.description_.get_keyword(description)
                        if description
                        else []
                    ),
                ],
            )
            if alias
            else (TypeKeyWords.none_.ast_name_obj if is_nullable else None)
        )
        return ast.AnnAssign(
            target=_field_name,
            annotation=_field_name_none if is_nullable else _field_name,
            value=field_value,
            simple=1,
        )
