import uuid

from pydantic import BaseModel, ConfigDict

import cloe_metadata.utils.writer as writer


class SourceTable(BaseModel):
    """Dataflow SourceTable metadata model base class"""

    table_id: uuid.UUID
    order_by: int
    is_active: bool = True
    tenant_id: uuid.UUID | None = None
    model_config = ConfigDict(
        populate_by_name=True, alias_generator=writer.to_lower_camel_case
    )
