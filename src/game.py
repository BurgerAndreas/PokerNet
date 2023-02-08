import numpy as np
import random as rand
from phevaluator import evaluate_cards

import global_vars

def random_pocket_cards(_dealt_cards=np.array([])):
  """Generates two random pocket cards"""
  remaining_deck_cards = np.setdiff1d(global_vars.CARDS, _dealt_cards, assume_unique=True)
  return np.random.choice(remaining_deck_cards, size=2, replace=False)

def random_board_cards(_dealt_cards=np.array([])):
  """Generates five random board cards"""
  remaining_deck_cards = np.setdiff1d(global_vars.CARDS, _dealt_cards, assume_unique=True)
  return np.random.choice(remaining_deck_cards, size=5, replace=False)

def random_flop_cards(_dealt_cards=np.array([])):
  """Generates three random flop cards"""
  remaining_deck_cards = np.setdiff1d(global_vars.CARDS, _dealt_cards, assume_unique=True)
  return np.random.choice(remaining_deck_cards, size=3, replace=False)

def random_turn_card(_dealt_cards=np.array([])):
  """Generates one random turn card"""
  remaining_deck_cards = np.setdiff1d(global_vars.CARDS, _dealt_cards, assume_unique=True)
  return np.random.choice(remaining_deck_cards, size=1, replace=False)

def random_river_card(_dealt_cards=np.array([])):
  """Generates one random river card"""
  remaining_deck_cards = np.setdiff1d(global_vars.CARDS, _dealt_cards, assume_unique=True)
  return np.random.choice(remaining_deck_cards, size=1, replace=False)


stage_names = ["pre-flop", "flop", "turn", "river", "reveal"]

class Game():
  """
  One Game = one hand.
  dCards dealt to players and on the board.
  Parent (base) class for players
  """
  def __init__(
    self, 
    n_players=3, 
    human_players=[0], 
    sblind=0.5, 
    bblind=1.0, 
    open_cards=False
  ):
    # Game parameters
    self.n_players = n_players
    self.human_players = human_players
    self.sblind = sblind
    self.bblind = bblind
    self.stake_to_match = bblind
    self.open_cards = open_cards

    # initialize
    self.pot = sblind + bblind
    self.players = []
    self.folded_players = np.asarray([False] * 5)
    self.dealt_cards = np.array([])
    self.board_cards = np.array([])

    # Game stage
    # 0 = pre-flop, 1 = flop, 2 = turn, 3 = river
    self.stage = 0

    # Deal cards
    self.init_players()

  def init_players(self):
    """Deal the cards and initialize players"""
    for i_player in range(self.n_players):
      # initialize players
      if i_player in self.human_players:
        self.players.append(
          Human(n_turn=i_player, pocket_cards=np.array([]), sblind=self.sblind, bblind=self.bblind)
        )
      else:
        self.players.append(
          Bot(n_turn=i_player, pocket_cards=np.array([]), sblind=self.sblind, bblind=self.bblind)
        )
      # deal cards to players
      self.players[i_player].pocket_cards = random_pocket_cards(self.dealt_cards)
      self.dealt_cards = np.append(self.dealt_cards, self.players[i_player].pocket_cards)

    # Flop, turn, river
    self.board_cards = random_board_cards(self.dealt_cards)
    self.dealt_cards = np.append(self.dealt_cards, self.board_cards)

    # set small and big blind
    self.players[-2].stake = self.sblind
    self.players[-1].stake = self.bblind
    return

  
  def get_player_action(self, player):
    """
    Get one players action.
    Update player stake and pot.
    """
    # raise_by = -1 for fold, 0 for call and check, >0 for raise
    # action = 'fold', 'check', 'call', 'raise' (is superfluous)
    action = player.do_action(self.stake_to_match)
    # update player stake and pot
    if action == -1:
      self.folded_players[player.n_turn] = True
      print('Player {} folded'.format(player.n_turn))
    elif action == 0:
      # check, call
      # add money to pot
      self.pot += self.stake_to_match - player.stake
      # update player stake
      player.stake = self.stake_to_match
      print('Player {} checked/called an additional {}'.format(player.n_turn, self.stake_to_match - player.stake))
    elif action > 0:
      # raise
      self.stake_to_match += action
      self.pot += self.stake_to_match - player.stake
      player.stake = self.stake_to_match
      print('Player {} raised by {}'.format(player.n_turn, action))
    else:
      raise ValueError('Invalid action')
    return
    
  def round(self):
    """
    Get all players actions.
    stage: 0 = pre-flop, 1 = flop, 2 = turn, 3 = river, 4 = reveal.
    stake_to_match: money a player has to match to stay in the round.
    """
    continue_round = True
    while continue_round:
      """
      Raising works like this:
      All players have to match the stake_to_match.
      There is at least one round where all players match the stake_to_match.
      Starts with player 0 (player after big blind)
      If player 0 raises, then player 1 has to call or raise.
      If every player did an action, and player 2 didn't raise, then the round is over.
      """
      for i_player in range(self.n_players):
        # ask player for action
        if not self.folded_players[self.players[i_player].n_turn]:
          self.get_player_action(self.players[i_player])
          continue

      # check if round is over
      first_not_folded_player = np.where(self.folded_players == False)[0][0]
      if self.players[first_not_folded_player].stake == self.stake_to_match:
        continue_round = False
        break

    return
    

  def print_game_state(self):
    print('Stage:', stage_names[self.stage])
    if self.open_cards:
      print('All players cards:', [self.players[i_player].pocket_cards for i_player in range(self.n_players)])
    else:
      for i_player in self.human_players:
        print('Player', i_player, 'cards:', self.players[i_player].pocket_cards)
    if self.stage == 1:
      print('Board cards:', self.board_cards[:3])
    elif self.stage == 2:
      print('Board cards:', self.board_cards[:4])
    elif self.stage == 3:
      print('Board cards:', self.board_cards[:5])
  

  def reveal_winner(self):
    player_hand_strength = np.array([])
    for i_player in range(self.n_players):
      if not self.folded_players[i_player]:
        player_hand_strength = np.append(player_hand_strength, 
          # evaluate_cards(*list(self.players[i_player].pocket_cards), *list(self.board_cards)))
          evaluate_cards(*self.players[i_player].pocket_cards, *self.board_cards))
      else:
        player_hand_strength = np.append(player_hand_strength, -1)
    print('Player hand strengths:', player_hand_strength)
    winner = np.argmax(player_hand_strength)
    print('Winner: Player', winner, 'with', self.players[winner].pocket_cards)
    return


  def play_game(self):
    print('------------------------')
    print('Game started')
    print('Human player(s): Nr.', *self.human_players)
    print('Big blind:', self.n_players-1)
    print('Small blind:', self.n_players-2)
    print('---------')
    for self.stage in range(4):
      self.print_game_state()
      self.round()
      print('---------')
    self.stage = 4
    self.reveal_winner()
    print('------------------------')
    return
  


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

def play_human_vs_bots(n_bots=2):
  game = Game(n_players=n_bots+1, human_players=[rand.randint(0,n_bots)])
  game.play_game()
  return

def play_bots_vs_bots(n_bots=3):
  game = Game(n_players=n_bots, human_players=[])
  game.play_game()
  return

