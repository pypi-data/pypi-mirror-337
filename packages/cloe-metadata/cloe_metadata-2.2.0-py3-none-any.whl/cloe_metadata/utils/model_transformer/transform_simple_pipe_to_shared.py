import uuid

from pydantic import ValidationError

from cloe_metadata import base
from cloe_metadata.base.modeler.simple_pipe import table_mapping
from cloe_metadata.shared.modeler import simple_pipe


def transform_simple_pipe_table_mappings_to_shared(
    base_obj_collection: list[table_mapping.TableMapping],
    databases: base.Databases,
) -> tuple[list[simple_pipe.TableMapping], list[ValidationError]]:
    errors: list[ValidationError] = []
    shared_obj_collection = []
    for base_obj in base_obj_collection:
        try:
            shared_obj = simple_pipe.TableMapping(
                base_obj=base_obj, databases=databases
            )
            shared_obj_collection.append(shared_obj)
        except ValidationError as err:
            errors.append(err)
    return shared_obj_collection, errors


def transform_simple_pipes_to_shared(
    base_obj_collection: base.Pipes,
    databases: base.Databases,
) -> tuple[list[simple_pipe.SimplePipe], dict[uuid.UUID, list[ValidationError]]]:
    errors: dict[uuid.UUID, list[ValidationError]] = {}
    shared_obj_collection = []
    for base_obj in base_obj_collection.get_simple_pipes():
        pipe_error = []
        try:
            (
                shared_table_mappings,
                shared_tm_errors,
            ) = transform_simple_pipe_table_mappings_to_shared(
                base_obj_collection=base_obj.table_mappings,
                databases=databases,
            )
            pipe_error += shared_tm_errors
            shared_obj = simple_pipe.SimplePipe(
                base_obj=base_obj,
                shared_table_mappings=shared_table_mappings,
            )
            shared_obj_collection.append(shared_obj)
        except ValidationError as err:
            pipe_error.append(err)
            errors[base_obj.id] = pipe_error
    return shared_obj_collection, errors
