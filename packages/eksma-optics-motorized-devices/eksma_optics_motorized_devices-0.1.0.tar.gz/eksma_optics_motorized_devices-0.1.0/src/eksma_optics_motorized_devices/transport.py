import logging
import threading
from abc import ABC, abstractmethod

import serial

logger = logging.getLogger(__name__)


class Transport(ABC):
    @abstractmethod
    def read(self) -> str:
        pass

    @abstractmethod
    def write(self, value: str) -> None:
        pass


class SerialTansport(Transport):
    ENCODING = "utf-8"

    def __init__(self, port: str) -> None:
        super().__init__()

        self._lock = threading.Lock()
        self._connection = serial.Serial(port, timeout=1)

    def read(self) -> str:
        with self._lock:
            value = self._connection.readline()

        decoded_value = value.decode(self.ENCODING)
        logger.debug("read: %s", value, extra={"value": value, "decoded_value": decoded_value})

        return decoded_value

    def write(self, value: str) -> None:
        encoded_value = value.encode(self.ENCODING)

        with self._lock:
            logger.debug("write: %s", encoded_value, extra={"value": value, "encoded_value": encoded_value})
            self._connection.write(encoded_value)
