import logging

from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, field_validator

from cloe_metadata import base
from cloe_metadata.base.modeler.dataflow import source_table

logger = logging.getLogger(__name__)


class SourceTable(BaseModel):
    """Class for advanced or shared SourceTable functionality."""

    base_obj: source_table.SourceTable
    databases: base.Databases = Field(..., exclude=True)
    tenants: base.Tenants = Field(..., exclude=True)
    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("databases")
    @classmethod
    def table_exists(cls, value: base.Databases, info: ValidationInfo):
        base_obj: source_table.SourceTable | None = info.data.get("base_obj")
        if base_obj is not None and base_obj.table_id not in value.id_to_tables:
            raise ValueError("table_id does not exist")
        return value

    @field_validator("tenants")
    @classmethod
    def tenant_exists(cls, value: base.Tenants, info: ValidationInfo):
        base_obj: source_table.SourceTable | None = info.data.get("base_obj")
        if (
            base_obj is not None
            and base_obj.tenant_id is not None
            and base_obj.tenant_id not in value.get_tenants()
        ):
            raise ValueError("tenant_id does not exist")
        return value

    @property
    def source_table(self) -> base.Table | None:
        return self.databases.id_to_tables[self.base_obj.table_id]

    @property
    def source_schema_table(self) -> tuple[base.Schema | None, base.Table | None]:
        return self.databases.get_table_and_schema(self.base_obj.table_id)

    @property
    def tenant(self) -> base.Tenant | None:
        if self.base_obj.tenant_id is not None:
            return self.tenants.get_tenants()[self.base_obj.tenant_id]
        return None
