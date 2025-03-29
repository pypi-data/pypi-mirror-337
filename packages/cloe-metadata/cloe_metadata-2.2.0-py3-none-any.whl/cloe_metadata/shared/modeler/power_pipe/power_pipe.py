import logging

from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, field_validator

from cloe_metadata import base
from cloe_metadata.shared.modeler.power_pipe import column_mapping, lookup, source_table

logger = logging.getLogger(__name__)


class PowerPipe(BaseModel):
    """Class for advanced or shared PowerPipe functionality."""

    base_obj: base.PowerPipe
    shared_lookups: list[lookup.Lookup]
    shared_source_tables: list[source_table.SourceTable]
    shared_column_mappings: list[column_mapping.ColumnMapping]
    databases: base.Databases = Field(..., exclude=True)
    sql_templates: base.SQLTemplates = Field(..., exclude=True)
    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("databases")
    @classmethod
    def sink_table_exists(cls, value: base.Databases, info: ValidationInfo):
        base_obj: base.PowerPipe | None = info.data.get("base_obj")
        if base_obj is not None and base_obj.sink_table_id not in value.id_to_tables:
            raise ValueError("sink_table_id does not exist")
        return value

    @field_validator("sql_templates")
    @classmethod
    def sql_template_exists(cls, value: base.SQLTemplates, info: ValidationInfo):
        base_obj: base.PowerPipe | None = info.data.get("base_obj")
        if (
            base_obj is not None
            and base_obj.sql_template_id not in value.get_templates()
        ):
            raise ValueError("sql_template_id does not exist")
        return value

    @property
    def sink_table(self) -> base.Table | None:
        return self.databases.id_to_tables[self.base_obj.sink_table_id]

    @property
    def sink_schema_table(self) -> tuple[base.Schema | None, base.Table | None]:
        return self.databases.get_table_and_schema(self.base_obj.sink_table_id)

    @property
    def sql_template(self) -> base.SQLTemplate | None:
        return self.sql_templates.get_templates()[self.base_obj.sql_template_id]
