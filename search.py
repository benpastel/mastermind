import numpy as np

# The actual Air Canada game had 6 colors, but only actually uses 4 of them
# in the solutions for some reason (a bug?).
#
# One of the results I'm most interested in is whether it's every optimal to guess
# the unused colors.  So I added a single color, Black, that's allowed in guesses
# but not in the solution.
COLORS = [
  'Red',
  'Blue',
  'Green',
  'Purple',
  'Black'
]

def all_combos(num_colors: int):
  # returns an (n x 4) numpy array
  # where each row is a unique combination of the colors
  # the columns are the 4 in-game columns
  # and the values are indices into COLORS
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
GUESSES = all_combos(5)

# exclude Black for solutions
LEGALS = all_combos(4)
