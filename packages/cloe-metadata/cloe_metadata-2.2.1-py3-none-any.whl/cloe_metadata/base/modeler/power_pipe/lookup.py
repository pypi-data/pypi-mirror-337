import logging
import uuid

from pydantic import BaseModel, ConfigDict, ValidationInfo, field_validator

import cloe_metadata.utils.writer as writer
from cloe_metadata.utils import validators

logger = logging.getLogger(__name__)


class LookupParameter(BaseModel):
    """PowerPipe LookupParameter metadata model base class"""

    source_column_name: str
    calculation: str | None = None
    order_by: int
    model_config = ConfigDict(
        populate_by_name=True, alias_generator=writer.to_lower_camel_case
    )


class ReturnColumnMapping(BaseModel):
    """PowerPipe ReturnColumnMapping metadata model base class"""

    sink_table_id: uuid.UUID
    on_null_value: str
    return_column_name: str
    sink_column_name: str
    is_insert: bool = True
    is_update: bool = True
    is_logging_on_lookup_error: bool = False
    model_config = ConfigDict(
        populate_by_name=True, alias_generator=writer.to_lower_camel_case
    )


class Lookup(BaseModel):
    """PowerPipe Lookup metadata model base class"""

    name: str
    lookup_parameters: list[LookupParameter]
    lookup_table_id: uuid.UUID
    is_add_tenant_to_lookup_parameter: bool = False
    sink_lookup_bk_column_name: str | None = None
    lookup_column_name: str | None = None
    lookup_valid_parameter_column_name: str | None = None
    lookup_valid_from_column_name: str | None = None
    lookup_valid_to_column_name: str | None = None
    return_column_mappings: list[ReturnColumnMapping]

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=writer.to_lower_camel_case
    )

    _check_name_w_replace = field_validator("name")(
        validators.name_alphanumeric_w_replace
    )

    @field_validator("lookup_parameters")
    @classmethod
    def lookup_parameters_order_by_unique_check(cls, value: list[LookupParameter]):
        order_number = []
        for lp in value:
            if lp.order_by not in order_number:
                order_number.append(lp.order_by)
            else:
                raise ValueError("order_by not unique")
        return value

    @field_validator("lookup_column_name")
    @classmethod
    def lookup_parameters_if_column_name(cls, value, info: ValidationInfo):
        if len(info.data.get("lookup_parameters", [])) > 0:
            return value
        else:
            raise ValueError("lookup column name set but no lookup parameters defined.")
