import ast
from typing import Any


class _AstObjMixin:
    @property
    def ast_name_obj(self):
        # Здесь self.value – это строковое представление, например, "Field"
        return AstSimpleObj.name_(id_=self.value)

    @property
    def ast_arg_obj(self):
        return AstSimpleObj.arg_(agr_name=self.value)

    @property
    def ast_constant(self):
        return AstSimpleObj.constant_(v=self.value)

    def get_attribute_(self, nv: str) -> ast.Attribute:
        return AstSimpleObj.attribute_alfa(self.value, nv)

    def get_keyword(self, nv: str) -> ast.Attribute:
        return AstSimpleObj.keyword_alfa(
            args_=[{self.value: AstSimpleObj.constant_(nv)}]
        )


class AstSimpleObj:
    CTX_ = {
        "l": ast.Load(),  # присваение obj[key] = v
        "s": ast.Store(),  # чтение значения obj[key]
        "d": ast.Del(),  # удаление del obj[key]
    }

    @staticmethod
    def creator_dict(in_dict: dict[str, str]) -> ast.Expr:
        return ast.Dict(
            keys=[ast.Constant(k) for k in in_dict.keys()],
            values=[ast.Constant(v) for v in in_dict.values()],
        )

    @staticmethod
    def annotation_fun(text: str) -> ast.Expr:
        "Анатация для функции"
        return ast.Expr(value=AstSimpleObj.constant_(text))

    @staticmethod
    def for_(target_: str, iter_: str, body_: ast) -> ast.For:
        return ast.For(
            target=AstSimpleObj.name_(target_, "s"),
            iter=AstSimpleObj.name_(iter_),
            body=[body_],
            orelse=[],
        )

    @staticmethod
    def try_except(
        body_: list[ast], handlers_: list[ast], handlers_body: list[ast]
    ) -> ast.Try:
        return ast.Try(
            body=body_,
            handlers=[
                ast.ExceptHandler(
                    type=AstSimpleObj.name_(handler), name=None, body=handlers_body
                )
                for handler in handlers_
            ],
            orelse=[],
            finalbody=[],
        )

    @staticmethod
    def assert_(
        left_obj: ast,
        type_ops: list[str],
        comparators_: list[ast.Constant],
        text_msg: [ast.Constant, ast.FormattedValue],
    ):
        return ast.Assert(
            test=ast.Compare(
                left=left_obj,
                ops=[
                    {"is_not": ast.IsNot(), "==": ast.Eq()}.get(op) for op in type_ops
                ],
                comparators=comparators_,
            ),
            msg=ast.JoinedStr(values=text_msg),
        )

    @staticmethod
    def if_expr(
        left_obj: ast,
        type_ops: list[str],
        comparators_: list[ast],
        body: ast,
        orelse: ast,
    ):
        return ast.IfExp(
            test=AstSimpleObj.compare_(
                left_obj=left_obj, type_ops=type_ops, comparators_=comparators_
            ),
            body=body,
            orelse=orelse,
        )

    @staticmethod
    def compare_(
        left_obj: ast,
        type_ops: list[str],
        comparators_: list[ast],
    ):
        return ast.Compare(
            left=left_obj,
            ops=[
                {
                    "is_not": ast.IsNot(),
                    "is": ast.Is(),
                    "==": ast.Eq(),
                }.get(op)
                for op in type_ops
            ],
            comparators=comparators_,
        )

    @staticmethod
    def arg_alfa(in_arg: dict[str, str]) -> list[ast.arg]:
        return [
            AstSimpleObj.arg_(arg, type_arg)
            for arg, type_arg in in_arg.items()
            if type_arg != "не_добавлять"
        ]

    @staticmethod
    def return_(arg_left: "str", arg_right: "str"):
        return ast.BinOp(
            left=AstSimpleObj.name_(arg_left),
            op=ast.BitOr(),
            right=AstSimpleObj.name_(arg_right),
        )

    @staticmethod
    def return_alfa(args: "str") -> ast.BinOp:
        bin_op = ast.BinOp(
            left=AstSimpleObj.name_(args[0]),
            op=ast.BitOr(),
            right=AstSimpleObj.name_(args[1]),
        )
        for arg in args[2:]:
            bin_op = ast.BinOp(
                left=bin_op, op=ast.BitOr(), right=AstSimpleObj.name_(arg)
            )
        return bin_op

    @staticmethod
    def arg_(agr_name: str, annotation: str | None = None) -> ast.arg:
        return ast.arg(arg=agr_name, annotation=annotation)

    @staticmethod
    def name_(id_: str, ctx_: str = "l") -> ast.Name:
        AstSimpleObj.CTX_.get(ctx_)
        return ast.Name(id=id_, ctx=ctx_)

    @staticmethod
    def keyword_(arg_: str, v: ast) -> ast.keyword:
        return ast.keyword(arg=arg_, value=v)

    @staticmethod
    def keyword_alfa(args_: list[dict[str, str]], ctx_: str = "l") -> list[ast.keyword]:
        "ключ - это левая часть, а значение - правая часть"
        return [
            ast.keyword(arg=k, value=AstSimpleObj.name_(v, AstSimpleObj.CTX_.get(v)))
            for arg in args_
            for k, v in arg.items()
        ]

    @staticmethod
    def constant_(v: str):
        return ast.Constant(value=v)

    @staticmethod
    def attribute_alfa(*attrs: str) -> ast.Attribute:
        """
        Принимает набор строк, описывающих последовательность атрибутов.
        Например:
            attribute_alfa("atr_1", "atr_2", "atr_n")
        Возвращает atr_1.atr_2...atr_n
        """
        if not attrs:
            raise ValueError("Нужно передать хотя бы один аргумент")
        base = AstSimpleObj.name_(attrs[0])
        for attr in attrs[1:]:
            base = AstSimpleObj.attribute_(base, attr)
        return base

    @staticmethod
    def attribute_(
        id_: str,
        attr_: str,
        ctx_: str = "l",
    ):
        return ast.Attribute(
            value=ast.Name(id=id_, ctx=ast.Load()),
            attr=attr_,
            ctx=AstSimpleObj.CTX_.get(ctx_),
        )

    @staticmethod
    def attribute_value(value_: str, attr_: str):
        return ast.Attribute(value=value_, attr=attr_, ctx=ast.Load())

    @staticmethod
    def call_(
        func_: ast,
        args_: list[Any] | None = None,
        keywords_: list[ast] | None = None,
    ):
        return ast.Call(
            func=func_,
            args=args_ if args_ is not None else [],
            keywords=keywords_ if keywords_ is not None else [],
        )

    @staticmethod
    def call_alfa(
        func_: ast,
        args_: list[Any] | None = None,
        keywords_: list[dict[str, str]] | None = None,
    ) -> ast.Call:
        return ast.Call(
            func=func_,
            args=args_ if args_ is not None else [],
            keywords=[
                ast.keyword(arg=a, value=v)
                for k in keywords_
                for a, v in k.items()
                if v != "не_добавлять"
            ]
            if keywords_ is not None
            else [],
        )

    @staticmethod
    def call_alfa_attribute(
        *attrs: str,
        args_: list[Any] | None = None,
        keywords_: list[dict[str, str]] | None = None,
    ) -> ast.Call:
        """
        Принимает последовательность имен атрибутов и дополнительные аргументы для формирования вызова.

        :param attrs: Набор строковых имен атрибутов, например: ("atr_1", "atr_2", "atr_n").
        :param args_: Список позиционных аргументов для вызова функции.
        :param keywords_: Список словарей, где ключ – имя аргумента, а значение – его значение.
                          Если значение равно "не_добавлять", соответствующий аргумент пропускается.
        :return: Объект ast.Call, представляющий вызов функции с заданными атрибутами.
        """
        return ast.Call(
            func=AstSimpleObj.attribute_alfa(*attrs),
            args=args_ if args_ is not None else [],
            keywords=[
                ast.keyword(arg=a, value=v)
                for k in keywords_
                for a, v in k.items()
                if v != "не_добавлять"
            ]
            if keywords_ is not None
            else [],
        )

    @staticmethod
    def formatted_value(value_: ast, conversion_: int = -1):
        "для f-строк"
        return ast.FormattedValue(value=value_, conversion=conversion_)

    @staticmethod
    def arguments_(
        args_: list[ast], defaults_: list[ast.Constant] | None = None
    ) -> ast.arguments:
        _defaults = []
        if defaults_ is not None:
            for default in defaults_:
                if isinstance(default, (str, ast.Constant, type(None), bool)):
                    _defaults.append(AstSimpleObj.constant_(default))
                else:
                    _defaults.append(default)
        return ast.arguments(
            posonlyargs=[],
            args=args_,
            kwonlyargs=[],
            kw_defaults=[],
            defaults=_defaults,
        )

    @staticmethod
    def assign_(targets_: list[ast], value_: ast):
        return ast.Assign(targets=targets_, value=value_)

    @staticmethod
    def subscript_list(union_objs: list[str]) -> ast.Subscript:
        "Передаем список объектов которые вернутся как list [obj1, obj2 ]"
        union_obj = union_objs[0]
        for u in union_objs[1:]:
            union_obj = ast.BinOp(left=union_obj, op=ast.BitOr(), right=u)
        return ast.Subscript(
            value=AstSimpleObj.name_("list"), slice=union_obj, ctx=ast.Load()
        )
