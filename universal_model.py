from dataclasses import dataclass, field
from typing import List

@dataclass
class Channel:
    number: int
    name: str

@dataclass
class Bus:
    number: int
    name: str

@dataclass
class FX:
    number: int
    name: str

@dataclass
class ShowFile:
    console_type: str
    session_name: str

    channels: List[Channel] = field(default_factory=list)
    buses: List[Bus] = field(default_factory=list)
    fx: List[FX] = field(default_factory=list)