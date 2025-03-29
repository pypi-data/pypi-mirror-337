import copy
import logging
import pathlib
from typing import Annotated

import cloe_metadata.utils.writer as m_writer
import cloe_snowflake_rbac.utils as rbac_utils
import typer
from cloe_metadata import base
from cloe_snowflake_rbac import technical_roles
from cloe_util_snowflake_connector import connection_parameters, snowflake_interface

from cloe_snowflake_feature_db_clone import models, utils

logger = logging.getLogger(__name__)

app = typer.Typer()


@app.command()
def create_clone_scripts(
    overwrite_model_path: Annotated[
        pathlib.Path,
        typer.Option(
            help="Path to overwrite yml.",
        ),
    ],
    database_model_path: Annotated[
        pathlib.Path,
        typer.Option(
            help="Path to database model.",
        ),
    ],
    output_path: Annotated[
        pathlib.Path,
        typer.Argument(help="Path where to store the output."),
    ],
    source_database_name: Annotated[
        str,
        typer.Argument(help="Name of the database that should be cloned."),
    ],
    clone_database_name: Annotated[
        str,
        typer.Argument(help="Name of the clone."),
    ],
    grant_to: Annotated[
        str,
        typer.Option(help="Comma separated list of roles to grant privileges to."),
    ],
) -> None:
    """
    Main entrypoint function
    """
    databases, d_errors = base.Databases.read_instances_from_disk(
        database_model_path,
    )
    if len(d_errors) > 0:
        raise ValueError(
            "The provided models did not pass validation, please run validation.",
        )
    source_database_model = [
        database
        for database in databases.databases
        if database.name == source_database_name
    ][0]
    overwrite_config_raw = rbac_utils.read_yaml_from_disk(overwrite_model_path) or {}
    overwrite_config = models.OverwriteConfig(**overwrite_config_raw)
    database_clone = copy.deepcopy(source_database_model)
    database_clone.name = clone_database_name
    databases.databases = [database_clone]
    tech_roles = technical_roles.TechnicalRoles(template_env=rbac_utils.env_sql)
    tech_roles_script = ""
    for role in grant_to.split(","):
        tech_roles_script += tech_roles.generate_wo_cleanup(
            databases,
            static_role_name_override=role,
        )
    tech_roles_revoke_script = utils.prepare_clone(
        database_clone=database_clone,
        source_database_model=source_database_model,
    )
    tech_roles_script += overwrite_config.create_overwrite(clone_database_name)
    m_writer.write_string_to_disk(tech_roles_script, output_path / "finalize_clone.sql")
    m_writer.write_string_to_disk(
        tech_roles_revoke_script,
        output_path / "prepare_clone.sql",
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
    sql_script = rbac_utils.read_text_from_disk(input_sql_path / "prepare_clone.sql")
    rbac_utils.role_deploy(snowflake_conn, sql_script, continue_on_error)
    sql_script = rbac_utils.read_text_from_disk(input_sql_path / "finalize_clone.sql")
    rbac_utils.role_deploy(snowflake_conn, sql_script, continue_on_error)
