from jinja2 import Template


class WarehouseGrant:
    """Represents a warehouse grant to functional role."""

    def __init__(
        self,
        name: str,
        template: Template,
        usage: bool | None = None,
        operate: bool | None = None,
        monitor: bool | None = None,
        modify: bool | None = None,
        applybudget: bool | None = None
    ) -> None:
        self.name = name
        self.usage = usage
        self.operate = operate
        self.monitor = monitor
        self.modify = modify
        self.applybudget = applybudget
        self.template = template

    def remove_grants(self) -> None:
        """Removes all set grants."""
        if self.usage is True:
            self.usage = False
        if self.operate is True:
            self.operate = False
        if self.monitor is True:
            self.monitor = False
        if self.modify is True:
            self.modify = False
        if self.applybudget is True:
            self.applybudget = False

    def gen_sql(self, role_name: str) -> str:
        """
        Generates SQL snippets for
        wh privileges.
        """
        return self.template.render(
            usage=self.usage,
            operate=self.operate,
            monitor=self.monitor,
            modify=self.modify,
            applybudget=self.applybudget,
            warehouse_name=self.name,
            role_name=role_name,
            use_doublequotes_for_name=True,
        )
