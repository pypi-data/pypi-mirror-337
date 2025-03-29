import logging

from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, field_validator

from cloe_metadata import base

logger = logging.getLogger(__name__)


class DataSourceInfo(BaseModel):
    """Class for advanced or shared DataSourceInfo functionality."""

    base_obj: base.DataSourceInfo
    sourcesystems: base.Sourcesystems = Field(..., exclude=True)
    tenants: base.Tenants = Field(..., exclude=True)
    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("sourcesystems")
    @classmethod
    def sourcesystem_exists(cls, value: base.Sourcesystems, info: ValidationInfo):
        base_obj: base.DataSourceInfo | None = info.data.get("base_obj")
        if (
            base_obj is not None
            and base_obj.sourcesystem_id not in value.get_sourcesystems()
        ):
            raise ValueError("sourcesystem does not exist")
        return value

    @field_validator("tenants")
    @classmethod
    def tenant_exists(cls, value: base.Tenants, info: ValidationInfo):
        base_obj: base.DataSourceInfo | None = info.data.get("base_obj")
        if (
            base_obj is not None
            and base_obj.tenant_id is not None
            and base_obj.tenant_id not in value.get_tenants()
        ):
            raise ValueError("tenant does not exist")
        return value

    @property
    def tenant(self) -> base.Tenant | None:
        if self.base_obj.tenant_id is not None:
            return self.tenants.get_tenants()[self.base_obj.tenant_id]
        return None

    @property
    def sourcesystem(self) -> base.Sourcesystem:
        return self.sourcesystems.get_sourcesystems()[self.base_obj.sourcesystem_id]
