# Problem URL  
http://www.research.ibm.com/haifa/ponderthis/challenges/May2018.html

I solved this month's challenge jointly with Daren Khu.

# Approach
Suppose we are given `N` balls (2 of which are fake and are lighter) and `M` weighs. `(N, M)` defines a problem instance. Of course one can generalise to different number of fake lighter balls.

We model the problem as a constraint search on how to fill up a `N`-by-`M` ternary matrix.

- `matrix[i][j] = 0` means ball `i` not used in weigh `j`
- `matrix[i][j] = 1` means ball `i` on left scale in weigh `j`
- `matrix[i][j] = 2` means ball `i` on right scale in weigh `j`

Define row `i` as "ball i's id”. Define column `j` as "weigh j's id”. These ids can be viewed as a ternary number.

As we fill up the matrix column by column (i.e. picking a weighing), we check if the weigh is “valid”.
A weigh is “valid” if it fulfils all 4 of the following conditions:

- Condition 1: No ball has id = 0

    That is, we don’t have any empty weighs that doesn’t use any balls.

- Condition 2: For each weigh, number of `1`'s = number of `2`’s

    That is, for every weigh, the number of balls on the left and right balances are equal.

- Condition 3: Ball ids are ordered (i.e. `A < B < ...`)

    Since the identity of the balls are useless, we enforce an ordering on the search so that we save `N!` permutations.

- Condition 4: Weighs so far can "distinguishing enough”

    This is the meat of the recursion insight. We know that `K` weighs can distinguish `3^K` possibilities, so for any problem instance `(N,M)` is not solvable if `3^M < (N choose 2)`. Using this insight, at any point, if the chosen weighs so far do not sufficiently split up `(N choose 2)` possibilities, then we know it will fail regardless of whatever future weighs we choose. Hence, we give up and choose another weigh, backtracking if necessary.


Below are sample runs for `(N, M) = (7, 3)` and `(N, M) = (11, 4)`:
```
Davins-MacBook-Pro:May2018 sozos$ time python3 recurse.py 7 3
[0, 0, 0]
[0, 1, 1]
[0, 2, 2]
[1, 1, 2]
[1, 2, 1]
[2, 0, 1]
[2, 0, 2]
DE-FG
BD-CE
BEF-CDG

real	0m0.138s
user	0m0.123s
sys	0m0.009s
Davins-MacBook-Pro:May2018 sozos$ time python3 recurse.py 11 4
[0, 0, 0, 0]
[0, 1, 1, 0]
[0, 1, 2, 1]
[0, 2, 1, 0]
[0, 2, 2, 2]
[1, 0, 2, 0]
[1, 1, 0, 2]
[1, 2, 0, 1]
[2, 0, 0, 1]
[2, 0, 0, 2]
[2, 0, 1, 0]
FGH-IJK
BCG-DEH
BDK-CEF
CHI-EGJ

real	35m38.473s
user	34m23.487s
sys	 0m6.994s
```

# Files
* README.md (This file)
* recurse.py

  Takes in two parameters:

  1. Number of balls `N` (of which 2 are lighter/fake)
  2. Number of weighs `M`
