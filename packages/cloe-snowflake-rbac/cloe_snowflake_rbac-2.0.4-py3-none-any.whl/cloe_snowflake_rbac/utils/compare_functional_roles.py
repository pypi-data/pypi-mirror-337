import logging

import cloe_snowflake_rbac.functional_roles as snow

logger = logging.getLogger(__name__)


def find_new_and_deleted_roles(
    func_old: list[snow.FunctionalRole],
    func_new: list[snow.FunctionalRole] | None = None,
) -> tuple[list[snow.FunctionalRole], list[snow.FunctionalRole]]:
    """
    Comparing functional models and find removed roles.
    """
    deleted_roles = []
    if func_new is None:
        for func_role in func_old:
            func_role.set_deleted()
            deleted_roles.append(func_role)
        return [], deleted_roles
    new_roles = []
    existing_roles = [func_role.name for func_role in func_new]
    old_roles = [func_role.name for func_role in func_old]
    for func_role in func_old:
        if func_role.name not in existing_roles:
            func_role.set_deleted()
            deleted_roles.append(func_role)
            logger.info("Role %s deleted.", func_role.name)
    new_roles += [role for role in func_new if role.name not in old_roles]
    return new_roles, deleted_roles


def find_changed_warehouses_grants(
    role_whs_old: list[snow.WarehouseGrant],
    role_whs_new: list[snow.WarehouseGrant],
) -> list[snow.WarehouseGrant]:
    """
    Comparing warehouse grants and find changed, new and
    deleted warehouse grants.
    """
    changed_warehouses = []
    existing_whs = {wh.name: wh for wh in role_whs_new}
    old_whs = [wh_grant.name for wh_grant in role_whs_old]
    for wh_grant in role_whs_old:
        if wh_grant.name not in existing_whs:
            wh_grant.remove_grants()
            changed_warehouses.append(wh_grant)
            logger.info("Warehouse grants for warehouse %s deleted.", wh_grant.name)
        elif wh_grant == existing_whs[wh_grant.name]:
            changed_warehouses.append(existing_whs[wh_grant.name])
            logger.info(
                "No changes in warehouse grants for warehouse %s.",
                wh_grant.name,
            )
        else:
            if wh_grant.usage is True and existing_whs[wh_grant.name].usage is not True:
                existing_whs[wh_grant.name].usage = False
            if (
                wh_grant.operate is True
                and existing_whs[wh_grant.name].operate is not True
            ):
                existing_whs[wh_grant.name].operate = False
            changed_warehouses.append(existing_whs[wh_grant.name])
            logger.info("Warehouse grants for warehouse %s changed.", wh_grant.name)
    changed_warehouses += [
        wh_grant for wh_grant in role_whs_new if wh_grant.name not in old_whs
    ]
    return changed_warehouses


def merge_schema_grant(
    schema_grant_old: snow.SchemaGrant,
    schema_grant_new: snow.SchemaGrant,
) -> snow.SchemaGrant:
    """
    Compares two grants and merges them. The merged schema grants
    revokes old changes.
    """
    if schema_grant_old.read is True and schema_grant_new.read is not True:
        schema_grant_new.read = False
    if schema_grant_old.write is True and schema_grant_new.write is not True:
        schema_grant_new.write = False
    if schema_grant_old.execute is True and schema_grant_new.execute is not True:
        schema_grant_new.execute = False
    if schema_grant_old.owner is True and schema_grant_new.owner is not True:
        schema_grant_new.owner = False
    return schema_grant_new


def find_changed_schema_grants(
    role_schemas_old: list[snow.SchemaGrant],
    role_schemas_new: list[snow.SchemaGrant],
) -> list[snow.SchemaGrant]:
    """
    Comparing schema grants and find changed, new and
    deleted schema grants.
    """
    changed_schemas = []
    existing_schemas = {wh.name: wh for wh in role_schemas_new}
    old_schemas = [schemas_grant.name for schemas_grant in role_schemas_old]
    for schemas_grant in role_schemas_old:
        if schemas_grant.name not in existing_schemas:
            schemas_grant.remove_grants()
            changed_schemas.append(schemas_grant)
            logger.info("Schema grants for schema %s deleted.", schemas_grant.name)
        elif schemas_grant == existing_schemas[schemas_grant.name]:
            changed_schemas.append(existing_schemas[schemas_grant.name])
            logger.info(
                "No changes in schema grants for schema %s.",
                schemas_grant.name,
            )
        else:
            merge_schema_grant(schemas_grant, existing_schemas[schemas_grant.name])
            changed_schemas.append(existing_schemas[schemas_grant.name])
            logger.info("Schema grants for schema %s changed.", schemas_grant.name)
    changed_schemas += [
        schemas_grant
        for schemas_grant in role_schemas_new
        if schemas_grant.name not in old_schemas
    ]
    return changed_schemas


def find_changed_database_grants(
    role_db_old: list[snow.DatabaseGrant],
    role_db_new: list[snow.DatabaseGrant],
) -> list[snow.DatabaseGrant]:
    """
    Comparing database grants and find changed, new and
    deleted database grants.
    """
    changed_dbs = []
    existing_dbs = {db.name: db for db in role_db_new}
    old_dbs = [db_grant.name for db_grant in role_db_old]
    for db_grant in role_db_old:
        if db_grant.name not in existing_dbs:
            db_grant.remove_grants()
            changed_dbs.append(db_grant)
            logger.info("Database grants for database %s deleted.", db_grant.name)
        elif db_grant == existing_dbs[db_grant.name]:
            changed_dbs.append(existing_dbs[db_grant.name])
            logger.info("No changes in database grants for database %s.", db_grant.name)
        else:
            if db_grant.owner is True and existing_dbs[db_grant.name].owner is not True:
                existing_dbs[db_grant.name].owner = False
            existing_dbs[db_grant.name].schemas = find_changed_schema_grants(
                db_grant.schemas,
                existing_dbs[db_grant.name].schemas,
            )
            changed_dbs.append(existing_dbs[db_grant.name])
            logger.info("Database grants for database %s changed.", db_grant.name)
    changed_dbs += [
        db_grant for db_grant in role_db_new if db_grant.name not in old_dbs
    ]
    return changed_dbs


def compare_func_model(
    func_roles_old: list[snow.FunctionalRole],
    func_roles_new: list[snow.FunctionalRole],
) -> list[snow.FunctionalRole]:
    """
    Compares two functional role models and returns
    the difference.
    """
    new_roles, deleted_roles = find_new_and_deleted_roles(
        func_roles_old,
        func_roles_new,
    )
    changed_roles = []
    existing_roles = {role.name: role for role in func_roles_new}
    for role in func_roles_old:
        if role in new_roles or role in deleted_roles:
            continue
        role.databases = find_changed_database_grants(
            role.databases,
            existing_roles[role.name].databases,
        )
        role.warehouses = find_changed_warehouses_grants(
            role.warehouses,
            existing_roles[role.name].warehouses,
        )
        role.additional_grants = existing_roles[role.name].additional_grants
        changed_roles.append(role)
        logger.info("Role %s processed.", role.name)
    return new_roles + deleted_roles + changed_roles
