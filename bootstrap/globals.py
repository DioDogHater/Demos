from __future__ import annotations

from typing import Self


class CompilerTarget:
    def __init__(self, name : str, triple : tuple[str, str, str], bits : int, pointer_size : int) -> None:
        self.__name : str = name
        self.__triple : tuple[str, str, str] = triple
        self.__bits : int = bits
        self.__pointer_size : int = pointer_size

    @property
    def name(self) -> str:
        return self.__name

    @property
    def triple(self) -> tuple[str, str, str]:
        return self.__triple

    @property
    def bits(self) -> int:
        return self.__bits

    @property
    def pointer_size(self) -> int:
        return self.__pointer_size

class CompilerGlobals:
    __instance : Self | None = None
    is_instanced : bool = False

    def __setup(self, target : CompilerTarget) -> None:
        self.__target : CompilerTarget = target

    def __new__(cls, target : CompilerTarget | None = None) -> Self:
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            if not isinstance(target, CompilerTarget):
                raise ValueError(f"target must be CompilerTarget on first instance, got {type(target)} instead.")
            cls.__instance.__setup(target)
            cls.is_instanced = True
        return cls.__instance

    @property
    def target(self) -> CompilerTarget:
        return self.__target

    @classmethod
    def get_target(cls) -> CompilerTarget:
        if not cls.__instance:
            raise ValueError("CompilerGlobals must be instanced because it can be used.")
        return cls.__instance.target
