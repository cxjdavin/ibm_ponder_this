var int: a;
var int: b;
var int: c;
var int: x0;
var int: y0;
var int: z0;
var int: x1;
var int: y1;
var int: z1;
var int: x2;
var int: y2;
var int: z2;
var int: x3;
var int: y3;
var int: z3;

% Enforces numbers in tuple to be distinct (<= works if this is not required)
% The ordering is used to break symmetry
% 100 is a hard-coded parameter. If it fails, increase it
constraint 1 <=  a /\  a <  b /\  b <  c /\  c <= 100;
constraint 1 <= x0 /\ x0 < y0 /\ y0 < z0 /\ z0 <= 100;
constraint 1 <= x1 /\ x1 < y1 /\ y1 < z1 /\ z1 <= 100;
constraint 1 <= x2 /\ x2 < y2 /\ y2 < z2 /\ z2 <= 100;
constraint 1 <= x3 /\ x3 < y3 /\ y3 < z3 /\ z3 <= 100;

% Enforce that witnesses are not just permutations of (a+k,b+k,c+k)
constraint ((a != x0 /\ a != y0 /\ a != z0)
         \/ (b != x0 /\ b != y0 /\ b != z0)
         \/ (c != x0 /\ c != y0 /\ c != z0));
constraint ((a+1 != x1 /\ a+1 != y1 /\ a+1 != z1)
         \/ (b+1 != x1 /\ b+1 != y1 /\ b+1 != z1)
         \/ (c+1 != x1 /\ c+1 != y1 /\ c+1 != z1));
constraint ((a+2 != x2 /\ a+2 != y2 /\ a+2 != z2)
         \/ (b+2 != x2 /\ b+2 != y2 /\ b+2 != z2)
         \/ (c+2 != x2 /\ c+2 != y2 /\ c+2 != z2));
constraint ((a+3 != x3 /\ a+3 != y3 /\ a+3 != z3)
         \/ (b+3 != x3 /\ b+3 != y3 /\ b+3 != z3)
         \/ (c+3 != x3 /\ c+3 != y3 /\ c+3 != z3));
         
% Enforce sum and product equalities
constraint (a+b+c) = (x0+y0+z0);
constraint (a*b*c) = (x0*y0*z0);
constraint (a+b+c+3) = (x1+y1+z1);
constraint ((a+1)*(b+1)*(c+1)) = (x1*y1*z1);
constraint (a+b+c+6) = (x2+y2+z2);
constraint ((a+2)*(b+2)*(c+2)) = (x2*y2*z2);
constraint (a+b+c+9) = (x3+y3+z3);
constraint ((a+3)*(b+3)*(c+3)) = (x3*y3*z3);

% Print out Python function calls
solve satisfy;
output
["check(0, \(a), \(b), \(c), \(x0), \(y0), \(z0))\n"] ++
["check(1, \(a), \(b), \(c), \(x1), \(y1), \(z1))\n"] ++
["check(2, \(a), \(b), \(c), \(x2), \(y2), \(z2))\n"] ++
["check(3, \(a), \(b), \(c), \(x3), \(y3), \(z3))\n"];