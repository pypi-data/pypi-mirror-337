import cloe_snowflake_rbac.utils as rbac_utils
from cloe_metadata import base
from cloe_snowflake_rbac import technical_roles

from cloe_snowflake_feature_db_clone import utils


def prepare_clone(
    database_clone: base.Database,
    source_database_model: base.Database,
) -> str:
    tech_roles = technical_roles.TechnicalRoles(template_env=rbac_utils.env_sql)
    tech_roles_revoke_script = tech_roles.revoke_roles(
        database_clone,
        source_database_model.name,
    )
    prepare_script = utils.env_sql.get_template("clone_database.sql.j2").render(
        clone_database_name=database_clone.name,
        source_database_name=source_database_model.name,
    )
    return prepare_script + "\n" + tech_roles_revoke_script
