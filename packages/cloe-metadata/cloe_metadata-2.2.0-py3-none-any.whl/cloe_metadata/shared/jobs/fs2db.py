import logging
import uuid

from pydantic import BaseModel, Field, ValidationInfo, field_validator

from cloe_metadata import base
from cloe_metadata.shared import jobs
from cloe_metadata.utils.templating_engine.general_templates import env

logger = logging.getLogger(__name__)


class FS2DB(BaseModel):
    """Class for advanced or shared FS2DB functionality."""

    base_obj: base.FS2DB
    dataset_types: base.DatasetTypes = Field(..., exclude=True)
    databases: base.Databases = Field(..., exclude=True)
    connections: base.Connections = Field(..., exclude=True)
    exec_sqls: dict[uuid.UUID, jobs.ExecSQL] = Field(..., exclude=True)

    @field_validator("dataset_types")
    @classmethod
    def dataset_type_exists(cls, value: base.DatasetTypes, info: ValidationInfo):
        base_obj: base.FS2DB | None = info.data.get("base_obj")
        if (
            base_obj is not None
            and base_obj.dataset_type_id not in value.get_dataset_types()
        ):
            raise ValueError("dataset_type_id does not exist")
        return value

    @field_validator("databases")
    @classmethod
    def tables_exists(cls, value: base.Databases, info: ValidationInfo):
        base_obj: base.FS2DB | None = info.data.get("base_obj")
        if base_obj is not None and base_obj.sink_table_id not in value.id_to_tables:
            raise ValueError("id not in tables")
        return value

    @field_validator("connections")
    @classmethod
    def sink_connection_exists(cls, value: base.Connections, info: ValidationInfo):
        base_obj: base.FS2DB | None = info.data.get("base_obj")
        error_text = ""
        if (
            base_obj is not None
            and base_obj.sink_connection_id not in value.get_connections()
        ):
            error_text += "sink_connection_id "
        if (
            base_obj is not None
            and base_obj.source_connection_id not in value.get_connections()
        ):
            error_text += " source_connection_id "
        if len(error_text) > 1:
            raise ValueError(f"{error_text} not in connections")
        return value

    @field_validator("exec_sqls")
    @classmethod
    def exec_sql_exists(
        cls, value: dict[uuid.UUID, jobs.ExecSQL], info: ValidationInfo
    ):
        base_obj: base.FS2DB | None = info.data.get("base_obj")
        if (
            base_obj is not None
            and base_obj.post_load_exec_job_id is not None
            and base_obj.post_load_exec_job_id not in value
        ):
            raise ValueError("post_load_exec_job_id not in ExecSQL jobs")
        return value

    @property
    def source_connection(self) -> base.Connection:
        return self.connections.get_connections()[self.base_obj.source_connection_id]

    @property
    def sink_connection(self) -> base.Connection:
        return self.connections.get_connections()[self.base_obj.sink_connection_id]

    @property
    def sink_table(self) -> base.Table:
        return self.databases.id_to_tables[self.base_obj.sink_table_id]

    @property
    def postload_execjob(self) -> jobs.ExecSQL | None:
        if self.base_obj.post_load_exec_job_id is None:
            return None
        else:
            return self.exec_sqls[self.base_obj.post_load_exec_job_id]

    @property
    def dataset_type(self) -> base.DatasetType:
        return self.dataset_types.get_dataset_types()[self.base_obj.dataset_type_id]

    @property
    def rendered_filename_pattern(self) -> str:
        return env.from_string(self.base_obj.filename_pattern).render(
            ds_type_name=self.dataset_type.name,
            ds_type_format=self.dataset_type.storage_format,
        )

    @property
    def rendered_folder_path_pattern(self) -> str:
        return env.from_string(self.base_obj.folder_path_pattern).render(
            ds_type_name=self.dataset_type.name,
            ds_type_format=self.dataset_type.storage_format,
        )
