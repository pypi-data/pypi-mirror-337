import logging
import re

from cloe_util_snowflake_connector import snowflake_interface

logger = logging.getLogger(__name__)


def create_deploy_groups(sql_script: str) -> dict[str, str]:
    """
    Extracts headers from sql script and groups queries into
    deployment groups
    """
    deploy_groups: dict[str, str] = {}
    if "TECHNICAL_ROLES" in sql_script:
        splits = sql_script.split("-- CLOE TECHNICAL_ROLES -- ")
    elif "FUNCTIONAL_ROLES" in sql_script:
        splits = sql_script.split("-- CLOE FUNCTIONAL_ROLES -- ")
    else:
        logger.error("Malformed header or unknown role script type.")
    for split in splits:
        if len(split) < 1:
            continue
        header = split.splitlines()[0]
        if match := re.search(r"GROUP\s+(\d+)", header, re.IGNORECASE):
            group = match.group(1)
        else:
            logger.error(
                "Malformed SQL script CLOE header. Manual changes made to script?",
            )
            raise SystemExit("Malformed SQL script CLOE header.")
        if group not in deploy_groups:
            deploy_groups[group] = ""
        deploy_groups[group] += split.split("\n", maxsplit=1)[1]
    return deploy_groups


def role_deploy(
    conn: snowflake_interface.SnowflakeInterface,
    sql_script: str,
    continue_on_error: bool = True,
) -> None:
    """
    Method for deploying roles in an asynchronous way.
    """
    deploy_groups = create_deploy_groups(sql_script)
    for group in sorted(deploy_groups):
        sql_group_split = [
            query for query in deploy_groups[group].split(";") if len(query) > 1
        ]
        logger.info("Starting deployment of group: %s", group)
        conn.run_many(sql_group_split, continue_on_error=continue_on_error)
