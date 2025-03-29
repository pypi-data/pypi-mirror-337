from __future__ import annotations

import logging
import uuid
from typing import ClassVar

from pydantic import Field, ValidationError, field_validator

from cloe_metadata.base.base import WithoutSubfoldersMixin
from cloe_metadata.base.modeler.simple_pipe import table_mapping
from cloe_metadata.utils import validators

logger = logging.getLogger(__name__)


class SimplePipe(WithoutSubfoldersMixin):
    """SimplePipe metadata model base class"""

    attribute_used_for_filename: ClassVar[str] = "name"

    name: str
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    sql_pipe_template: str
    table_mappings: list[table_mapping.TableMapping]
    job_id: uuid.UUID | None = None

    _check_name_w_replace = field_validator("name")(
        validators.name_alphanumeric_w_replace
    )

    _check_sql_pipe_template = field_validator("sql_pipe_template")(
        validators.check_if_valid_template
    )

    @field_validator("table_mappings")
    @classmethod
    def min_number_table_mappings(cls, value):
        if len(value) < 1:
            raise ValueError("at least one table mapping needs to be set.")
        return value

    @classmethod
    def json_object_to_class(
        cls, data: dict
    ) -> tuple[SimplePipe | None, list[ValidationError]]:
        errors = []
        table_mappings = []
        for tm in data.pop("tableMappings", []):
            try:
                table_mappings.append(table_mapping.TableMapping(**tm))
            except ValidationError as e:
                errors.append(e)
        try:
            instance = cls(**data, table_mappings=table_mappings)
        except ValidationError as e:
            instance = None
            errors.append(e)
        return instance, errors
