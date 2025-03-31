from enum import Enum
from typing import Any


class KeywordsAst(str, Enum):
    arg_: str
    value_: Any
