import ast

from astfriend.ast_python.ast_simpl_obj import AstSimpleObj


class AstClassDefObj:
    @staticmethod
    def get_basses(list_name_parent_class: list[str]) -> list[ast.Name]:
        return [
            ast.Name(id=name_parent_class, ctx=ast.Load())
            for name_parent_class in list_name_parent_class
        ]

    @staticmethod
    def create_class(
        class_name: str | None = None,
        class_body: list[ast] | None = None,
        list_name_parent_class: list[str] | None = None,
    ) -> ast.ClassDef:
        """
        :param class_name: - имя класса
        :param list_name_parent_class: - перечень наследований
        :param class_body:
        :return:
        """
        return ast.ClassDef(
            name=class_name if class_name is not None else "NoNameClass",
            bases=AstClassDefObj.get_basses(list_name_parent_class)
            if list_name_parent_class is not None
            else [],
            keywords=[],
            body=class_body if class_body is not None else [],
            decorator_list=[],
        )

    @staticmethod
    def assign_self(name_attribute: str, value_attribute: str):
        "формат self.name_attribute = value_attribute"
        return ast.Assign(
            targets=[AstSimpleObj.attribute_self(name_attribute)],
            value=AstSimpleObj.name_(value_attribute),
        )

    @staticmethod
    def attribute_self(name_attribute: str):
        "формат self.name_attribute"
        return AstSimpleObj.attribute_("self", name_attribute, ctx_="s")
