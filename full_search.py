# python 3.6
from typing import List, Tuple
from time import time

import numpy as np

from shared import all_combos, find_hints, WIN, format_hint

COLORS = [
  'Red',
  'Blue',
  'Green',
  # 'Purple',
  'Black' # allowed in guesses but not solutions
]

GUESSES = all_combos(len(COLORS))
SOLUTIONS = all_combos(len(COLORS) - 1)

ALL_HINTS = np.zeros((len(GUESSES), len(SOLUTIONS)), dtype=np.uint8)
for g, guess in enumerate(GUESSES):
  ALL_HINTS[g] = find_hints(guess, SOLUTIONS, len(COLORS))

def format_move(move):
  return np.array(COLORS)[GUESSES[move]] if move is not None else None

def full_search(
    valid: np.ndarray = np.ones(len(SOLUTIONS), dtype=bool),
    depth: int = 0,
    abort_above_cost: int = 5,
    abort_below_cost: int = -1
  ) -> Tuple:
  """
  the cost is the max number of moves to force a win; i.e. the final depth

  the player tries to minimize cost by choosing guesses;

  the demon tries to maximize cost by choosing hints for the guesses that are consistent
  with one of the remaining valid solutions

  unlike the restricted search, this method considers guesses that are not
  currently valid solutions - for example guesses that contain Black.

  abort_above_cost is the best solution we can force
    ("alpha" in alpha-beta search)
  start with this at 5 instead of the usual +infinity
  because restricted_search found 5-move solutions

  abort_below_cost is the worst solution the demon can force on this branch of the tree
    ("beta" in alpha-beta search)

  returns: (best cost, move that achieves that cost)
  """
  # TODO shortcut this before the recursive call
  if depth >= abort_above_cost:
    return depth, None

  valid_count = np.sum(valid)

  # restricted search already found solutions that cost 5
  # so we'll abort if a search path hits 5
  min_move_cost = 100
  best_move = None

  # first pass: figure out which moves are promising
  guess_scores = np.zeros(len(GUESSES), dtype=int)
  for move in range(len(GUESSES)):
    hints = ALL_HINTS[move][valid]

    # heuristic: we want as few solutions as possible to give the same hint
    # so we want a low max count of how many hints each unique hint has
    _, counts = np.unique(hints, return_counts=True)
    guess_scores[move] = np.max(counts)

  # now search in score order from low to high
  for move in np.argsort(guess_scores):
    if guess_scores[move] == valid_count:
      # all the solutions had the same hint
      # so guesses from here on give us literally 0 information
      # and we can safely ignore them
      break

    if guess_scores[move] == 1:
      # all of the solutions give unique hints
      # we win next turn
      return depth + 2, None

    if min_move_cost <= abort_below_cost:
      # the demon can already force an equally bad branch
      # so stop searching
      return min_move_cost, None

    hints = ALL_HINTS[move][valid]

    # choose among the unique hints
    uniques, inverse, counts = np.unique(hints, return_inverse=True, return_counts=True)

    # order the hints so that we explore the LEAST promising one first
    # this increases the chances that it's too slow and we can abort this path
    hint_order = np.argsort(counts)[::-1]

    max_hint_cost = -1
    new_valid = np.zeros(len(SOLUTIONS), dtype=bool) # re-use for efficiency
    for h in hint_order:
      if max_hint_cost >= abort_above_cost:
        # this is already equal or worse to a move we already searched
        # so stop searching
        continue

      if hints[h] == WIN:
        # TODO: I don't think we need this case anymore?
        hint_cost = depth + 1
        next_move = None
      elif counts[h] == 1:
        # only a single solution; we will win on the next round by guessing it
        hint_cost = depth + 2
        next_move = None # TODO update properly
      else:
        # the new valid moves are the ones that would have produced this hint
        new_valid[:] = 0
        new_valid[valid] = (inverse == h)
        hint_cost, next_move = full_search(new_valid, depth + 1, abort_above_cost, max_hint_cost)

      max_hint_cost = max(hint_cost, max_hint_cost)

    if max_hint_cost < min_move_cost:
      best_move = move
      min_move_cost = max_hint_cost
      abort_above_cost = min(min_move_cost, abort_above_cost)

  return min_move_cost, best_move

if __name__ == '__main__':
  start = time()
  cost, move = full_search()
  print(f"\n\nfound a solution in {cost} moves")
  print(f"with first move: {format_move(move)}")
  print(f" in {time() - start:.1f} seconds")
