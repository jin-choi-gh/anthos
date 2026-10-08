from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True, order=True)
class Position:
    line: int
    offset: int


# TODO: Write doc strings
# rule: A span never starts at the end of a line,
# and never ends at the start of a line.
#
# spans can be understood as half-open intervals of the form [pos_a, pos_b)
@dataclass(frozen=True)
class Span:
    start: Position
    end: Position

    def is_point(self) -> bool:
        return self.start == self.end

    def contains(self, other: Span) -> bool:
        return self.start <= other.start and other.end <= self.end

    def overlaps(self, other: Span) -> bool:
        return self.start < other.end and other.start < self.end


@dataclass(frozen=True)
class Line:
    id: str
    text: str


@dataclass(frozen=True)
class Substrate:
    lines: tuple[Line, ...]


@dataclass(frozen=True)
class UnitDescription:
    rank: Rank
    content: tuple[str | UnitDescription, ...] = ()
    value: str | None = None
    local_id: str | None = None


@dataclass(frozen=True)
class Rank:
    name: str
    parents: frozenset[str]
    values: frozenset[str] | None
    is_point: bool


@dataclass(frozen=True)
class Representation:
    path: Path
    format: Format
    source: str
    name: str


class Format:
    name: str
    suffix: str
    ranks: dict[str, Rank]
    can_be_base: bool

    def read(self, representation: Representation) -> tuple[UnitDescription, ...]:
        raise NotImplementedError

    def transcribe(self, descriptions: tuple[UnitDescription, ...]) -> Substrate:
        raise NotImplementedError


class SynthesisError(Exception):
    """Something went wrong in the process of synthesising the textual complex"""
