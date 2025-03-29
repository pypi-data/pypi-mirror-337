from pydantic import BaseModel

from .stage_overwrite import StageOverwrite


class OverwriteConfig(BaseModel):
    stage_overwrites: list[StageOverwrite]

    def create_overwrite(self, clone_database_name: str) -> str:
        overwrite_script = ""
        for stage_overwrite in self.stage_overwrites:
            overwrite_script += stage_overwrite.create_overwrite(
                clone_database_name=clone_database_name,
            )
        return overwrite_script
