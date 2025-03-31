import ast
from enum import Enum

from astfriend.ast_python.ast_simpl_obj import AstSimpleObj, _AstObjMixin


class AlureKeyWords(str, _AstObjMixin, Enum):
    ALLURE_ = "allure"
    STEP_ = "step"


class AstCreateAlureObj:
    @staticmethod
    def create_decorator_allure(description: str) -> ast.Call:
        return AstSimpleObj.call_alfa_attribute(
            AlureKeyWords.ALLURE_.value,
            AlureKeyWords.STEP_.value,
            args_=[ast.Constant(value=description)],
        )

    @staticmethod
    def create_decorator_allure_extended(args_: list[ast]) -> ast.Call:
        return AstSimpleObj.call_alfa_attribute(
            AlureKeyWords.ALLURE_.value,
            AlureKeyWords.STEP_.value,
            args_=[AstSimpleObj.constant_(a) for a in args_],
        )
