from jinja2 import Environment

from cloe_snowflake_rbac.functional_roles.database_grant import DatabaseGrant
from cloe_snowflake_rbac.functional_roles.warehouse_grant import WarehouseGrant


class FunctionalRole:
    """Represents a functional role in snowflake."""

    def __init__(
        self,
        name: str,
        template_env: Environment,
        warehouses: list | None = None,
        databases: list | None = None,
        additional_grants: list | None = None,
    ) -> None:
        self.name = name
        self.template_env = template_env
        self.warehouses = []
        self.databases = []
        self.additional_grants = []
        self.deploy_groups = {"1": "", "2": "", "3": ""}
        if warehouses:
            wh_template = template_env.get_template(
                "functional_roles/set_warehouse_privileges.sql.j2",
            )
            self.warehouses = [
                WarehouseGrant(template=wh_template, **wh) for wh in warehouses
            ]
        if databases:
            db_template = template_env.get_template(
                "functional_roles/set_database_privileges.sql.j2",
            )
            schema_template = template_env.get_template(
                "functional_roles/set_schema_privileges.sql.j2",
            )
            self.databases = [
                DatabaseGrant(
                    template_db=db_template,
                    template_schema=schema_template,
                    **db,
                )
                for db in databases
            ]
        if additional_grants:
            self.additional_grants = additional_grants
        self.deleted = False

    def set_deleted(self) -> None:
        """Set role to deleted state."""
        self.deleted = True

    def deploy_groups_to_script(self) -> str:
        """
        Sorts deployment groups and concats group values
        based on sorting.
        """
        all_queries = ""
        for group_name in sorted(self.deploy_groups):
            all_queries += f"-- CLOE FUNCTIONAL_ROLES -- GROUP {group_name}\n"
            all_queries += self.deploy_groups[group_name]
        return all_queries

    def gen_sql(self) -> None:
        """
        Combines all snippets and queries and
        returns them.
        """
        use_doublequotes_for_name = True
        name = f'"{self.name}"' if use_doublequotes_for_name is True else self.name
        if self.deleted:
            self.deploy_groups["1"] = f"DROP ROLE IF EXISTS {name};\n"
        else:
            self.deploy_groups["1"] = f"CREATE ROLE IF NOT EXISTS {name};\n"
            self.deploy_groups["2"] = f"GRANT ROLE {name} TO ROLE SYSADMIN;\n"
            for warehouse in self.warehouses:
                self.deploy_groups["2"] += warehouse.gen_sql(self.name)
            for database in self.databases:
                self.deploy_groups["2"] += database.gen_sql(self.name)
            self.deploy_groups["3"] += "\n".join(self.additional_grants)

    def create_sql_script(self) -> str:
        """
        Combines a list of queries and returns
        a script.
        """
        self.gen_sql()
        return self.deploy_groups_to_script()
