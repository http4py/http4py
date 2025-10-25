from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from io import BytesIO
from typing import BinaryIO


class Body(ABC):
    @property
    @abstractmethod
    def stream(self) -> BinaryIO:
        pass

    @property
    @abstractmethod
    def bytes(self) -> bytes:
        pass

    @property
    @abstractmethod
    def text(self) -> str:
        pass

    @property
    @abstractmethod
    def length(self) -> int | None:
        pass

    def close(self) -> None:
        pass


@dataclass(init=False)
class _MemoryBody(Body):
    _bytes: bytes
    _text: str

    def __init__(self, content: str | bytes):
        if isinstance(content, str):
            self._bytes = content.encode("utf-8")
            self._text = content
        else:
            self._bytes = content
            self._text = content.decode("utf-8")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Body):
            return False
        return self.bytes == other.bytes

    def __hash__(self) -> int:
        return hash(self._bytes)

    @property
    def stream(self) -> BinaryIO:
        return BytesIO(self._bytes)

    @property
    def bytes(self) -> bytes:
        return self._bytes

    @property
    def text(self) -> str:
        return self._text

    @property
    def length(self) -> int | None:
        return len(self._bytes)


@dataclass(init=False)
class _StreamBody(Body):
    _stream: BinaryIO
    _length: int | None
    _cached_bytes: bytes | None

    def __init__(self, stream: BinaryIO, length: int | None = None):
        self._stream = stream
        self._length = length
        self._cached_bytes = None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Body):
            return False
        return self.bytes == other.bytes

    def __hash__(self) -> int:
        return hash(self.bytes)

    @property
    def stream(self) -> BinaryIO:
        return self._stream

    @property
    def bytes(self) -> bytes:
        if self._cached_bytes is None:
            current_pos = self._stream.tell()
            self._stream.seek(0)
            self._cached_bytes = self._stream.read()
            self._stream.seek(current_pos)
        return self._cached_bytes

    @property
    def text(self) -> str:
        return self.bytes.decode("utf-8")

    @property
    def length(self) -> int | None:
        return self._length

    def close(self) -> None:
        if hasattr(self._stream, "close"):
            self._stream.close()
