# Problem URL

http://www.research.ibm.com/haifa/ponderthis/challenges/August2018.html

# Solution

### Solution \#1
Here’s a solution with 17 primes:

- W = [189, 191, 193, 197, 199, 211, 227, 239, 241]
- G = [3, 23, 43, 83, 103, 223, 383, 503, 523]
- sum(W) = sum(G) = 1887
- Each 0.1 unit of water contributed will gain 1 unit of gold.

### Solution \#2
If we change the constraint to 18 primes (instead of >= 17 primes), we have the following solution:

- W = [223, 227, 229, 233, 239, 241, 251, 257, 317]
- G = [13, 53, 73, 113, 173, 193, 293, 353, 953]

# Approach

I directly encoded it into a constraint program. See attached for the Minizinc script.

Modify "constraint sum(P) >= 2\*N-1;” to "constraint sum(P) = 2\*N;” to generate Solution \#2.
Both variants run in under a second.

# Files
* README.md (This file)
* august.mzn (Run with [Minizinc constraint solver](http://www.minizinc.org/))
