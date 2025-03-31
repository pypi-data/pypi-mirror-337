import ast
from enum import Enum

from astfriend.ast_python.ast_simpl_obj import _AstObjMixin


class TypeKeyWords(str, _AstObjMixin, Enum):
    list_ = "list"
    str_ = "str"
    none_ = "None"


class ClassKeyWords(str, _AstObjMixin, Enum):
    "Класс со стандратными объектами в формате ast и текстом"
    init_ = "__init__"
    super_ = "super"
    classmethod_ = "classmethod"
    self_ = "self"
    cls_ = "cls"


class ExceptionKeyWords(str, _AstObjMixin, Enum):
    EXCEPTION_ = "Exception"
