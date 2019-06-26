# python 3.6
from typing import List, Tuple
from time import time

import numpy as np

from shared import all_combos, find_hints, WIN, format_hint

COLORS = [
  'Red',
  'Blue',
  'Green',
  'Purple',
]

SOLUTIONS = all_combos(len(COLORS))

ALL_HINTS = np.zeros((len(SOLUTIONS), len(SOLUTIONS)), dtype=np.uint8)
for g, guess in enumerate(SOLUTIONS):
  ALL_HINTS[g] = find_hints(guess, SOLUTIONS, len(COLORS))

def format_move(move):
  return np.array(COLORS)[SOLUTIONS[move]] if move is not None else None

def search_restricted(valid: np.ndarray, depth: int) -> Tuple:
  """
  the cost is the max number of moves to force a win; i.e. the final depth

  the player tries to minimize cost by choosing guesses;

  the demon tries to maximize cost by choosing hints for the guesses that are consistent
  with one of the remaining valid solutions

  this method only considers guesses that are potential solutions

  returns: (best cost, move that achieves that cost)
  """
  min_move_cost = 100
  best_move = None
  for move in np.nonzero(valid)[0]:
    # find the possible hints from valid solutions after this guess
    hints = ALL_HINTS[move][valid]

    # for printing out parts of the game tree
    logs = []

    # choose among the unique hints
    uniques, inverse, counts = np.unique(hints, return_inverse=True, return_counts=True)

    max_hint_cost = -1
    # re-use a single array for efficiency
    new_valid = np.zeros(len(SOLUTIONS), dtype=bool)
    for h, hint in enumerate(uniques):
      if max_hint_cost >= min_move_cost:
        # this is already equal or worse to a move we already searched
        # so stop searching
        continue

      if hint == WIN:
        hint_cost = depth + 1
        next_move = None
      elif counts[h] == 1:
        # only a single solution; we will win on the next round by guessing it
        hint_cost = depth + 2
        next_move = np.arange(len(SOLUTIONS))[valid][inverse == h][0]
        assert len(np.arange(len(SOLUTIONS))[valid][inverse == h]) == 1

      else:
        # the new valid moves are the ones that would have produced this hint
        new_valid[:] = 0
        new_valid[valid] = (inverse == h)
        hint_cost, next_move = search_restricted(new_valid, depth + 1)

      if depth == 0:
        logs.append(f"     {format_hint(uniques[h])} => {format_move(next_move)} (win in {hint_cost})")

      max_hint_cost = max(hint_cost, max_hint_cost)

    if depth == 0 and max_hint_cost != 5:
      print(f"  {format_move(move)} (win in {max_hint_cost}):")
      print('\n'.join(logs))

    if max_hint_cost < min_move_cost:
      best_move = move
      min_move_cost = max_hint_cost

  assert best_move is not None
  return min_move_cost, best_move

if __name__ == '__main__':
  start = time()
  all_valid = np.ones(len(SOLUTIONS), dtype=bool)
  cost, move = search_restricted(all_valid, 0)
  print(f"\n\nfound a solution in {cost} moves")
  print(f"with first move: {format_move(move)}")
  print(f" in {time() - start:.1f} seconds")
