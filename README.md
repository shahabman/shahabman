## Poker Solver

This repository now includes a simple Texas Hold'em poker solver that can
evaluate player hands and determine the winner for a given board. The solver
exposes both a Python API and a command line interface.

### Command line usage

```bash
python -m poker_solver "As Kd" "Qc Qd" -b "Ah Th 2c"
```

### Python usage

```python
from poker_solver import parse_cards, determine_winners

board = parse_cards("As Kd Qh Jc Td".split())
hands = [
    parse_cards("2c 3d".split()),
    parse_cards("4h 5s".split()),
]
winners = determine_winners(hands, board)
print(winners)
```


