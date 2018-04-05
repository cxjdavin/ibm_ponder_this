enum LETTER = {'A', 'E', 'I', 'O', 'U'};
array[1..64] of var LETTER: assignment;

function var int: int_xor(int: x, int: y) =
  ((x div 1 mod 2) + (y div 1 mod 2) - 2 * (x div 1 mod 2) * (y div 1 mod 2))*1 +
  ((x div 2 mod 2) + (y div 2 mod 2) - 2 * (x div 2 mod 2) * (y div 2 mod 2))*2 +
  ((x div 4 mod 2) + (y div 4 mod 2) - 2 * (x div 4 mod 2) * (y div 4 mod 2))*4 +
  ((x div 8 mod 2) + (y div 8 mod 2) - 2 * (x div 8 mod 2) * (y div 8 mod 2))*8 +
  ((x div 16 mod 2) + (y div 16 mod 2) - 2 * (x div 16 mod 2) * (y div 16 mod 2))*16 +
  ((x div 32 mod 2) + (y div 32 mod 2) - 2 * (x div 32 mod 2) * (y div 32 mod 2))*32;
  
predicate letter_ok(int: i, LETTER: l) =
  assignment[i] = l \/
  assignment[int_xor(i-1, 1) mod 64 + 1] = l \/
  assignment[int_xor(i-1, 2) mod 64 + 1] = l \/
  assignment[int_xor(i-1, 4) mod 64 + 1] = l \/
  assignment[int_xor(i-1, 8) mod 64 + 1] = l \/
  assignment[int_xor(i-1, 16) mod 64 + 1] = l \/
  assignment[int_xor(i-1, 32) mod 64 + 1] = l;

constraint forall(i in 1..64, l in LETTER)(letter_ok(i,l));

solve satisfy;
output ["\(assignment)"];
