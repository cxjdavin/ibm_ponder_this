# Problem URL

http://www.research.ibm.com/haifa/ponderthis/challenges/March2018.html

# Approach
Model problem as the following constraint program: For any integer x in [0, 63], every letter is either at position x, or x^(2^j) for j = {0,1,2,3,4,5}.

My choice of constraint solver was [Minizinc constraint solver](http://www.minizinc.org/). The caveat was that it only has bit level XOR so I had to create my own N-bit XOR. I'm not sure how to create a general N-bit XOR via arrays, so I hardcoded 3-bit (in simple.mzn) and 6-bit (in full.mzn) XOR functions. Drop me a message if you know how to create general N-bit XOR functions!

# Files
* README.md (This file)
* simple.mzn (Run with [Minizinc constraint solver](http://www.minizinc.org/))

  Solution to simple problem of 3 switches and 3 letters 'A', 'B', 'C'

* full.mzn (Run with [Minizinc constraint solver](http://www.minizinc.org/))

  Solution to actual problem of 6 switches and 3 letters 'A', 'E', 'I', 'O', 'U'
