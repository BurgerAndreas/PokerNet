import numpy as np
import os

#
pwd_path = os.getcwd()

# Table of all possible pocket cards
# independet of game state
SUITS = ['c', 'd', 'h', 's']
# last is best
# "T": 8, "J": 9, "Q": 10, "K": 11, "A": 12
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
CARDS = []
for suit in SUITS:
  for rank in RANKS:
    CARDS.append(rank + suit)
POCKET_CARDS = np.load(file=pwd_path + '/tables/pocket_cards.npy', allow_pickle=True)