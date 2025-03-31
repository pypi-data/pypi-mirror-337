import ast
from enum import Enum

from astfriend.ast_python.ast_simpl_obj import _AstObjMixin


class TypeKeyWords(str, _AstObjMixin, Enum):
    list_ = "list"
    str_ = "str"
    int_ = "int"
    dict_ = "dict"
    none_ = "None"


class ClassKeyWords(str, _AstObjMixin, Enum):
    "Класс со стандратными объектами в формате ast и текстом"
    init_ = "__init__"
    super_ = "super"
    classmethod_ = "classmethod"
    self_ = "self"
    cls_ = "cls"


class AnnotationKeyWords:
    "Класс со стандратными типами python в формате ast.name"
    list_: ast.Name = ast.Name(id="list", ctx=ast.Load())
    str_: ast.Name = ast.Name(id="str", ctx=ast.Load())
    callable_: ast.Name = ast.Name(id="callable", ctx=ast.Load())
    dict_: ast.Name = ast.Name(id="dict", ctx=ast.Load())
    none_: ast.Name = ast.Name(id="None", ctx=ast.Load())
