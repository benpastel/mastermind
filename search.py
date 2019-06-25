from typing import List, Tuple

import numpy as np

# The actual Air Canada game had 6 colors, but only actually uses 4 of them
# in the solutions for some reason (a bug?).
#
# One of the results I'm most interested in is whether it's every optimal to guess
# the unused colors.  So I added a single color, Black, that's allowed in guesses
# but not in the solution.
#
# Start with two active colors for now & add the rest later.
COLORS = [
  'Red',
  'Blue',
  # 'Green',
  # 'Purple',
  'Black'
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

# include Black for guessing
GUESSES = all_combos(len(COLORS))

# exclude Black for solutions
# note that indices into SOLUTIONS are valid indices into
# the corresponding GUESSES, but not vice-versa
SOLUTIONS = all_combos(len(COLORS) - 1)

def find_hints(guess):
  # TODO pre-calc
  # not too optimized since we are going to pre-calc anyway

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

  return black_counts * 10 + white_counts


def search(valid: np.ndarray, moves: List[int], depth: int) -> Tuple:
  """
  the cost is the max number of moves to force a win; i.e. the final depth

  the player tries to minimize cost by choosing guesses;

  the demon tries to maximize cost by choosing hints for the guesses that are consistent
  with one of the remaining valid solutions

  returns: (best cost, list of moves that achieves that cost)
  """
  assert depth < 10

  valid_count = np.sum(valid)
  assert valid_count > 0
  if valid_count == 1:
    # there's only one remaining solution; we win by guessing it
    move = np.nonzero(valid)[0][0]
    return depth + 1, moves + [move]

  print(f"{valid_count}, {moves}, {depth}")

  min_move_cost = 100
  best_move_path = None
  for move, guess in enumerate(GUESSES):
    new_moves = moves + [move]

    # find the hint for each (guess, solution) pair and write to hints array
    hints = find_hints(guess)
    hints[~valid] = -1 # wipe the hints at solutions that are already invalid

    # choose among the unique, valid hints
    unique_hints, inverse = np.unique(hints, return_inverse=True)

    max_hint_cost = -1
    worst_hint_path = None
    for h, hint in enumerate(unique_hints):
      if hint == -1:
        continue

      # the new valid moves are the ones that would have produced this hint
      new_valid = (inverse == h)

      if np.sum(new_valid) < valid_count:
        hint_cost, path = search(new_valid, new_moves, depth + 1)
      else:
        hint_cost = 999
        path = None

      if hint_cost > max_hint_cost:
        worst_hint_path = path
        max_hint_cost = hint_cost

    if max_hint_cost < min_move_cost:
      best_move_path = worst_hint_path
      min_move_cost = max_hint_cost

  assert best_move_path is not None
  return min_move_cost, best_move_path

all_valid = np.ones(len(SOLUTIONS), dtype=bool)
print(search(all_valid, [], 0))
