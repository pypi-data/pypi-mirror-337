from __future__ import annotations

import logging
import uuid
from typing import ClassVar

from pydantic import field_validator

from cloe_metadata.base.base import WithoutSubfoldersMixin
from cloe_metadata.utils import validators

logger = logging.getLogger(__name__)


class FS2DB(WithoutSubfoldersMixin):
    """Base class for loading FS2DB model objects."""

    attribute_used_for_filename: ClassVar[str] = "name"

    id: uuid.UUID
    name: str
    description: str | None = None
    sink_connection_id: uuid.UUID
    source_connection_id: uuid.UUID
    container_name: str
    filename_pattern: str
    folder_path_pattern: str
    sink_table_id: uuid.UUID
    dataset_type_id: uuid.UUID
    get_from_filecatalog: bool = False
    post_load_exec_job_id: uuid.UUID | None = None

    _check_filename_pattern = field_validator("filename_pattern")(
        validators.check_if_valid_template
    )

    _check_folder_path_pattern = field_validator("folder_path_pattern")(
        validators.check_if_valid_template
    )
