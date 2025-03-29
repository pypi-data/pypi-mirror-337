from pydantic import BaseModel, ConfigDict

from cloe_metadata.utils import writer


class Column(BaseModel):
    """Base class for loading Column model objects."""

    comment: str | None = None
    constraints: str | None = None
    data_type: str
    data_type_length: int | None = None
    data_type_numeric_scale: int | None = None
    data_type_precision: int | None = None
    is_key: bool | None = None
    is_nullable: bool | None = None
    labels: str | None = None
    name: str
    ordinal_position: int | None = None
    model_config = ConfigDict(
        populate_by_name=True, alias_generator=writer.to_lower_camel_case
    )
