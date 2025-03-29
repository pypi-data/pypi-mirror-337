import logging
import re

import cloe_metadata.base.repository.database as model_db
from jinja2 import Environment

from cloe_snowflake_rbac import utils

logger = logging.getLogger(__name__)


class TechnicalRoles:
    """
    TechnicalRoles class filters database objects and integrates them
    into a fully working role concept.
    """

    def __init__(
        self,
        template_env: Environment,
        database_filter_positive: str | None = None,
        database_filter_negative: str | None = None,
    ) -> None:
        self.database_filter_positive = database_filter_positive
        self.database_filter_negative = database_filter_negative
        self.template_env = template_env
        self.templates = {
            "Database": {
                "DB OWNER": {
                    "name": "technical_roles/role_db_owner.sql.j2",
                    "group": "2",
                },
            },
            "Schema": {
                "SCHEMA OWNER": {
                    "name": "technical_roles/role_ownership.sql.j2",
                    "group": "2",
                },
                "READ": {"name": "technical_roles/role_read.sql.j2", "group": "2"},
                "WRITE": {"name": "technical_roles/role_write.sql.j2", "group": "2"},
                "EXECUTE": {
                    "name": "technical_roles/role_execute.sql.j2",
                    "group": "2",
                },
            },
        }
        self.deploy_groups = {
            role["group"]: ""
            for group in self.templates.values()
            for role in group.values()
        }
        self.deploy_groups["1"] = ""

    def filter_databases(
        self,
        databases: model_db.Databases,
    ) -> list[model_db.Database]:
        """
        Method filters all database entitites based on the specified
        regex pattern.
        """
        filtered_content = []
        for database in databases.databases:
            if (
                not self.database_filter_positive
                or re.match(self.database_filter_positive, database.name)
            ) and (
                not self.database_filter_negative
                or not re.match(self.database_filter_negative, database.name)
            ):
                filtered_content.append(database)
        return filtered_content

    def deploy_groups_to_script(self) -> str:
        """
        Sorts deployment groups and concats group values
        based on sorting.
        """
        all_queries = ""
        for group_name in sorted(self.deploy_groups):
            all_queries += f"-- CLOE TECHNICAL_ROLES -- GROUP {group_name}\n"
            all_queries += self.deploy_groups[group_name]
        return all_queries

    def create_roles(
        self,
        filtered_databases_new: list[model_db.Database],
        filtered_databases_old: list[model_db.Database] | None = None,
        static_role_name_override: str | None = None,
    ) -> None:
        """
        Method creates all necessary roles for a given set of database entities
        """
        grants_only: bool = static_role_name_override is not None
        databases_to_process, schemas_to_process = utils.compare_databases(
            filtered_databases_new,
            filtered_databases_old,
        )
        for database in filtered_databases_new:
            catalog_name = database.name
            schemas = [
                schema
                for schema in database.schemas
                if catalog_name in schemas_to_process
                and schema.name in schemas_to_process[catalog_name]
            ]
            if catalog_name in databases_to_process:
                logger.info(
                    "Creating role ddls %s for database %s",
                    list(self.templates["Database"].keys()),
                    catalog_name,
                )
                for role_name, role in self.templates["Database"].items():
                    logger.debug(
                        "Creating role ddl %s for database %s",
                        role_name,
                        catalog_name,
                    )
                    self.deploy_groups["1"] += self.template_env.get_template(
                        role["name"],
                    ).render(
                        database_name=catalog_name,
                        create_role=not grants_only,
                        static_role_name_override=static_role_name_override,
                    )
                    self.deploy_groups[role["group"]] += self.template_env.get_template(
                        role["name"],
                    ).render(
                        database_name=catalog_name,
                        grant_role=True,
                        grants_only=grants_only,
                        static_role_name_override=static_role_name_override,
                    )
            else:
                logger.info(
                    "Skipping role ddls %s for database %s",
                    list(self.templates["Database"].keys()),
                    catalog_name,
                )
            for schema in schemas:
                logger.info(
                    "Creating role ddls %s for schema %s in database %s",
                    list(self.templates["Schema"].keys()),
                    schema.name,
                    catalog_name,
                )
                for role_name, role in self.templates["Schema"].items():
                    logger.debug(
                        "Creating role ddl %s for schema %s in database %s",
                        role_name,
                        schema.name,
                        catalog_name,
                    )
                    self.deploy_groups["1"] += self.template_env.get_template(
                        role["name"],
                    ).render(
                        database_name=catalog_name,
                        schema_name=schema.name,
                        create_role=not grants_only,
                    )
                    self.deploy_groups[role["group"]] += self.template_env.get_template(
                        role["name"],
                    ).render(
                        database_name=catalog_name,
                        schema_name=schema.name,
                        grant_role=True,
                        grants_only=grants_only,
                        static_role_name_override=static_role_name_override,
                    )

    def revoke_roles(
        self,
        database: model_db.Database,
        database_name_role_override: str | None = None,
    ) -> str:
        """
        Method revokes all privileges all roles of a database
        """
        catalog_name = database.name
        for role_name, role in self.templates["Database"].items():
            logger.debug(
                "Revoking role ddl %s for database %s",
                role_name,
                catalog_name,
            )
            self.deploy_groups[role["group"]] += self.template_env.get_template(
                role["name"],
            ).render(
                database_name=catalog_name,
                database_name_role_override=database_name_role_override,
                revoke_role=True,
            )
        for schema in database.schemas:
            logger.info(
                "Revoking role ddls %s for schema %s in database %s",
                list(self.templates["Schema"].keys()),
                schema.name,
                catalog_name,
            )
            for role_name, role in self.templates["Schema"].items():
                logger.debug(
                    "Revoking role ddl %s for schema %s in database %s",
                    role_name,
                    schema.name,
                    catalog_name,
                )
                self.deploy_groups[role["group"]] += self.template_env.get_template(
                    role["name"],
                ).render(
                    database_name=catalog_name,
                    database_name_role_override=database_name_role_override,
                    schema_name=schema.name,
                    revoke_role=True,
                )
        return self.deploy_groups_to_script()

    def delete_roles(
        self,
        filtered_databases_old: list[model_db.Database],
        filtered_databases_new: list[model_db.Database],
    ) -> None:
        """
        Method creates all drop roles for two sets of database entities.
        """
        self.deploy_groups["0"] = ""
        deleted_databases, deleted_schemas = utils.compare_databases(
            filtered_databases_old,
            filtered_databases_new,
        )
        for catalog_name in deleted_databases:
            logger.warning(
                "Creating drop role dmls %s for database %s",
                list(self.templates["Database"].keys()),
                catalog_name,
            )
            for role in self.templates["Database"].values():
                logger.debug(
                    "Creating drop role dml %s for database %s",
                    role["name"],
                    catalog_name,
                )
                self.deploy_groups["0"] += self.template_env.get_template(
                    role["name"],
                ).render(database_name=catalog_name, delete_role=True)
        for catalog_name, schemas in deleted_schemas.items():
            for schema_name in schemas:
                logger.warning(
                    "Creating drop role dmls %s for schema %s in database %s",
                    list(self.templates["Schema"].keys()),
                    schema_name,
                    catalog_name,
                )
                for role in self.templates["Schema"].values():
                    logger.debug(
                        "Creating drop role dmls %s for schema %s in database %s",
                        role["name"],
                        schema_name,
                        catalog_name,
                    )
                    self.deploy_groups["0"] += self.template_env.get_template(
                        role["name"],
                    ).render(
                        database_name=catalog_name,
                        schema_name=schema_name,
                        delete_role=True,
                    )

    def generate_w_cleanup(
        self,
        databases: model_db.Databases,
        databases_old: model_db.Databases,
        create_roles_incremental: bool,
    ) -> str:
        """
        Wrapper function for generating role drops for deleted database objects.
        """
        filtered_repository_new = self.filter_databases(databases)
        filtered_repository_old = self.filter_databases(databases_old)
        if create_roles_incremental:
            self.create_roles(filtered_repository_new, filtered_repository_old)
        else:
            self.create_roles(filtered_repository_new)
        self.delete_roles(filtered_repository_old, filtered_repository_new)
        return self.deploy_groups_to_script()

    def generate_wo_cleanup(
        self,
        databases: model_db.Databases,
        static_role_name_override: str | None = None,
    ) -> str:
        """
        Method calling all methods for generating role conept based on json
        cloe metadata.
        """
        repository = self.filter_databases(databases)
        self.create_roles(
            repository,
            static_role_name_override=static_role_name_override,
        )
        return self.deploy_groups_to_script()
