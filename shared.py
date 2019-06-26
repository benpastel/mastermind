import numpy as np

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

def find_hints(guess, solutions, num_colors):
  # find hints (black & white pegs) for all solutions given a single guess
  # return black & white peg counts encoded as a single number
  #
  # this function is not optimized because hints are precalculated quickly

  # tile guess to the same size as solutions
  guesses = np.zeros_like(solutions)
  guesses[:] = guess

  # make a scrap copy of solutions so we can modify in-place
  scrap = solutions.copy()

  same = (guesses == scrap)
  black_counts = np.sum(same, axis=1)

  # anything already counted for black does not get counted for white
  scrap[same] = 255
  guesses[same] = 254

  white_counts = np.zeros_like(black_counts)
  for c in range(num_colors):
    guess_color_counts = np.sum(guesses == c, axis=1)
    scrap_color_counts = np.sum(scrap == c, axis=1)
    white_counts += np.minimum(guess_color_counts, scrap_color_counts)

  return 10 * black_counts + white_counts

WIN = 40 # see encoding above
def format_hint(hint):
  white = hint % 10
  black = int((hint - white) / 10)
  return f"(black: {black}, white: {white})"
