import logging
import pathlib
import tempfile
from typing import Annotated, Optional

import cloe_metadata.utils.writer as m_writer
import typer
from cloe_metadata import base
from cloe_util_git_client.git_client import GitClient
from cloe_util_snowflake_connector import connection_parameters, snowflake_interface

from cloe_snowflake_rbac import functional_roles, technical_roles, utils

logger = logging.getLogger(__name__)

app = typer.Typer()


@app.command()
def generate_technical_roles(
    git_root_path: Annotated[
        pathlib.Path,
        typer.Argument(help="Path to the git root folder."),
    ],
    output_path: Annotated[
        pathlib.Path,
        typer.Argument(help="Path where to store the output."),
    ],
    database_model_filepath: Annotated[
        pathlib.Path,
        typer.Option(
            help="Relative path to database model file (relative to git-root-path).",
        ),
    ],
    git_tag_regex: Annotated[
        Optional[str],  # noqa: UP007
        typer.Option(help="Regex expressions, should lead to the last deployment tag."),
    ] = None,
    database_filter_positive: Annotated[
        Optional[str],  # noqa: UP007
        typer.Option(
            help="Regex expressions, use databases matched by the expression.",
        ),
    ] = None,
    database_filter_negative: Annotated[
        Optional[str],  # noqa: UP007
        typer.Option(
            help="Regex expressions, exclude databases matched by the expression.",
        ),
    ] = None,
    use_incremental_mode: Annotated[
        bool,
        typer.Option(
            help="Use incremental mode to only create roles and grants for new objects.",
        ),
    ] = False,
) -> None:
    """
    Main entrypoint function to generate technical roles.
    """
    if use_incremental_mode and git_tag_regex is None:
        raise ValueError(
            "If use_incremental_mode is used, a git_tag_regex has to be supplied!",
        )
    databases, d_errors = base.Databases.read_instances_from_disk(
        git_root_path / database_model_filepath,
    )
    if len(d_errors) > 0:
        raise ValueError(
            "The provided models did not pass validation, please run validation.",
        )
    tech_roles = technical_roles.TechnicalRoles(
        template_env=utils.env_sql,
        database_filter_positive=database_filter_positive,
        database_filter_negative=database_filter_negative,
    )
    if git_tag_regex is None:
        tech_roles_script = tech_roles.generate_wo_cleanup(databases)
    else:
        git_client = GitClient(git_root_path, git_tag_regex)
        structure_databases_old = git_client.get_json_from_tag(database_model_filepath)
        with tempfile.TemporaryDirectory() as temp_dir:
            utils.recreate_file_structure(
                structure_databases_old,
                target_path=pathlib.Path(temp_dir),
            )
            databases_old, d_errors = base.Databases.read_instances_from_disk(
                pathlib.Path(temp_dir) / database_model_filepath,
            )
            if len(d_errors) > 0:
                raise ValueError(
                    "The provided models did not pass validation, please run validation.",
                )
            tech_roles_script = tech_roles.generate_w_cleanup(
                databases,
                databases_old,
                use_incremental_mode,
            )
    m_writer.write_string_to_disk(
        tech_roles_script, output_path / "technical_roles.sql"
    )


@app.command()
def generate_functional_roles(
    git_root_path: Annotated[
        pathlib.Path,
        typer.Argument(help="Path to the git root folder."),
    ],
    output_path: Annotated[
        pathlib.Path,
        typer.Argument(help="Path where to store the output."),
    ],
    functional_model_path: Annotated[
        pathlib.Path,
        typer.Option(
            help="Relative path to functional roles (relative to git-root-path).",
        ),
    ],
    git_tag_regex: Annotated[
        Optional[str],  # noqa: UP007
        typer.Option(help="Regex expressions, should lead to the last deployment tag."),
    ] = None,
) -> None:
    """
    Main entrypoint function to generate functional roles.
    """
    func_model = utils.read_yaml_from_disk(git_root_path / functional_model_path) or {}
    func_roles = [
        functional_roles.FunctionalRole(
            name=name,
            template_env=utils.env_sql,
            **attributes,
        )
        for name, attributes in func_model.items()
    ]
    if git_tag_regex is not None:
        git_client = GitClient(git_root_path, git_tag_regex)
        structure_functional_old_raw: dict[str, dict | list] = (
            git_client.get_yaml_from_tag(functional_model_path) or {}
        )
        func_model_old = {
            k: v
            for p, c in structure_functional_old_raw.items()
            if isinstance(c, dict)
            for k, v in c.items()
        }
        func_roles_old = [
            functional_roles.FunctionalRole(
                name=name,
                template_env=utils.env_sql,
                **attributes,
            )
            for name, attributes in func_model_old.items()
        ]
        func_roles = utils.compare_func_model(func_roles_old, func_roles)
    scripts = [role.create_sql_script() for role in func_roles]
    m_writer.write_string_to_disk(
        "\n".join(scripts), output_path / "functional_roles.sql"
    )


@app.command()
def deploy(
    input_sql_path: Annotated[
        pathlib.Path,
        typer.Argument(help="Path to where sql script is located."),
    ],
    continue_on_error: Annotated[
        bool,
        typer.Option(
            help="Fail/stop if one of the queries causes an error.",
        ),
    ] = True,
) -> None:
    """
    main entrypoint function to deploy roles
    """
    conn_params = connection_parameters.ConnectionParameters.init_from_env_variables()
    snowflake_conn = snowflake_interface.SnowflakeInterface(conn_params)
    sql_script = utils.read_text_from_disk(input_sql_path)
    utils.role_deploy(snowflake_conn, sql_script, continue_on_error)
