import logging
import uuid

from pydantic import BaseModel, ConfigDict

import cloe_metadata.utils.writer as writer

logger = logging.getLogger(__name__)


class TableMapping(BaseModel):
    """SimplePipe TableMapping metadata model base class"""

    source_table_id: uuid.UUID
    sink_table_id: uuid.UUID
    order_by: int
    model_config = ConfigDict(
        populate_by_name=True, alias_generator=writer.to_lower_camel_case
    )
