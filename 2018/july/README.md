# Problem URL

http://www.research.ibm.com/haifa/ponderthis/challenges/July2018.html

# Approach
Directly encode problem as a constraint program. Solutions are then independently verified with a short Python script.

# Solution

The triplet {7, 30, 54} works.

Witnesses (for various offsets k = 0,1,2,3):
- K = 0: {10, 18, 63} => sum = 91, product = 11340
- K = 1: {10, 22, 62} => sum = 94, product = 13640
- K = 2: {12, 21, 64} => sum = 97, product = 16128
- K = 3: {15, 19, 66} => sum = 100, product = 18810

# Files
* README.md (This file)
* direct.mzn (Run with [Minizinc constraint solver](http://www.minizinc.org/))
* verify.py

Note that `direct.mzn` can be easily re-written in a more general/parameterized manner instead of hardcoding `k = 3` and the search upper limit `m = 100`.
