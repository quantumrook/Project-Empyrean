from enum import Enum
from typing import Any, Self


class EmpyreanEnum(Enum):

    @classmethod
    def list(cls) -> list[Self]:
        """
        Returns all of the types as a list.
        """
        return list(map(lambda c: c, cls))

    @classmethod
    def from_string(cls, str_to_convert: str) -> Self:
        if isinstance(str_to_convert, EmpyreanEnum):
            str_to_convert = str(str_to_convert.value)
        for enum in cls.list():
            if str(enum.value).lower() == str_to_convert.lower():
                return enum
        raise ValueError(f"Tried to convert {str_to_convert=} to {cls=}.")

    @classmethod
    def is_numeric(cls, enum) -> bool:
        if isinstance(enum, int):
            return True
        elif isinstance(enum, float):
            return True
        else:
            return False

    @classmethod
    def max_value(cls) -> Any:
        current_max = None
        for enum in cls.list():
            if EmpyreanEnum.is_numeric(enum):
                if current_max is None:
                    current_max = enum.value
                if enum.value > current_max:
                    current_max = enum.value
        if current_max is not None:
            return current_max
        else:
            return cls.list()[-1].value

    @classmethod
    def min_value(cls) -> Any:
        current_min = None
        for enum in cls.list():
            if EmpyreanEnum.is_numeric(enum):
                if current_min is None:
                    current_min = enum.value
                if enum.value < current_min:
                    current_min = enum.value
        if current_min is not None:
            return current_min
        else:
            return cls.list()[0].value

