import logging

from pydantic import BaseModel

from cloe_metadata import base
from cloe_metadata.shared.modeler.simple_pipe import table_mapping

logger = logging.getLogger(__name__)


class SimplePipe(BaseModel):
    """Class for advanced or shared SimplePipe functionality."""

    base_obj: base.SimplePipe
    shared_table_mappings: list[table_mapping.TableMapping]
