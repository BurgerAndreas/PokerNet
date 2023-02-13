import numpy as np
import random as rand

# Instead of passing parameters, we could also pass a game object
class Player():
  """
  Player class.
  Parent (base) class for bot and human players
  n_turn: player's turn in the game
  (0 = first to act, 1 = second to act, etc., n_players-2 = small blind, n_players-1 = big blind)
  """

  def __init__(self, n_turn=0, pocket_cards=np.array([]), sblind=0.5, bblind=1.0):
    # Player's turn in the round
    self.n_turn = n_turn
    # Player's pocket cards
    self.pocket_cards = pocket_cards
    # blinds
    self.sblind = sblind
    self.bblind = bblind
    # money put into pot by player
    if n_turn == 0:
      self.stake = self.sblind
    elif n_turn == 1:
      self.stake = self.bblind
    else:
      self.stake = 0

  # Placeholder method, to be overwritten by child classes
  def do_action(self, stake_to_match):
    """Player's action"""
    # always check
    # stake gets updated in parent class
    return 0



class Bot(Player):
  """Bot which mostly checks"""
  def __init__(self, n_turn=0, pocket_cards=np.array([]), sblind=0.5, bblind=1.0):
    # Get methods and attributes from parent class
    super().__init__(n_turn=n_turn, pocket_cards=pocket_cards, sblind=sblind, bblind=bblind) 
    # Call parent class constructor
    # Player.__init__(self, parent_var1, parent_var2)

  def do_action(self, stake_to_match):
    if self.stake == stake_to_match:
      return 0
    else:
      rand.randint(0,9)
      if rand == 0:
        # fold
        return -1
      elif rand == 9:
        # raise
        return rand.randint(0, 5*self.bblind)
      else:
        # call
        return 0



class Human(Player):
  """Human player"""
  def __init__(self, n_turn=0, pocket_cards=np.array([]), sblind=0.5, bblind=1.0):
    # Get methods and attributes from parent class
    super().__init__(n_turn=n_turn, pocket_cards=pocket_cards, sblind=sblind, bblind=bblind) 

  def do_action(self, stake_to_match):
    print('You have to raise by', stake_to_match - self.stake)
    action = input('What do you want to do? \n(-1 fold, 0 check, 0 call, >0 raise)\n')
    return int(action)