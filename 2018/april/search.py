import itertools
import subprocess
import sys

# From https://docs.python.org/3/library/itertools.html#recipes
def powerset(iterable):
  "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
  s = list(iterable)
  return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))

def compute_subsets(N, bound):
  all_subsets = []
  for subset in powerset(list(range(1,N+1))):
    # If total weight exceeds bound, ignore constraint
    # If constraint only single balloon, ignore as it is not useful
    if sum(subset) < bound and len(subset) > 1:
      all_subsets.append(subset)
  return all_subsets

def generate_minizinc(fname, N, constraints, bound):
  with open("{0}.mzn".format(fname), 'w') as fout:
    fout.write("include \"alldifferent.mzn\";\n")
    fout.write("array[1..{0}] of var 1..{0}: X;\n".format(N))
    for i in range(1, N+1):
      fout.write("var 1..{0}: x{1} = X[{1}];\n".format(N, i))
    fout.write("constraint alldifferent(X);\n")
    for subset in constraints:
      subset_sum = ""
      for i in range(len(subset)):
        subset_sum += "x{0}".format(subset[i])
        if i < len(subset) - 1:
          subset_sum += " + "
      fout.write("constraint {0} < {1};\n".format(subset_sum, bound))
    fout.write("constraint x1 != 1;\n")
    fout.write("solve satisfy;\n")

def unsat(fname):
  res = False
  cmd = "minizinc {0}.mzn > {0}.out".format(fname)
  subprocess.call(cmd, shell=True)
  with open("{0}.out".format(fname), 'r') as fin:
    line = fin.readline()
    if line == "=====UNSATISFIABLE=====\n":
      res = True
  return res

def main(N, print_all_solns):
  print("Problem instance: {0} balloons".format(N))
  print("Print all solutions? {0}".format(print_all_solns))

  fname = "{0}_{1}".format(N, print_all_solns)
  bound = N + 1 # Actually, bound = N + 0.5, but integer wise, no difference
  all_subsets = compute_subsets(N, bound)
  M = len(all_subsets)
  print("Number of useful constraints: {0}".format(M))

  '''
  For any given N, upper bound on soln_len is N-2 via:
  1,2
  1,3
  ...
  1,N-1
  '''
  soln_len = 1
  soln = None
  done = False
  num_considered = 0
  while not done and soln_len <= N-2:
    print("Searching over solutions of length {0}...".format(soln_len))
    for constraints in itertools.combinations(all_subsets, soln_len):
      num_considered += 1
      generate_minizinc(fname, N, constraints, bound)
      if unsat(fname):
        print("Found solution of length: {0}".format(soln_len))
        print(constraints)
        done = True
      if done and not print_all_solns:
        break
    if not done:
      soln_len += 1
  print("Total number of considered sets of tests: {0}".format(num_considered))

if __name__ == "__main__":
  N = int(sys.argv[1])
  print_all_solns = sys.argv[2] == '1'
  main(N, print_all_solns)

