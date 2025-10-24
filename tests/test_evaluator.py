from poker_solver import HandCategory, determine_winners, evaluate_best_hand, parse_cards


def build_cards(*tokens):
    return parse_cards(tokens)


def test_straight_flush_beats_four_of_a_kind():
    straight_flush = build_cards("Ah", "Kh", "Qh", "Jh", "Th")
    four_kind = build_cards("9c", "9d", "9h", "9s", "2d")

    assert evaluate_best_hand(straight_flush).category == HandCategory.STRAIGHT_FLUSH
    assert evaluate_best_hand(four_kind).category == HandCategory.FOUR_OF_A_KIND
    assert evaluate_best_hand(straight_flush) > evaluate_best_hand(four_kind)


def test_full_house_vs_flush():
    cards = build_cards("As", "Ad", "Ac", "Kd", "Kh", "Qh", "2c")
    evaluation = evaluate_best_hand(cards)
    assert evaluation.category == HandCategory.FULL_HOUSE
    assert evaluation.ranks[0] == 14


def test_determine_winners_handles_split_pot():
    board = build_cards("As", "Kd", "Qh", "Jc", "Td")
    hero = build_cards("2c", "3d")
    villain = build_cards("4h", "5s")
    assert determine_winners([hero, villain], board) == [0, 1]


def test_pair_breakers():
    board = build_cards("2c", "7d", "9s", "Jh", "Qd")
    hero = build_cards("As", "Ad")
    villain = build_cards("Ks", "Kd")
    winners = determine_winners([hero, villain], board)
    assert winners == [0]
