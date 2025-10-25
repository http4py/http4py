from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class Http4pyServer(ABC):
    @abstractmethod
    def start(self) -> Http4pyServer:
        pass

    @abstractmethod
    def stop(self) -> Http4pyServer:
        pass

    @abstractmethod
    def block(self) -> None:
        pass

    @abstractmethod
    def port(self) -> int:
        pass
