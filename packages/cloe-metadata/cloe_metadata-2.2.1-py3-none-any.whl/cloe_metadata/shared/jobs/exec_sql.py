import logging

from pydantic import BaseModel, Field, ValidationInfo, field_validator

from cloe_metadata import base
from cloe_metadata.base.jobs import exec_sql
from cloe_metadata.utils import base_models

logger = logging.getLogger(__name__)


class ExecSQL(BaseModel):
    """Base class for loading ExecSQL model objects."""

    base_obj: exec_sql.ExecSQL
    connections: base.Connections = Field(..., exclude=True)

    @field_validator("connections")
    @classmethod
    def sink_connection_exists(cls, value: base.Connections, info: ValidationInfo):
        base_obj: base.ExecSQL | None = info.data.get("base_obj")
        if (
            base_obj is not None
            and base_obj.connection_id not in value.get_connections()
        ):
            raise ValueError("connection_id not in connections")
        return value

    @property
    def sink_connection(self) -> base.Connection:
        return self.connections.get_connections()[self.base_obj.connection_id]

    def get_rendered_runtimes(self) -> list[str]:
        return [
            base_models.get_rendered_query(query)
            for query in sorted(self.base_obj.queries, key=lambda x: x.exec_order)
        ]

    def get_procedure_name(self) -> str:
        return f"sp_{self.base_obj.name.lower().replace(' ', '_')}"
