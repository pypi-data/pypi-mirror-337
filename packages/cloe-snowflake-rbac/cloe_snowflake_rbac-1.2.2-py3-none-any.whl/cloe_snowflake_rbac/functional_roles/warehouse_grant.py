from jinja2 import Template


class WarehouseGrant:
    """Represents a warehouse grant to functional role."""

    def __init__(
        self,
        name: str,
        template: Template,
        usage: bool | None = None,
        operate: bool | None = None,
    ) -> None:
        self.name = name
        self.usage = usage
        self.operate = operate
        self.template = template

    def remove_grants(self) -> None:
        """Removes all set grants."""
        if self.usage is True:
            self.usage = False
        if self.operate is True:
            self.operate = False

    def gen_sql(self, role_name: str) -> str:
        """
        Generates SQL snippets for
        wh privileges.
        """
        return self.template.render(
            usage=self.usage,
            operate=self.operate,
            warehouse_name=self.name,
            role_name=role_name,
            use_doublequotes_for_name=True,
        )
