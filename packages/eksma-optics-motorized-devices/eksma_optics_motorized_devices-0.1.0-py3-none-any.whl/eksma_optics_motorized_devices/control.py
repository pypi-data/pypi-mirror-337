from __future__ import annotations

import logging
import threading
import time
from contextlib import contextmanager
from typing import TYPE_CHECKING, Generator

from eksma_optics_motorized_devices.command import (
    LINE_ENDING,
    BEXError,
    ConfigurationCollimation,
    ConfigurationMagnification,
    ConfigurationWavelength,
    DecimalWithDimension,
    Identification,
    IdentificationValue,
    Lens1,
    Lens1Maximum,
    Lens1Minimum,
    Lens2,
    Lens2Maximum,
    Lens2Minimum,
    Preset,
    PresetDelete,
    PresetRemaining,
    PresetSave,
    PresetValue,
    Reset,
    SystemCollimationRange,
    SystemErr,
    SystemFlags,
    SystemFlagsValue,
    SystemMagnificationRange,
    SystemMinimumSpace,
    SystemStatus,
    SystemStatusValue,
    SystemVersion,
    SystemWavelenghts,
)

if TYPE_CHECKING:
    from eksma_optics_motorized_devices.transport import Transport

logger = logging.getLogger(__name__)


def _strip_nl(value: str) -> str:
    return value.rstrip(LINE_ENDING)


class DeviceTimeoutError(Exception):
    pass


class Control:
    STATUS_OK = "OK"
    TIMEOUT = 5

    @classmethod
    def _expect_ok(cls, value: str) -> None:
        if value != cls.STATUS_OK:
            raise BEXError(value)

    @contextmanager
    def _wait_for_status_idle(self) -> Generator[None, None, None]:
        try:
            yield
        finally:
            start_time = time.time()
            while True:
                current_time = time.time()
                status = self.get_status_unsafe()

                if status == SystemStatusValue.IDLE:
                    break

                if (current_time - start_time) >= self.TIMEOUT:
                    raise DeviceTimeoutError

    def __init__(self, transport: Transport) -> None:
        self._transport = transport

        self._lock = threading.Lock()

    def is_busy(self) -> bool:
        return self._lock.locked()

    def get_identification(self) -> IdentificationValue:
        with self._lock:
            self._transport.write(Identification().query())
            response = _strip_nl(self._transport.read())

        return Identification.parse_query_response(response)

    def reset(self) -> None:
        with self._lock:
            self._transport.write(Reset().command())
            response = _strip_nl(self._transport.read())

        self._expect_ok(response)

    def get_lens1(self) -> float:
        with self._lock:
            self._transport.write(Lens1().query())
            response = _strip_nl(self._transport.read())

        return Lens1.parse_query_response(response)

    def set_lens1_unsafe(self, value: float) -> None:
        self._transport.write(Lens1().command(value))
        response = _strip_nl(self._transport.read())

        self._expect_ok(response)

    def set_lens1(self, value: float) -> None:
        with self._lock, self._wait_for_status_idle():
            self.set_lens1_unsafe(value)

    def get_lens2(self) -> float:
        with self._lock:
            self._transport.write(Lens2().query())
            response = _strip_nl(self._transport.read())

        return Lens2.parse_query_response(response)

    def set_lens2_unsafe(self, value: float) -> None:
        self._transport.write(Lens2().command(value))
        response = _strip_nl(self._transport.read())

        self._expect_ok(response)

    def set_lens2(self, value: float) -> None:
        with self._lock, self._wait_for_status_idle():
            self.set_lens2_unsafe(value)

    def get_lens1_minimum(self) -> float:
        with self._lock:
            self._transport.write(Lens1Minimum().query())
            response = _strip_nl(self._transport.read())

        return Lens1Minimum.parse_query_response(response)

    def get_lens1_maximum(self) -> float:
        with self._lock:
            self._transport.write(Lens1Maximum().query())
            response = _strip_nl(self._transport.read())

        return Lens1Maximum.parse_query_response(response)

    def get_lens2_minimum(self) -> float:
        with self._lock:
            self._transport.write(Lens2Minimum().query())
            response = _strip_nl(self._transport.read())

        return Lens2Minimum.parse_query_response(response)

    def get_lens2_maximum(self) -> float:
        with self._lock:
            self._transport.write(Lens2Maximum().query())
            response = _strip_nl(self._transport.read())

        return Lens2Maximum.parse_query_response(response)

    def get_wavelength(self) -> DecimalWithDimension:
        with self._lock:
            self._transport.write(ConfigurationWavelength().query())
            response = _strip_nl(self._transport.read())

        return ConfigurationWavelength.parse_query_response(response)

    def set_wavelength(self, value: int) -> None:
        with self._lock:
            self._transport.write(ConfigurationWavelength().command(value))
            response = _strip_nl(self._transport.read())

        self._expect_ok(response)

    def get_magnification(self) -> float:
        with self._lock:
            self._transport.write(ConfigurationMagnification().query())
            response = _strip_nl(self._transport.read())

        return ConfigurationMagnification.parse_query_response(response)

    def set_magnification_unsafe(self, value: float) -> None:
        self._transport.write(ConfigurationMagnification().command(value))
        response = _strip_nl(self._transport.read())

        self._expect_ok(response)

    def set_magnification(self, value: float) -> None:
        with self._lock, self._wait_for_status_idle():
            self.set_magnification_unsafe(value)

    def get_collimation(self) -> int:
        with self._lock:
            self._transport.write(ConfigurationCollimation().query())
            response = _strip_nl(self._transport.read())

        return ConfigurationCollimation.parse_query_response(response)

    def set_collimation_unsafe(self, value: int) -> None:
        self._transport.write(ConfigurationCollimation().command(value))
        response = _strip_nl(self._transport.read())

        self._expect_ok(response)

    def set_collimation(self, value: int) -> None:
        with self._lock, self._wait_for_status_idle():
            self.set_collimation_unsafe(value)

    def get_presets(self) -> list[PresetValue]:
        with self._lock:
            self._transport.write(Preset().query())
            response = _strip_nl(self._transport.read())

        return Preset.parse_query_response(response)

    def save_preset(self) -> None:
        with self._lock:
            self._transport.write(PresetSave().command())
            response = _strip_nl(self._transport.read())

        self._expect_ok(response)

    def get_remaining_presets(self) -> int:
        with self._lock:
            self._transport.write(PresetRemaining().query())
            response = _strip_nl(self._transport.read())

        return PresetRemaining.parse_query_response(response)

    def delete_preset(self, value: int) -> None:
        with self._lock:
            self._transport.write(PresetDelete().command(value))
            response = _strip_nl(self._transport.read())

        self._expect_ok(response)

    def get_wavelengths(self) -> list[DecimalWithDimension]:
        with self._lock:
            self._transport.write(SystemWavelenghts().query())
            response = _strip_nl(self._transport.read())

        return SystemWavelenghts.parse_query_response(response)

    def get_magnification_range(self) -> tuple[float, float]:
        with self._lock:
            self._transport.write(SystemMagnificationRange().query())
            response = _strip_nl(self._transport.read())

        return SystemMagnificationRange.parse_query_response(response)

    def get_collimation_range(self) -> tuple[int, int]:
        with self._lock:
            self._transport.write(SystemCollimationRange().query())
            response = _strip_nl(self._transport.read())

        return SystemCollimationRange.parse_query_response(response)

    def get_minimal_lens_space(self) -> DecimalWithDimension:
        with self._lock:
            self._transport.write(SystemMinimumSpace().query())
            response = _strip_nl(self._transport.read())

        return SystemMinimumSpace.parse_query_response(response)

    def get_status_unsafe(self) -> str:
        self._transport.write(SystemStatus().query())
        response = _strip_nl(self._transport.read())

        return SystemStatus.parse_query_response(response)

    def get_status(self) -> str:
        with self._lock:
            return self.get_status_unsafe()

    def get_error(self) -> str | BEXError:
        with self._lock:
            self._transport.write(SystemErr().query())
            response = _strip_nl(self._transport.read())

        return SystemErr.parse_query_response(response)

    def get_version(self) -> str:
        with self._lock:
            self._transport.write(SystemVersion().query())
            response = _strip_nl(self._transport.read())

        return SystemVersion.parse_query_response(response)

    def get_flags(self) -> SystemFlagsValue:
        with self._lock:
            self._transport.write(SystemFlags().query())
            response = _strip_nl(self._transport.read())

        return SystemFlags.parse_query_response(response)
