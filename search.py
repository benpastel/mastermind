# python 3.6
from typing import List, Tuple
from time import time

import numpy as np

COLORS = [
  'Red',
  'Blue',
  'Green',
  'Purple',
]

def all_combos(num_colors: int) -> np.ndarray:
  """
  returns a (n x 4) array
  where each row is a unique combination of the colors
  the columns are the 4 in-game columns
  and the values are indices into COLORS
  """
  combos = np.zeros((num_colors ** 4, 4), dtype=np.uint8)
  i = 0
  for c1 in range(num_colors):
    for c2 in range(num_colors):
      for c3 in range(num_colors):
        for c4 in range(num_colors):
          combos[i] = (c1, c2, c3, c4)
          i += 1
  assert i == num_colors ** 4
  return combos

SOLUTIONS = all_combos(len(COLORS))

def find_hints(guess):
  # find hints (black & white pegs) for all solutions given a single guess
  # return black & white peg counts encoded as a single number
  #
  # this function is not optimized because hints are precalculated quickly

  # tile guess to the same size as solutions
  guesses = np.zeros_like(SOLUTIONS)
  guesses[:] = guess

  # make a scrap copy of solutions so we can modify in-place
  scrap = SOLUTIONS.copy()

  same = (guesses == scrap)
  black_counts = np.sum(same, axis=1)

  # anything already counted for black does not get counted for white
  scrap[same] = 255
  guesses[same] = 254

  white_counts = np.zeros_like(black_counts)
  for c in range(len(COLORS) - 1):
    guess_color_counts = np.sum(guesses == c, axis=1)
    scrap_color_counts = np.sum(scrap == c, axis=1)
    white_counts += np.minimum(guess_color_counts, scrap_color_counts)

  return 10 * black_counts + white_counts

WIN = 40 # see encoding above
def format_hint(hint):
  white = hint % 10
  black = int((hint - white) / 10)
  return f"(black: {black}, white: {white})"

# precalculate hints for all pairs of guesses and solutions
ALL_HINTS = np.zeros((len(SOLUTIONS), len(SOLUTIONS)), dtype=np.uint8)
for g, guess in enumerate(SOLUTIONS):
  ALL_HINTS[g] = find_hints(guess)

def format_move(move):
  return np.array(COLORS)[SOLUTIONS[move]] if move is not None else None

def search(valid: np.ndarray, depth: int) -> Tuple:
  """
  the cost is the max number of moves to force a win; i.e. the final depth

  the player tries to minimize cost by choosing guesses;

  the demon tries to maximize cost by choosing hints for the guesses that are consistent
  with one of the remaining valid solutions

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
      elif hint == WIN:
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
        hint_cost, next_move = search(new_valid, depth + 1)

      if depth == 0:
        logs.append(f"     {format_hint(uniques[h])} => {format_move(next_move)} (win in {hint_cost})")

      max_hint_cost = max(hint_cost, max_hint_cost)

    if depth == 0:
      print(f"  {format_move(move)} (win in {max_hint_cost}):")
      print('\n'.join(logs))

    if max_hint_cost < min_move_cost:
      best_move = move
      min_move_cost = max_hint_cost

  assert best_move is not None
  return min_move_cost, best_move

start = time()
all_valid = np.ones(len(SOLUTIONS), dtype=bool)
cost, move = search(all_valid, 0)
print(f"\n\nfound a solution in {cost} moves")
print(f"with first move: {format_move(move)}")
print(f" in {time() - start:.1f} seconds")
