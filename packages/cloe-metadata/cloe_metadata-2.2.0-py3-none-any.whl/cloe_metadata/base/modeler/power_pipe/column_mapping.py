import logging
import uuid

from pydantic import BaseModel, ConfigDict

import cloe_metadata.utils.writer as writer

logger = logging.getLogger(__name__)


class ColumnMapping(BaseModel):
    """PowerPipe ColumnMapping metadata model base class"""

    source_column_name: str | None = None
    is_insert: bool = True
    is_update: bool = True
    is_load_on_convert_error: bool = True
    is_logging_on_convert_error: bool = True
    sink_table_id: uuid.UUID
    convert_to_datatype: str | None = None
    bk_order: int | None = None
    sink_column_name: str | None = None
    calculation: str | None = None
    on_convert_error_value: str | None = None
    on_null_value: str | None = None
    model_config = ConfigDict(
        populate_by_name=True, alias_generator=writer.to_lower_camel_case
    )
