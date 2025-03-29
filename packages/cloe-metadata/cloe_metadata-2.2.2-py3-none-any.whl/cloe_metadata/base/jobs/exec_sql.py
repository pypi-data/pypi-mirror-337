from __future__ import annotations

import logging
import uuid
from typing import ClassVar

from pydantic import BaseModel, ConfigDict, ValidationError, field_validator

from cloe_metadata.base.base import WithoutSubfoldersMixin
from cloe_metadata.utils import validators, writer

logger = logging.getLogger(__name__)


class Query(BaseModel):
    """Base class for loading query model objects."""

    exec_order: int
    query: str
    description: str | None = None
    model_config = ConfigDict(
        populate_by_name=True, alias_generator=writer.to_lower_camel_case
    )

    _check_query = field_validator("query")(validators.check_if_valid_template)


class ExecSQL(WithoutSubfoldersMixin):
    """Base class for loading ExecSQL model objects."""

    attribute_used_for_filename: ClassVar[str] = "name"

    id: uuid.UUID
    name: str
    description: str | None = None
    connection_id: uuid.UUID
    queries: list[Query]

    @field_validator("queries")
    @classmethod
    def runtimes_order_by_unique_check(cls, value: list[Query]):
        order_number = []
        for query in value:
            if query.exec_order not in order_number:
                order_number.append(query.exec_order)
            else:
                raise ValueError("Queries exec_order not unique")
        return value

    @classmethod
    def json_object_to_class(
        cls, data: dict
    ) -> tuple[ExecSQL | None, list[ValidationError]]:
        errors = []
        queries = []
        for query in data.pop("queries", []):
            try:
                queries.append(Query(**query))
            except ValidationError as e:
                errors.append(e)
        try:
            instance = cls(**data, queries=queries)
        except ValidationError as e:
            instance = None
            errors.append(e)
        return instance, errors
