include "alldifferent.mzn";

% List of primes up to 1000
set of int: primes = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997};

% Assignment of gold and water
int: N = 9;
array[1..N] of var int: G;
array[1..N] of var int: W;
constraint forall(i in 1..N)(G[i] > 0);
constraint forall(i in 1..N)(W[i] > 0);

% S = water split amongst everyone, including Sauron
% Gold given is proportional to water contributed: G[i]/(W[i] - S) equal for each i
% Rewrite without fractions: constraint forall(i in 2..N)(G[i-1]/(W[i-1] - sum(W)/(N+1)) =  G[i]/(W[i] - sum(W)/(N+1)));
constraint forall(i in 2..N)(G[i-1]/((N+1)*W[i-1] - sum(W)) =  G[i]/((N+1)*W[i] - sum(W)));

% Indicator function
% P[1..9] = True -> G[1..9] is prime; P[10..18] = True -> W[1..9] is prime
array[1..2*N] of var bool: P;
constraint forall(i in 1..N)(P[i] -> G[i] in primes);
constraint forall(i in 1..N)(P[N+i] -> W[i] in primes);

% W_1+W_2+...+W_9 = G_1+G_2+...+G_9
constraint sum(G) = sum(W);

% All different
constraint alldifferent(G ++ W);
constraint forall(i in 2..N)(G[i-1] < G[i]);
constraint forall(i in 2..N)(W[i-1] < W[i]);

% At least 17 of them are prime numbers.
constraint sum(P) >= 2*N-1;
% constraint sum(P) = 2*N; % Use this if we want 18 primes

solve satisfy;

output ["W = \(W)\n"] ++ ["G = \(G)\n"];
