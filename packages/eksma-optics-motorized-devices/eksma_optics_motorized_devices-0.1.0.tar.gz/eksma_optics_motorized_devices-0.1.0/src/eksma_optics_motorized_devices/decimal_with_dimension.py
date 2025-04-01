from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class DecimalWithDimension:
    value: int
    dimension: str

    def __int__(self) -> int:
        return int(self.value)

    def __float__(self) -> float:
        return float(self.value)

    def __str__(self) -> str:
        return f"{self.value}{self.dimension}"

    @staticmethod
    def from_string(value: str) -> DecimalWithDimension:
        match = re.search(r"^(\d+)(\D\w+)$", value)
        if not match:
            msg = f"invalid format: {value}"
            raise ValueError(msg)

        numeric_value, dimension = match.groups()

        return DecimalWithDimension(int(numeric_value), dimension)
