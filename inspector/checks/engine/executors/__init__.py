import dataclasses
import typing
from abc import ABCMeta, abstractmethod
from datetime import datetime

from ....systems.models import Instance

if typing.TYPE_CHECKING:
    from ....checks.models import Datacheck


@dataclasses.dataclass
class Result:
    value_type: str
    string_value: str | None = None
    number_value: float | None = None
    date_value: datetime | None = None
    object_value: dict | None = None

    @property
    def value(self):
        match self.value_type:
            case "string":
                return self.string_value
            case "number":
                return self.number_value
            case "date":
                return self.date_value
            case "object":
                return self.object_value
            case _:
                raise ValueError("Invalid value type")

    def __eq__(self, other):
        if self.value_type == other.value_type:
            return self.value == other.value
        raise ValueError("Cannot compare results of different types")

    def __neg__(self, other):
        if self.value_type == other.value_type:
            return self.value != other.value
        raise ValueError("Cannot compare results of different types")

    def __le__(self, other):
        if self.value_type == other.value_type:
            return self.value <= other.value
        raise ValueError("Cannot compare results of different types")

    def __lt__(self, other):
        if self.value_type == other.value_type:
            return self.value < other.value
        raise ValueError("Cannot compare results of different types")

    def __ge__(self, other):
        if self.value_type == other.value_type:
            return self.value >= other.value
        raise ValueError("Cannot compare results of different types")

    def __gt__(self, other):
        if self.value_type == other.value_type:
            return self.value > other.value
        raise ValueError("Cannot compare results of different types")


@dataclasses.dataclass
class ExpectationResult:
    result: bool
    object_value: dict


class CheckExecutor(metaclass=ABCMeta):
    def __init__(self, datacheck: "Datacheck", side: str, instance: Instance | None):
        self.datacheck: "Datacheck" = datacheck
        self.side: str = side
        self.instance: Instance | None = instance

    @abstractmethod
    def execute(self) -> Result | ExpectationResult:
        """Execute the check logic and return the result"""
