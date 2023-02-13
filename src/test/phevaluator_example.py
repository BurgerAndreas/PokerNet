from phevaluator import evaluate_cards


# from https://github.com/HenryRLee/PokerHandEvaluator/blob/master/python/phevaluator/card.py
rank_map = {
  "2": 0, "3": 1, "4": 2, "5": 3, "6": 4, "7": 5, "8": 6, "9": 7,
  "T": 8, "J": 9, "Q": 10, "K": 11, "A": 12,
}
suit_map = {
  "C": 0, "D": 1, "H": 2, "S": 3,
  "c": 0, "d": 1, "h": 2, "s": 3
}


# from https://github.com/HenryRLee/PokerHandEvaluator/blob/master/python/examples.py
def phe_example1():
  p1 = evaluate_cards("9c", "4c", "4s", "9d", "4h", "Qc", "6c")
  p2 = evaluate_cards("9c", "4c", "4s", "9d", "4h", "2c", "9h")

  # Player 2 has a stronger hand
  print(f"The rank of the hand in player 1 is {p1}") # 292
  print(f"The rank of the hand in player 2 is {p2}") # 236


def phe_example2():
  # card = mapped_rank * 4 + mapped_suit 
  a = 7 * 4 + 0  # 9c
  b = 2 * 4 + 0  # 4c
  c = 2 * 4 + 3  # 4s
  d = 7 * 4 + 1  # 9d
  e = 2 * 4 + 2  # 4h

  # Player 1
  f = 10 * 4 + 0  # Qc
  g = 4 * 4 + 0  # 6c

  # Player 2
  h = 0 * 4 + 0  # 2c
  i = 7 * 4 + 2  # 9h

  rank1 = evaluate_cards(a, b, c, d, e, f, g)  # expected 292
  rank2 = evaluate_cards(a, b, c, d, e, h, i)  # expected 236

  print(f"The rank of the hand in player 1 is {rank1}")
  print(f"The rank of the hand in player 2 is {rank2}")
  print("Player 2 has a stronger hand")


def card_to_id(card):
  rank, suit = card
  return rank_map[rank] * 4 + suit_map[suit]

def cards_to_ids(cards):
  return [card_to_id(card) for card in cards]

def phe_example3():
  community_cards = ["9c", "4c", "4s", "9d", "4h"]
  player1_cards = ["Qc", "6c"]
  player2_cards = ["2c", "9h"]

  rank1 = evaluate_cards(*cards_to_ids(community_cards), *cards_to_ids(player1_cards))
  rank2 = evaluate_cards(*community_cards, *player2_cards)

  print(f"The rank of the hand in player 1 is {rank1}")
  print(f"The rank of the hand in player 2 is {rank2}")

