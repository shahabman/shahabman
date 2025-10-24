"""Card parsing helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

_RANK_CHARS = "23456789TJQKA"
_SUIT_CHARS = "cdhs"  # clubs, diamonds, hearts, spades

_RANK_TO_VALUE = {char: idx + 2 for idx, char in enumerate(_RANK_CHARS)}
_VALUE_TO_RANK = {value: char for char, value in _RANK_TO_VALUE.items()}


@dataclass(frozen=True)
class Card:
    """Represents a standard 52-card deck card."""

    rank: int
    suit: str

    def __post_init__(self) -> None:
        if self.rank not in _VALUE_TO_RANK:
            raise ValueError(f"Invalid rank value: {self.rank}")
        if self.suit not in _SUIT_CHARS:
            raise ValueError(f"Invalid suit: {self.suit}")

    @property
    def rank_char(self) -> str:
        """Return the single-character representation of the rank."""

        return _VALUE_TO_RANK[self.rank]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.rank_char}{self.suit}"


def parse_card(token: str) -> Card:
    """Parse a single card from a two-character token."""

    token = token.strip().lower()
    if len(token) != 2:
        raise ValueError(f"Invalid card token: {token!r}")
    rank_char, suit_char = token[0].upper(), token[1]
    if rank_char not in _RANK_TO_VALUE:
        raise ValueError(f"Unknown rank: {rank_char}")
    if suit_char not in _SUIT_CHARS:
        raise ValueError(f"Unknown suit: {suit_char}")
    return Card(rank=_RANK_TO_VALUE[rank_char], suit=suit_char)


def parse_cards(text: Iterable[str]) -> List[Card]:
    """Parse multiple cards from an iterable of tokens or a string."""

    if isinstance(text, str):
        tokens = text.split()
    else:
        tokens = list(text)
    return [parse_card(token) for token in tokens]
