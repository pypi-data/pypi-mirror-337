from pydantic import BaseModel

from cloe_snowflake_feature_db_clone import utils


class StageOverwrite(BaseModel):
    name: str
    schema_name: str
    storage_integration: str
    storage_url: str

    def create_overwrite(self, clone_database_name: str) -> str:
        return utils.env_sql.get_template("alter_stage.sql.j2").render(
            clone_database_name=clone_database_name,
            stage_schema=self.schema_name,
            stage_name=self.name,
            storage_integration=self.storage_integration,
            storage_url=self.storage_url,
        )
