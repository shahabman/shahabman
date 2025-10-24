"""Poker hand evaluation utilities."""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from itertools import combinations
from typing import Iterable, List, Sequence, Tuple

from .cards import Card


class HandCategory(IntEnum):
    """Ordered hand categories for poker hands."""

    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    FOUR_OF_A_KIND = 7
    STRAIGHT_FLUSH = 8


@dataclass(frozen=True)
class HandEvaluation:
    """Result of evaluating a 5-card poker hand."""

    category: HandCategory
    ranks: Tuple[int, ...]
    cards: Tuple[Card, ...]

    def compare_key(self) -> Tuple[int, ...]:
        """Return a tuple suitable for comparisons."""

        return (int(self.category),) + self.ranks

    def __lt__(self, other: "HandEvaluation") -> bool:
        return self.compare_key() < other.compare_key()

    def __le__(self, other: "HandEvaluation") -> bool:
        return self.compare_key() <= other.compare_key()

    def __gt__(self, other: "HandEvaluation") -> bool:
        return self.compare_key() > other.compare_key()

    def __ge__(self, other: "HandEvaluation") -> bool:
        return self.compare_key() >= other.compare_key()


def _is_straight(ranks: Sequence[int]) -> Tuple[bool, int]:
    """Return whether the given sorted ranks form a straight."""

    unique = sorted(set(ranks), reverse=True)
    if len(unique) != 5:
        return False, 0

    # Handle wheel straight (A-2-3-4-5)
    if unique == [14, 5, 4, 3, 2]:
        return True, 5

    high = unique[0]
    if all(unique[i] - 1 == unique[i + 1] for i in range(4)):
        return True, high
    return False, 0


def _evaluate_five(cards: Sequence[Card]) -> HandEvaluation:
    """Evaluate a 5-card poker hand."""

    ranks = sorted((card.rank for card in cards), reverse=True)
    rank_counts: dict[int, int] = {}
    for rank in ranks:
        rank_counts[rank] = rank_counts.get(rank, 0) + 1

    suits = [card.suit for card in cards]
    is_flush = len(set(suits)) == 1

    is_straight, straight_high = _is_straight(ranks)

    if is_straight and is_flush:
        category = HandCategory.STRAIGHT_FLUSH
        kickers = (straight_high,)
    else:
        # Count ranks for groups (pairs, trips, quads)
        groups = sorted(
            ((count, rank) for rank, count in rank_counts.items()),
            key=lambda item: (item[0], item[1]),
            reverse=True,
        )
        counts = [count for count, _ in groups]
        ordered_ranks = [rank for _, rank in groups]

        if counts[0] == 4:
            category = HandCategory.FOUR_OF_A_KIND
            kicker = max(rank for rank in ranks if rank != ordered_ranks[0])
            kickers = (ordered_ranks[0], kicker)
        elif counts[0] == 3 and counts[1] == 2:
            category = HandCategory.FULL_HOUSE
            kickers = (ordered_ranks[0], ordered_ranks[1])
        elif is_flush:
            category = HandCategory.FLUSH
            kickers = tuple(ranks)
        elif is_straight:
            category = HandCategory.STRAIGHT
            kickers = (straight_high,)
        elif counts[0] == 3:
            category = HandCategory.THREE_OF_A_KIND
            kickers = (ordered_ranks[0],) + tuple(
                rank for rank in ranks if rank != ordered_ranks[0]
            )
        elif counts[0] == 2 and counts[1] == 2:
            category = HandCategory.TWO_PAIR
            high_pair, low_pair = sorted(ordered_ranks[:2], reverse=True)
            kicker = max(rank for rank in ranks if rank not in (high_pair, low_pair))
            kickers = (high_pair, low_pair, kicker)
        elif counts[0] == 2:
            category = HandCategory.ONE_PAIR
            pair_rank = ordered_ranks[0]
            kickers = (pair_rank,) + tuple(
                rank for rank in ranks if rank != pair_rank
            )
        else:
            category = HandCategory.HIGH_CARD
            kickers = tuple(ranks)

    return HandEvaluation(category=category, ranks=kickers, cards=tuple(cards))


def evaluate_best_hand(cards: Iterable[Card]) -> HandEvaluation:
    """Return the best 5-card hand from the given cards."""

    card_list = list(cards)
    if len(card_list) < 5:
        raise ValueError("At least five cards are required for evaluation")

    best: HandEvaluation | None = None
    for combo in combinations(card_list, 5):
        evaluation = _evaluate_five(combo)
        if best is None or evaluation > best:
            best = evaluation
    if best is None:
        raise RuntimeError("No hand combinations were evaluated")
    return best


def determine_winners(hands: Sequence[Sequence[Card]], board: Sequence[Card] | None = None) -> List[int]:
    """Determine winning hand indices for the given players and board."""

    board_cards: Tuple[Card, ...] = tuple(board or [])
    evaluations: List[HandEvaluation] = []
    for hand in hands:
        cards = list(hand) + list(board_cards)
        evaluations.append(evaluate_best_hand(cards))

    best = max(evaluations)
    return [idx for idx, evaluation in enumerate(evaluations) if evaluation == best]
