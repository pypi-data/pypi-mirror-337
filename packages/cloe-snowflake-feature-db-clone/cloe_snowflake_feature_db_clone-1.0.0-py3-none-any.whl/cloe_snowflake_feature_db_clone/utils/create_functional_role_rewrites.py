import cloe_snowflake_rbac.utils as rbac_utils
from cloe_metadata import base
from cloe_snowflake_rbac import functional_roles


def create_functional_role_rewrites(
    functional_role_model: dict,
    source_database_name: str,
    clone_database_name: str,
    source_database_model: base.Database,
    grant_to: list[str],
) -> list[str]:
    tech_func_roles = [
        functional_roles.FunctionalRole(
            name=name,
            template_env=rbac_utils.env_sql,
            **attributes,
        )
        for name, attributes in functional_role_model.items()
        if source_database_name in name and name.startswith("R_T_")
    ]
    for role in tech_func_roles:
        role.name = role.name.replace(source_database_name, clone_database_name)
        role.additional_grants = [
            ad_grant.replace(source_database_name, clone_database_name)
            for ad_grant in role.additional_grants
        ]
    schema_grants = [
        {
            "name": schema.name,
            "read": True,
            "write": True,
            "execute": True,
            "owner": True,
        }
        for schema in source_database_model.schemas
    ]
    db_grant = [{"name": clone_database_name, "schemas": schema_grants}]
    new_roles = [
        functional_roles.FunctionalRole(
            name=role,
            template_env=rbac_utils.env_sql,
            databases=db_grant,
        )
        for role in grant_to
    ]
    tech_func_roles += new_roles
    func_roles_script = [role.create_sql_script() for role in tech_func_roles]
    return func_roles_script
