# Problem URL

http://www.research.ibm.com/haifa/ponderthis/challenges/June2018.html

# Approach
Model the problem as a constraint search problem, then post-process for solutions that do not have holes.

### Observation

Each L and J shape has 4 orientations.

L1 (3x2):
```
xo
xo
xx
```

L2 (3x2):
```
xx
ox
ox
```

L3 (2x3):
```
oox
xxx
```

L4 (2x3):
```
xxx
xoo
```

J1 (2x3):
```
ox
ox
xx
```

J2 (2x3):
```
xx
xo
xo
```

J3 (3x2):
```
xxx
oox
```

J4 (3x2):
```
xoo
xxx
```

Under this notation, our solution (see below)) contains {2 L1's, 1 L3, and 2 L4's} and {2 J1's, 1 J2, and 2 J4's}.

Consider a grid labelled in "1 + (modulo 4)" and how the orientation tile on it:
```
1 2 3 4
2 3 4 1
3 4 1 2
4 1 2 3
```

Observe a bipartition on the 4 orientations:
{L1, L2, J3, J4} : Cover 4 different numbers
{L3, L4, J1, J2} : Cover numbers "k, k+1, k+1, k+2", where k = 1,2,3,4 (then take modulo 4 appropriately)

This means that:
- n = (Number of L1) + (Number of L2) = (Number of J3) + (Number of J4)
- 5-n = (Number of L3) + (Number of L4) = (Number of J1) + (Number of J2)

Furthermore, since the L and J orientations are of different bounding dimensions (2x3 vs 3x2) in each partition, n and 5-n both cannot equal 1. i.e. (n != 1 and n != 4).

### Encoding as a constraint search

Using the observation, I encoded the problem as a search over R-by-C grid, where R and C are input parameters. Loop through all possible valid choices of 5 L/J-orientations (constrained by n = 5-n, and n != 1, and n != 4 as per the observation above)
1. Create an indicator variable for each possible location which each orientation can fit on the grid
2. Constrain that exactly 5 L-indicators and 5 J-indicators are toggled to True
3. Constrain that no 2 L-shapes overlap (i.e. at each grid cell, number of True L-indicators <= 1)
4. Constrain that no 2 J-shapes overlap (i.e. at each grid cell, number of True J-indicators <= 1)
5. Constrain that at each cell, (number of True L-indicators) = (number of True J-indicators)
6. Solve for all possible solutions, and check number of connected components of unused cells. Given a sufficiently large grid where the solution does not split the unused space, there should only be 1 connected component of unused cells. i.e. If there are >1, then there must be some holes in the layout proposed by the solution

Since there are 5 shapes, each taking 4 cells, at least 20 cells will be used. As such, I started my search from 5x5 grid (which yielded no solutions) and stumbled upon a solution on 6x6 grid.

### Sample run
```
Davins-MBP:June2018 sozos$ python3 generate.py 6 6 5
R = 6, C = 6, N = 5
[1, 1, 1, 0, 0, 0]
[1, 1, 1, 1, 1, 0]
[1, 1, 1, 0, 0, 0]
[1, 1, 1, 0, 0, 0]
[1, 1, 1, 0, 0, 0]
[1, 1, 1, 0, 0, 0]

Time taken: 331.29 seconds
```
Legend:
- 0: empty/unused
- 1: filled by shape

Solution annotated by L shapes (from 'a' to 'e'):
```
[a, a, a, 0, 0, 0]
[a, b, c, c, c, 0]
[d, b, c, 0, 0, 0]
[d, b, b, 0, 0, 0]
[d, d, e, 0, 0, 0]
[e, e, e, 0, 0, 0]
```

Solution annotated by J shapes (from 'a' to 'e'):
```
[a, a, b, 0, 0, 0]
[a, c, b, b, b, 0]
[a, c, d, 0, 0, 0]
[c, c, d, 0, 0, 0]
[e, d, d, 0, 0, 0]
[e, e, e, 0, 0, 0]
```

# Files
* README.md (This file)
* generate.py (Run with [Minizinc constraint solver](http://www.minizinc.org/))

  Takes in 3 parameters:
  1. Number of rows R
  2. Number of columns C
  3. Number of shapes N
