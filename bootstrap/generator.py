from __future__ import annotations

from abc import ABC, abstractmethod


class GenerationError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class Generator(ABC):
    @property
    @abstractmethod
    def output(self) -> str:
        pass
