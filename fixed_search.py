# python 3.6
#
# Since we already have a 5-solution from restricted_search,
# this method looks for 4-move solutions only.
#
# This allows us to make special optimizations for each move.

import numpy as np
from shared import all_combos, find_hints, format_hint

COLORS = np.array([
  'Red',
  'Blue',
  'Green',
  'Purple',
  'Black' # allowed in guesses but not solutions
])

GUESSES = all_combos(len(COLORS))
SOLUTIONS = all_combos(len(COLORS) - 1)

ALL_HINTS = np.zeros((len(GUESSES), len(SOLUTIONS)), dtype=np.uint8)
for g, guess in enumerate(GUESSES):
  ALL_HINTS[g] = find_hints(guess, SOLUTIONS, len(COLORS))


def format_move(m):
  return COLORS[GUESSES[m]]

def format_solution(s):
  return COLORS[SOLUTIONS[s]]

# represents which solutions are consistent after the 2nd-round hint
# declare now and re-use for effiency
valid2 = np.zeros(len(SOLUTIONS), dtype=bool)


def search_3rd_guesses(valid2, print_tree):
  # if any 3rd guess generates a unique hint for each remaining valid solution,
  # we'll win by guessing it on the 4th guess.
  #
  # if it doesn't, then there's no way to win on the 4th guess.
  hints_for_guess3 = ALL_HINTS[:, valid2]
  for guess3 in range(len(GUESSES)):
    # checking for bincount collisions is faster than unique
    if np.all(np.bincount(hints_for_guess3[guess3]) <= 1):
      if print_tree:
        print(format_move(guess3))
        for s in range(len(SOLUTIONS)):
          if valid2[s]:
            print(f"        {format_hint(ALL_HINTS[guess3, s])} => {format_solution(s)}")

      return True
  return False


def search_2nd_hints(guess2, valid1, valid1_count, print_tree):
  # all unique hints that can be produced by the 2nd guess
  uniques, inverse = np.unique(ALL_HINTS[guess2][valid1], return_inverse=True)

  for hint2 in range(len(uniques)):
    valid2[:] = False
    valid2[valid1] = (hint2 == inverse)

    if np.count_nonzero(valid2) == valid1_count:
      # we gained no information from this hint
      return False

    if print_tree:
      print(f"    {format_hint(uniques[hint2])} => " , end="")

    if not search_3rd_guesses(valid2, print_tree):
      return False

  return True

def search_2nd_guesses(valid1, valid1_count, print_tree):
  # for the 2nd move, only search the guesses with Red or Blue first
  # (Red is fixed because of guess1, but we can relabel any other color to Blue)
  # TODO: also consider the ones where Black comes first, and there are least 2 black
  for guess2 in range(2 * len(GUESSES) // len(COLORS)):

    if search_2nd_hints(guess2, valid1, valid1_count, False):
      if print_tree:
        print(format_move(guess2))
        search_2nd_hints(guess2, valid1, valid1_count, True)
      return True

  return False


def search_1st_hints(guess1, print_tree):
  # all unique hints that can be produced by the 1st guess
  uniques, inverse = np.unique(ALL_HINTS[guess1], return_inverse=True)

  for hint1 in range(len(uniques)):
    # which solutions are consistent with the hint
    valid1 = (hint1 == inverse)
    valid1_count = np.count_nonzero(valid1)

    if print_tree:
      print(f"  {format_hint(uniques[hint1])} => " , end="")

    if not search_2nd_guesses(valid1, valid1_count, print_tree):
      return False

  return True


def search_1st_guesses():
  # for the 1st move, only search the guesses with Red first
  #   (if Blue, Green, or Purple comes first, relabel the colors so that it's Red)
  #   (if Black comes first, switch the columns so it doesn't, and skip
  #     the all-Black guess)
  for guess1 in range(len(GUESSES) // len(COLORS)):
    if search_1st_hints(guess1, print_tree=False):
      print(f"Solution found!")
      print(format_move(guess1))

      # retrace our steps, but printing this time
      search_1st_hints(guess1, print_tree=True)
      return
    else:
      print(f"  no solution: {format_move(guess1)}")
  print("No solution found.")


search_1st_guesses()
