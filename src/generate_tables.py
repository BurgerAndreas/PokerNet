import numpy as np
import os

import global_vars

def generate_pocket_cards():
  """Generates all possible pocket cards"""
  # 52 choose 2 = 1326
  pocket_cards = []
  for i in global_vars.CARDS:
    for j in global_vars.CARDS:
      if i == j:
        continue
      else:
        pocket_cards.append([i, j])
  pocket_cards = np.asarray(pocket_cards)
  return pocket_cards

def save_pocket_cards():
  """Saves all possible pocket cards"""
  pocket_cards = generate_pocket_cards()
  np.save(file=(global_vars.pwd_path + '/tables/pocket_cards'), arr=pocket_cards, allow_pickle=True)
  print('Saved pocket cards to tables/pocket_cards.npy')

# save_pocket_cards()
# np.load(file=(global_vars.pwd_path + '/tables/pocket_cards.npy'))



