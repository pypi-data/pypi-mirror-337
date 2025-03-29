from jinja2 import Template


class SchemaGrant:
    """Represents a schema grant to functional role."""

    def __init__(
        self,
        name: str,
        template: Template,
        read: bool | None = None,
        write: bool | None = None,
        execute: bool | None = None,
        owner: bool | None = None,
    ) -> None:
        self.name = name
        self.read = read
        self.write = write
        self.execute = execute
        self.owner = owner
        self.template = template

    def remove_grants(self) -> None:
        """Removes all set grants."""
        if self.read is True:
            self.read = False
        if self.write is True:
            self.write = False
        if self.execute is True:
            self.execute = False
        if self.owner is True:
            self.owner = False

    def gen_sql(self, database_name: str, role_name: str) -> str:
        """
        Generates SQL snippets for
        schema privileges.
        """
        return self.template.render(
            read=self.read,
            write=self.write,
            execute=self.execute,
            owner=self.owner,
            schema_name=self.name,
            database_name=database_name,
            role_name=role_name,
            use_doublequotes_for_name=True,
        )
