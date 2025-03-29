from __future__ import annotations

import json
import logging
import pathlib
from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

import cloe_metadata.utils.writer as writer
from cloe_metadata.base.modeler import power_pipe, simple_pipe
from cloe_metadata.utils import validators

logger = logging.getLogger(__name__)


class Pipes(BaseModel):
    """Base class for loading CLOE Pipe model objects."""

    subfolder_path: ClassVar[pathlib.Path] = pathlib.Path("pipes")

    pipes: list[simple_pipe.SimplePipe | power_pipe.PowerPipe] = Field(default=[])
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=writer.to_lower_camel_case,
    )

    @field_validator("pipes")
    @classmethod
    def child_uniqueness_check(
        cls, value: list[simple_pipe.SimplePipe | power_pipe.PowerPipe]
    ):
        validators.find_non_unique(value, "name")
        return value

    @classmethod
    def read_instances_from_disk(
        cls, input_path: pathlib.Path
    ) -> tuple[Pipes, list[ValidationError | json.JSONDecodeError]]:
        instances: list[simple_pipe.SimplePipe | power_pipe.PowerPipe] = []
        errors = []
        if not input_path.exists():
            raise FileNotFoundError(f"Directory not found: {input_path}")

        instances_path = input_path / cls.subfolder_path
        sub_pipes: list[type[simple_pipe.SimplePipe] | type[power_pipe.PowerPipe]] = [
            simple_pipe.SimplePipe,
            power_pipe.PowerPipe,
        ]
        for sub_pipe in sub_pipes:
            sub_instances, sub_errors = sub_pipe.read_instances_from_disk(
                instances_path / sub_pipe.__name__.lower()
            )
            instances += sub_instances
            errors += sub_errors
        try:
            instance = cls(pipes=instances)
        except ValidationError as e:
            errors.append(e)

        return instance, errors

    def write_to_disk(self, output_path: pathlib.Path) -> None:
        for child in self.pipes:
            child.write_to_disk(
                output_path / self.subfolder_path / child.__class__.__name__.lower()
            )

    def get_power_pipes(
        self,
    ) -> list[power_pipe.PowerPipe]:
        """
        Filters the pipes list based on the given pipe type.
        """
        return [pipe for pipe in self.pipes if isinstance(pipe, power_pipe.PowerPipe)]

    def get_simple_pipes(
        self,
    ) -> list[simple_pipe.SimplePipe]:
        """
        Filters the pipes list based on the given pipe type.
        """
        return [pipe for pipe in self.pipes if isinstance(pipe, simple_pipe.SimplePipe)]
