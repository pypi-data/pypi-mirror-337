from __future__ import annotations

import logging
import uuid
from typing import ClassVar

from pydantic import field_validator

from cloe_metadata.base.base import WithoutSubfoldersMixin
from cloe_metadata.utils import validators

logger = logging.getLogger(__name__)


class DB2FS(WithoutSubfoldersMixin):
    """Base class for loading DB2FS model objects."""

    attribute_used_for_filename: ClassVar[str] = "name"

    id: uuid.UUID
    name: str
    description: str | None = None
    sink_connection_id: uuid.UUID
    source_connection_id: uuid.UUID
    container_name: str
    select_statement: str
    dataset_type_id: uuid.UUID
    source_table_id: uuid.UUID
    datasource_info_id: uuid.UUID
    folder_path: str | None = None
    sequence_column_name: str | None = None

    _check_name_w_replace = field_validator("name")(
        validators.name_alphanumeric_w_replace
    )

    _check_select_statement = field_validator("select_statement")(
        validators.check_if_valid_template
    )

    _check_folder_path = field_validator("folder_path")(
        validators.check_if_valid_template
    )
