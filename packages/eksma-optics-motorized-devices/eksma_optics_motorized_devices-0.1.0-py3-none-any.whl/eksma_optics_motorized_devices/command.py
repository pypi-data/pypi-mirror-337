from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, IntFlag, auto
from types import MappingProxyType
from typing import TYPE_CHECKING, Any

from eksma_optics_motorized_devices.decimal_with_dimension import DecimalWithDimension

if TYPE_CHECKING:
    from collections.abc import Iterable

LINE_ENDING = "\r\n"


class BEXError(Exception):
    ERROR_CODES = MappingProxyType(
        {
            "?m1": "short to ground indicator phase B",
            "?m2": "short to ground indicator phase A",
            "?m3": "open load indicator phase B",
            "?m4": "open load indicator phase A",
            "?m5": "overtemperature flag",
            "?m6": "short to supply indicator phase B",
            "?m7": "short to supply indicator phase A",
            "?p1": "Lens1 position error",
            "?p2": "Lens2 position error",
            "?c1": "first symbol mismatch",
            "?c2": "command not found",
            "?c3": "value mismatch",
            "?c4": "value limit exceed",
            "?c5": "query only",
        },
    )

    def __init__(self, code: str) -> None:
        self.code = code
        message = self.ERROR_CODES.get(code, "unknown error")
        full_message = f"{code}: {message}"

        super().__init__(full_message)


class NoQueryError(Exception):
    def __init__(self) -> None:
        super().__init__("only command form is available")


class QueryOnlyError(Exception):
    def __init__(self) -> None:
        super().__init__("only query form is available")


class FloatInfinityError(ValueError):
    def __init__(self) -> None:
        super().__init__("float infinity is not supported")


class AbstractCommand(ABC):
    no_query = False
    query_only = False
    parent: type[AbstractCommand] | None = None

    @staticmethod
    def parse_command_response(value: str) -> Any:  # noqa: ANN401
        return value

    @staticmethod
    def parse_query_response(value: str) -> Any:  # noqa: ANN401
        return value

    @abstractmethod
    def mnemonic(self) -> str:
        pass  # pragma: no cover

    @abstractmethod
    def command_header(self) -> str:
        pass  # pragma: no cover

    def query_header(self) -> str:
        return f"{self.command_header()}?"

    def command(self, *args: Any) -> str:  # noqa: ANN401
        if self.query_only:
            raise QueryOnlyError

        return self._format(self.command_header(), *args)

    def query(self, *args: Any) -> str:  # noqa: ANN401
        if self.no_query:
            raise NoQueryError

        return self._format(self.query_header(), *args)

    def _format(self, header: str, *args: tuple[Any]) -> str:
        out = header

        if len(args) > 0:
            out += f" {','.join([str(a) for a in args])}"

        out += LINE_ENDING

        return out


class CommonCommand(AbstractCommand):
    def command_header(self) -> str:
        return f"*{self.mnemonic()}"


class InstrumentControlCommand(AbstractCommand):
    def command_header(self) -> str:
        mnemonics = self._fully_qualified_mnemonic()

        return f":{':'.join(mnemonics)}"

    def _fully_qualified_mnemonic(self) -> Iterable[str]:
        parts: list[str] = []
        parent: type[AbstractCommand] | None = self.__class__
        while parent is not None:
            instance = parent()
            parts.append(instance.mnemonic())
            parent = instance.parent

        return reversed(parts)


@dataclass
class IdentificationValue:
    vendor: str
    model: str
    serial_number: str
    version: str
    raw: str

    def description(self) -> str:
        return f"{self.vendor} {self.model} v{self.version} ({self.serial_number})"


class Identification(CommonCommand):
    def __init__(self) -> None:
        self.query_only = True

    @classmethod
    def parse_query_response(cls, value: str) -> IdentificationValue:
        try:
            vendor, model, serial_number, version = value.split(",")
        except ValueError as ex:
            msg = "invalid identification response"
            raise ValueError(msg) from ex

        if (serial_number_match := re.match("^SN(.+)$", serial_number)) is None:
            msg = "invalid serial number"
            raise ValueError(msg)

        serial_number = serial_number_match.group(1)
        version = SystemVersion.parse_query_response(version)

        return IdentificationValue(vendor=vendor, model=model, serial_number=serial_number, version=version, raw=value)

    def mnemonic(self) -> str:
        return "IDN"


class Reset(CommonCommand):
    def __init__(self) -> None:
        self.no_query = True

    def mnemonic(self) -> str:
        return "RST"


class Lens1(InstrumentControlCommand):
    @classmethod
    def parse_query_response(cls, value: str) -> float:
        return float(value)

    def mnemonic(self) -> str:
        return "LENS1"

    def command(self, value: float) -> str:
        return InstrumentControlCommand.command(self, _format_dot_three_f(value))


class Lens2(InstrumentControlCommand):
    @classmethod
    def parse_query_response(cls, value: str) -> float:
        return float(value)

    def mnemonic(self) -> str:
        return "LENS2"

    def command(self, value: float) -> str:
        return InstrumentControlCommand.command(self, _format_dot_three_f(value))


class Lens1Minimum(InstrumentControlCommand):
    parent = Lens1

    def mnemonic(self) -> str:
        return "MIN"

    def command(self, value: float) -> str:
        return InstrumentControlCommand.command(self, _format_dot_three_f(value))


class Lens1Maximum(InstrumentControlCommand):
    parent = Lens1

    def mnemonic(self) -> str:
        return "MAX"

    def command(self, value: float) -> str:
        return InstrumentControlCommand.command(self, _format_dot_three_f(value))


class Lens2Minimum(InstrumentControlCommand):
    parent = Lens2

    def mnemonic(self) -> str:
        return "MIN"

    def command(self, value: float) -> str:
        return InstrumentControlCommand.command(self, _format_dot_three_f(value))


class Lens2Maximum(InstrumentControlCommand):
    parent = Lens2

    def mnemonic(self) -> str:
        return "MAX"

    def command(self, value: float) -> str:
        return InstrumentControlCommand.command(self, _format_dot_three_f(value))


class Configuration(InstrumentControlCommand):
    def mnemonic(self) -> str:
        return "CONF"


class ConfigurationWavelength(InstrumentControlCommand):
    parent = Configuration

    @classmethod
    def parse_query_response(cls, value: str) -> DecimalWithDimension:
        return DecimalWithDimension.from_string(value)

    def mnemonic(self) -> str:
        return "WAVE"

    def command(self, value: int) -> str:
        return InstrumentControlCommand.command(self, _format_zero_four_u(value))


class ConfigurationMagnification(InstrumentControlCommand):
    parent = Configuration

    @classmethod
    def parse_query_response(cls, value: str) -> float:
        return float(value)

    def mnemonic(self) -> str:
        return "MAG"

    def command(self, value: float) -> str:
        return InstrumentControlCommand.command(self, _format_dot_one_f(value))


class ConfigurationCollimation(InstrumentControlCommand):
    parent = Configuration

    @classmethod
    def parse_query_response(cls, value: str) -> int:
        return int(value)

    def mnemonic(self) -> str:
        return "COL"

    def command(self, value: int) -> str:
        return InstrumentControlCommand.command(self, _format_d(value))


class PresetFlags(IntFlag):
    PROTECTED = auto()


@dataclass
class PresetValue:
    id: int
    magnification: float
    collimation: int
    flags: PresetFlags


class Preset(InstrumentControlCommand):
    @staticmethod
    def parse_query_response(value: str) -> list[PresetValue]:
        presets = value.split(";")

        out = []
        for preset in presets:
            if len(preset) == 0:
                break

            preset_id, mag, col, *rest = preset.split(",")
            flags = rest[0] if len(rest) >= 1 else 0

            out.append(
                PresetValue(
                    id=int(preset_id), magnification=float(mag), collimation=int(col), flags=PresetFlags(int(flags))
                )
            )

        return out

    def mnemonic(self) -> str:
        return "PRES"

    def command(self, value: tuple[float, int]) -> str:
        return InstrumentControlCommand.command(self, _format_tuple(value))


class PresetRemaining(InstrumentControlCommand):
    parent = Preset

    def __init__(self) -> None:
        self.query_only = True

    @staticmethod
    def parse_query_response(value: str) -> int:
        return int(value)

    def mnemonic(self) -> str:
        return "REM"

    def command(self) -> str:
        return InstrumentControlCommand.command(self)


class PresetSave(InstrumentControlCommand):
    parent = Preset

    def __init__(self) -> None:
        self.no_query = True

    def mnemonic(self) -> str:
        return "SAVE"

    def command(self) -> str:
        return InstrumentControlCommand.command(self)


class PresetDelete(InstrumentControlCommand):
    parent = Preset

    def __init__(self) -> None:
        self.no_query = True

    def mnemonic(self) -> str:
        return "DEL"

    def command(self, value: int) -> str:
        return InstrumentControlCommand.command(self, str(value))


class System(InstrumentControlCommand):
    def mnemonic(self) -> str:
        return "SYST"


class SystemWavelenghts(InstrumentControlCommand):
    parent = System

    @classmethod
    def parse_query_response(cls, value: str) -> list[DecimalWithDimension]:
        return [DecimalWithDimension.from_string(s) for s in value.split(", ")]

    def mnemonic(self) -> str:
        return "WAVES"


class SystemMagnificationRange(InstrumentControlCommand):
    parent = System

    @classmethod
    def parse_query_response(cls, value: str) -> tuple[float, float]:
        mag_min, mag_max = value.split(",")
        return float(mag_min.rstrip("x")), float(mag_max.rstrip("x"))

    def mnemonic(self) -> str:
        return "MAGR"


class SystemCollimationRange(InstrumentControlCommand):
    parent = System

    @classmethod
    def parse_query_response(cls, value: str) -> tuple[int, int]:
        col_min, col_max = value.split(",")
        return int(col_min), int(col_max)

    def mnemonic(self) -> str:
        return "COLR"


class SystemMinimumSpace(InstrumentControlCommand):
    parent = System

    @classmethod
    def parse_query_response(cls, value: str) -> DecimalWithDimension:
        return DecimalWithDimension.from_string(value)

    def mnemonic(self) -> str:
        return "MINS"


class SystemStatusValue(str, Enum):
    IDLE = "Idle"
    MOVING = "Moving"
    INITIALIZING = "initializing"
    ERROR = "Error"
    FATAL_ERROR = "Fatal Error"


class SystemStatus(InstrumentControlCommand):
    parent = System

    @classmethod
    def parse_query_response(cls, value: str) -> SystemStatusValue:
        return SystemStatusValue(value)

    def mnemonic(self) -> str:
        return "STAT"


class SystemErr(InstrumentControlCommand):
    parent = System

    NO_ERROR = "No Error"

    @classmethod
    def parse_query_response(cls, value: str) -> str | BEXError:
        if value == cls.NO_ERROR:
            return value

        return BEXError(value)

    def mnemonic(self) -> str:
        return "ERR"


class SystemVersion(InstrumentControlCommand):
    parent = System

    @classmethod
    def parse_query_response(cls, value: str) -> str:
        if (match := re.match("^v(.+)$", value)) is None:
            msg = "invalid version"
            raise ValueError(msg)

        return match.group(1)

    def __init__(self) -> None:
        self.query_only = True

    def mnemonic(self) -> str:
        return "VERS"


class SystemFlagsValue(IntFlag):
    STATE_CHANGED = auto()


class SystemFlags(InstrumentControlCommand):
    @classmethod
    def parse_query_response(cls, value: str) -> SystemFlagsValue:
        return SystemFlagsValue(int(value))

    def __init__(self) -> None:
        self.query_only = True

    def mnemonic(self) -> str:
        return "DISP"


def _assert_float_finite(value: float) -> None:
    if value == float("+inf") or value == float("-inf"):
        raise FloatInfinityError


def _format_dot_three_f(value: float) -> str:
    value = float(value)
    _assert_float_finite(value)

    return f"{value:.3f}"


def _format_dot_one_f(value: float) -> str:
    value = float(value)
    _assert_float_finite(value)

    return f"{value:.1f}"


def _format_zero_four_u(value: int) -> str:
    return f"{int(value):04}"


def _format_d(value: int) -> str:
    return f"{int(value):d}"


def _format_tuple(value: tuple) -> str:
    return ",".join(str(v) for v in value)
