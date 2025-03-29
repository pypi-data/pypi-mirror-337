from jinja2 import Template

from cloe_snowflake_rbac.functional_roles.schema_grant import SchemaGrant


class DatabaseGrant:
    """Represents a database grant to functional role."""

    def __init__(
        self,
        name: str,
        template_db: Template,
        template_schema: Template,
        owner: bool | None = None,
        schemas: list | None = None,
    ) -> None:
        self.name = name
        self.owner = owner
        self.schemas = []
        self.template = template_db
        if schemas:
            self.schemas = [
                SchemaGrant(template=template_schema, **schema) for schema in schemas
            ]

    def remove_grants(self) -> None:
        """Removes all set grants."""
        if self.owner is True:
            self.owner = False
        for schema in self.schemas:
            schema.remove_grants()

    def _gen_sql(self, role_name: str) -> str:
        """
        Generates SQL snippets for
        database privileges.
        """
        return self.template.render(
            owner=self.owner,
            database_name=self.name,
            role_name=role_name,
            use_doublequotes_for_name=True,
        )

    def gen_sql(self, role_name: str) -> str:
        """
        Combines all snippets and queries and
        returns them.
        """
        queries = self._gen_sql(role_name)
        for schema in self.schemas:
            queries += schema.gen_sql(self.name, role_name)
        return queries
