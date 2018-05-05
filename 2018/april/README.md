# Problem URL  http://www.research.ibm.com/haifa/ponderthis/challenges/April2018.html

# Approach
Model problem as the following constraint program: For any integer x in [0, 63], every letter is either at position x, or x^(2^j) for j = {0,1,2,3,4,5}.


### Step 1
With N balloons, there are 2^N possible constraints (i.e. Pick subset of 9 balloons), but not all are useful. We can prune by ignoring
- Constraints with only 1 balloon (This gives no information)
- Constraints where sum of balloons exceed bound of N+0.5 (since balloon weights are integral, it’s ok to check sum(balloons) < N+1)

### Step 2
Suppose there are K useful constraints. We can form 2^K sets. Since we want the minimal sized solution, we search with increasing group size.
I modelled each set S as a constraint problem instance:
- x_1, … , x_N are variables that can take up values from 1 to N
- Constrain that each x_i has a different value assignment
- Add in constraints from the set S of useful constraints
- Constrain that x_1 != 1
By Step 1’s construction, any set S is satisfiable with the solution “x_i = i, for i = 1, 2, … , 9”. The last constraint essentially bans that solution. That is, if the constraint problem instance is satisfiable, then there is some other assignment for the weight 1 balloon, so set S is insufficient in disambiguating the balloon of weight 1. Therefore, given set S, if the corresponding constraint problem instance is unsatisfiable, then S is a solution to the balloon problem.

For N = 6, we have K = 7 useful constraints and only 1 solution of minimal length 3: ((1, 4), (1, 5), (1, 2, 3))
For N = 9, we have K = 23 useful constraints and 5 solutions of minimal length 4. Namely,
- (2, 7), (1, 2, 6), (1, 3, 4), (1, 3, 5)
- (4, 5), (1, 2, 6), (1, 3, 4), (1, 3, 5)
- (1, 2, 4), (1, 2, 5), (1, 3, 4), (1, 3, 5)
- (1, 2, 4), (1, 2, 6), (1, 3, 4), (1, 3, 5)
- (1, 2, 5), (1, 2, 6), (1, 3, 4), (1, 3, 5)

Below is a sample run with N = 1, printing all solutions:
```
Davins-MacBook-Pro:April2018 sozos$ time python3 search.py 9 1
Problem instance: 9 balloons
Print all solutions? True
Number of useful constraints: 23
Searching over solutions of length 1...
Searching over solutions of length 2...
Searching over solutions of length 3...
Searching over solutions of length 4...
Found solution of length: 4
((2, 7), (1, 2, 6), (1, 3, 4), (1, 3, 5))
Found solution of length: 4
((4, 5), (1, 2, 6), (1, 3, 4), (1, 3, 5))
Found solution of length: 4
((1, 2, 4), (1, 2, 5), (1, 3, 4), (1, 3, 5))
Found solution of length: 4
((1, 2, 4), (1, 2, 6), (1, 3, 4), (1, 3, 5))
Found solution of length: 4
((1, 2, 5), (1, 2, 6), (1, 3, 4), (1, 3, 5))
Total number of considered sets of tests: 10902

real  10m41.616s
user  8m18.204s
sys   2m39.500s
```

# Files
* README.md (This file)
* search.py (Runs with [Minizinc constraint solver](http://www.minizinc.org/))

  Takes in two parameters: (1) size of problem N; (2) Print all solutions, or just the first. `compute_subsets` performs Step 1, then `generate_minizinc` and `unsat` performs Step 2.
