"""Lego models."""

from enum import Enum

from humps import camelize
from pydantic import BaseModel, ConfigDict


class ReprEnum(Enum):
    """General enum in the project."""

    def __str__(self) -> str:
        """Return the string representation of the enum."""
        return self.value

    ## Currently is under question
    ## For debugging, the parent method is more useful
    ## In the f-strings, we can use {self.value} instead
    # def __repr__(self) -> str:
    #     return self.value

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Enum):
            try:
                return self.value == other.value
            except AttributeError:
                return False
        return False

    def __hash__(self) -> int:
        return hash(self.value)


class CamelModel(BaseModel):
    """Base model with camel serialization for JavaScript frontend."""

    model_config = ConfigDict(populate_by_name=True, alias_generator=camelize)
