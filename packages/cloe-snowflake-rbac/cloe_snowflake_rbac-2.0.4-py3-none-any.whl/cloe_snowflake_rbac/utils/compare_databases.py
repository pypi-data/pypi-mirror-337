import logging

import cloe_metadata.base.repository.database as model_db

logger = logging.getLogger(__name__)


def find_missing_schemas_in_databases(
    database_old: model_db.Database,
    database_new: model_db.Database | None = None,
) -> list[str]:
    """
    Comparing two databases and return list of schemas not existing in
    new database.
    """
    if database_new is None:
        return [schema.name for schema in database_old.schemas]
    missing_schemas: list[str] = []
    existing_schemas = [schema.name for schema in database_new.schemas]
    for schema in database_old.schemas:
        if schema.name not in existing_schemas:
            missing_schemas.append(schema.name)
            logger.debug(
                "Schema %s in database %s is missing.",
                schema.name,
                database_old.name,
            )
    return missing_schemas


def find_missing_databases(
    databases_old: list[model_db.Database] | None,
    databases_new: list[model_db.Database] | None,
) -> list[str]:
    """Comparing two lists of databases and return the list of databases not existing in
    new databases list.

    Args:
        databases_old (list[dict]): _description_
        databases_new (list[dict]): _description_

    Returns:
        tuple: _description_
    """
    old_names = [db.name for db in databases_old] if databases_old is not None else []
    new_names = [db.name for db in databases_new] if databases_new is not None else []
    missing_databases: list[str] = [name for name in old_names if name not in new_names]
    return missing_databases


def compare_databases(
    repo_old: list[model_db.Database] | None,
    repo_new: list[model_db.Database] | None,
) -> tuple[list, dict]:
    """Comparing two repositories and returns name of missing databases and schemas.

    Args:
        repo_new (dict): _description_
        repo_old (dict): _description_

    Returns:
        tuple: _description_
    """
    missing_databases = find_missing_databases(repo_old, repo_new)
    missing_schemas_in_databases = {}
    existing_dbs = (
        {database.name: database for database in repo_new}
        if repo_new is not None
        else {}
    )
    for database in repo_old if repo_old is not None else []:
        missing_schemas_in_databases[database.name] = find_missing_schemas_in_databases(
            database,
            existing_dbs[database.name] if database.name in existing_dbs else None,
        )
    return missing_databases, missing_schemas_in_databases
