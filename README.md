# mastermind
Finds the best strategies for a specific mastermind clone on the Air Canada in-flight touchscreens.

If the guesses are restricted to solutions that are consistent with the guesses so far, the best you can do is win in 5 moves.  And you can force a win in 5 moves from literally any starting guess.

The output below prints the explored game tree up to depth 2.  It's not the full game tree because I do some simple pruning (a partial implementation of alpha-beta pruning).
```
python search.py
```
=>
```
  ['Red' 'Red' 'Red' 'Red'] (win in 5):
     (black: 0, white: 0) => ['Blue' 'Blue' 'Blue' 'Green'] (win in 5)
     (black: 1, white: 0) => ['Red' 'Blue' 'Blue' 'Green'] (win in 5)
     (black: 2, white: 0) => ['Red' 'Red' 'Blue' 'Blue'] (win in 5)
     (black: 3, white: 0) => ['Red' 'Red' 'Red' 'Blue'] (win in 5)
     (black: 4, white: 0) => None (win in 1)
  ['Red' 'Red' 'Red' 'Blue'] (win in 5):
     (black: 0, white: 0) => ['Green' 'Green' 'Green' 'Purple'] (win in 5)
  ['Red' 'Red' 'Red' 'Green'] (win in 5):
     (black: 0, white: 0) => ['Blue' 'Blue' 'Blue' 'Purple'] (win in 5)
  ['Red' 'Red' 'Red' 'Purple'] (win in 5):
     (black: 0, white: 0) => ['Blue' 'Blue' 'Blue' 'Green'] (win in 5)
  ['Red' 'Red' 'Blue' 'Red'] (win in 5):
     (black: 0, white: 0) => ['Green' 'Green' 'Green' 'Purple'] (win in 5)
  ['Red' 'Red' 'Blue' 'Blue'] (win in 5):
     (black: 0, white: 0) => ['Green' 'Green' 'Green' 'Purple'] (win in 5)
  ['Red' 'Red' 'Blue' 'Green'] (win in 5):
     (black: 0, white: 0) => ['Purple' 'Purple' 'Purple' 'Purple'] (win in 2)
     (black: 0, white: 1) => ['Blue' 'Purple' 'Purple' 'Blue'] (win in 4)
     (black: 0, white: 2) => ['Blue' 'Blue' 'Red' 'Blue'] (win in 5)
  ['Red' 'Red' 'Blue' 'Purple'] (win in 5):
     (black: 0, white: 0) => ['Green' 'Green' 'Purple' 'Green'] (win in 4)
     (black: 0, white: 1) => ['Blue' 'Green' 'Green' 'Green'] (win in 4)
     (black: 0, white: 2) => ['Blue' 'Blue' 'Green' 'Red'] (win in 4)
     (black: 0, white: 3) => ['Blue' 'Blue' 'Red' 'Red'] (win in 4)
     (black: 1, white: 0) => ['Red' 'Green' 'Green' 'Green'] (win in 5)
  ['Red' 'Red' 'Green' 'Red'] (win in 5):
     (black: 0, white: 0) => ['Blue' 'Blue' 'Blue' 'Purple'] (win in 5)
  ['Red' 'Red' 'Green' 'Blue'] (win in 5):
     (black: 0, white: 0) => ['Purple' 'Purple' 'Purple' 'Purple'] (win in 2)
     (black: 0, white: 1) => ['Blue' 'Purple' 'Blue' 'Purple'] (win in 4)
     (black: 0, white: 2) => ['Blue' 'Blue' 'Red' 'Purple'] (win in 5)
  ['Red' 'Red' 'Green' 'Green'] (win in 5):
     (black: 0, white: 0) => ['Blue' 'Blue' 'Blue' 'Purple'] (win in 5)
  ['Red' 'Red' 'Green' 'Purple'] (win in 5):
     (black: 0, white: 0) => ['Blue' 'Blue' 'Purple' 'Blue'] (win in 4)
     (black: 0, white: 1) => ['Blue' 'Green' 'Blue' 'Blue'] (win in 4)
     (black: 0, white: 2) => ['Blue' 'Green' 'Red' 'Blue'] (win in 4)
     (black: 0, white: 3) => ['Blue' 'Green' 'Red' 'Red'] (win in 4)
     (black: 1, white: 0) => ['Red' 'Blue' 'Blue' 'Blue'] (win in 5)

  [...]

found a solution in 5 moves
with first move: ['Red' 'Red' 'Red' 'Red']
 in 23.1 seconds
```
