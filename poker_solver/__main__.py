"""Command line interface for the poker solver."""

from __future__ import annotations

import argparse
from typing import List

from .cards import parse_cards
from .evaluator import determine_winners


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evaluate Texas Hold'em hands")
    parser.add_argument(
        "hands",
        metavar="HAND",
        type=str,
        nargs="+",
        help="Player hands as space-separated card tokens (e.g. 'AsKd')",
    )
    parser.add_argument(
        "-b",
        "--board",
        type=str,
        default="",
        help="Board cards as space-separated tokens",
    )
    return parser


def main(argv: List[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    if len(args.hands) < 1:
        parser.error("At least one player hand must be provided")

    player_hands = [parse_cards(hand.split()) for hand in args.hands]
    for hand in player_hands:
        if len(hand) != 2:
            parser.error("Each player hand must contain exactly two cards")

    board_cards = parse_cards(args.board.split()) if args.board else []
    if board_cards and len(board_cards) not in {3, 4, 5}:
        parser.error("Board must contain 3, 4, or 5 cards")

    winners = determine_winners(player_hands, board_cards)
    winner_text = ", ".join(str(index + 1) for index in winners)
    print(f"Winning player(s): {winner_text}")


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
