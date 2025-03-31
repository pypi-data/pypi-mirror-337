import ast
from enum import Enum

from astfriend.ast_python.ast_simpl_obj import AstSimpleObj, _AstObjMixin
from astfriend.ast_python.python_keywords import ExceptionKeyWords


class TenacityKeyWords(str, _AstObjMixin, Enum):
    TENACITY_ = "tenacity"
    RETRY_ = "retry"
    WAIT_FIXED_ = "wait_fixed"
    STOP_AFTER_ATTEMPT_ = "stop_after_attempt"
    RETRY_IF_EXCEPTION_TYPE_ = "retry_if_exception_type"


class AstCreateTenacityObj:
    def _get_default_retry(
        self,
        reraise_: bool = True,
        wait_: int = 5,
        stop_: int = 5,
        type_exceptions: list[ast.Name] = [ExceptionKeyWords.EXCEPTION_.ast_name_obj],
    ) -> dict[str, ast]:
        return {
            "retry": AstSimpleObj.call_(
                func_=TenacityKeyWords.TENACITY_.get_attribute_(
                    TenacityKeyWords.RETRY_IF_EXCEPTION_TYPE_.value
                ),
                args_=type_exceptions,
            ),
            "wait": AstSimpleObj.call_(
                func_=TenacityKeyWords.TENACITY_.get_attribute_(
                    TenacityKeyWords.WAIT_FIXED_.value
                ),
                args_=[AstSimpleObj.constant_(wait_)],
            ),
            "stop": AstSimpleObj.call_(
                func_=TenacityKeyWords.TENACITY_.get_attribute_(
                    TenacityKeyWords.STOP_AFTER_ATTEMPT_.value
                ),
                args_=[AstSimpleObj.constant_(stop_)],
            ),
            "reraise": AstSimpleObj.constant_(reraise_),
        }

    @staticmethod
    def create_decorator_tenacity_extended() -> ast.Call:
        return AstSimpleObj.call_alfa_attribute(
            TenacityKeyWords.TENACITY_.ast_name_obj,
            TenacityKeyWords.RETRY_.value,
            keywords_=[AstCreateTenacityObj()._get_default_retry()],
        )
