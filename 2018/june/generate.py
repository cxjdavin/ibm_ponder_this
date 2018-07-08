import itertools
import subprocess
import sys
import time

def stringify(arr):
  result = ""
  for i in range(len(arr)):
    result += arr[i]
    if i < len(arr) - 1:
      result += " + "
  return result

def create_minizinc(mzn_fname, R, C, N, L_patterns, J_patterns):
  grid_vars = []
  for r in range(R):
    grid_vars.append([])
    for c in range(C):
      grid_vars[r].append([[],[]])
      
  indicator_dict = dict()
  with open(mzn_fname, 'w') as fout:
    # Setup problem
    L_count = 0
    L_indicators = []
    for pr, pc, pattern in L_patterns:
      for r in range(R):
        for c in range(C):
          # If pattern's top left cell can fit at grid[r][c]
          if pr + r <= R and pc + c <= C:
            L_count += 1
            v = "L_{0}".format(L_count)
            L_indicators.append(v)
            indicator_dict[v] = (r, c, pr, pc, pattern)

            # Fill mask in grid
            for mask_r in range(pr):
              for mask_c in range(pc):
                if pattern[mask_r][mask_c] == 1:
                  grid_vars[mask_r + r][mask_c + c][0].append(v)
                  
    J_count = 0
    J_indicators = []
    for pr, pc, pattern in J_patterns:
      for r in range(R):
        for c in range(C):
          # If pattern's top left cell can fit at grid[r][c]
          if pr + r <= R and pc + c <= C:
            J_count += 1
            v = "J_{0}".format(J_count)
            J_indicators.append(v)
            indicator_dict[v] = (r, c, pr, pc, pattern)

            # Fill mask in grid
            for mask_r in range(pr):
              for mask_c in range(pc):
                if pattern[mask_r][mask_c] == 1:
                  grid_vars[mask_r + r][mask_c + c][1].append(v)

    # Declare indictor variables
    for indicator in L_indicators:
      fout.write("var 0..1: {0};\n".format(indicator))
    L_indicators_string = "array[int] of var 0..1: L_indicators = ["
    for i in range(1, L_count+1):
      L_indicators_string += "L_{0}".format(i)
      if i < L_count:
        L_indicators_string += ", "
      else:
        L_indicators_string += "];\n"
    fout.write(L_indicators_string)
    for indicator in J_indicators:
      fout.write("var 0..1: {0};\n".format(indicator))
    J_indicators_string = "array[int] of var 0..1: J_indicators = ["
    for i in range(1, J_count+1):
      J_indicators_string += "J_{0}".format(i)
      if i < J_count:
        J_indicators_string += ", "
      else:
        J_indicators_string += "];\n"
    fout.write(J_indicators_string)
    
    # Exactly N patterns used
    fout.write("constraint sum(L_indicators) = {0};\n".format(N))
    fout.write("constraint sum(J_indicators) = {0};\n".format(N))
    
    for r in range(R):
      for c in range(C):
        if len(grid_vars[r][c][0]) != 0:
          # Grid cell has at most 1 indictor variable active
          fout.write("constraint ({0}) <= 1;\n".format(stringify(grid_vars[r][c][0])))
        if len(grid_vars[r][c][1]) != 0:
          # Grid cell has at most 1 indictor variable active
          fout.write("constraint ({0}) <= 1;\n".format(stringify(grid_vars[r][c][1])))
        if len(grid_vars[r][c][0]) != 0 and len(grid_vars[r][c][1]) != 0:
          # L and J patterns cancel out
          fout.write("constraint ({0}) = ({1});\n".format(stringify(grid_vars[r][c][0]), stringify(grid_vars[r][c][1])))
  
    # Solve and print indictor assignments
    fout.write("solve satisfy;\n")
    fout.write("output [\"\(L_indicators)\"];\n")
  return indicator_dict

def print_grid(R, C, N, indicator_dict, result):
  # Extract activated patterns
  activated = [indicator_dict["L_{0}".format(i+1)] for i in range(len(result)) if result[i] == 1]

  # Initialize grid
  grid = []
  for r in range(R):
    grid.append([])
    for c in range(C):
      grid[r].append(0)
  
  # Draw patterns on grid
  for r, c, pr, pc, pattern in activated:
    for i in range(pr):
      for j in range(pc):
        if pattern[i][j] == 1:
          grid[r+i][c+j] += 1
 
  # Sanity check
  assert(sum([sum(grid[r]) for r in range(R)]) == 4*N)

  # Check for holes by counting connected components of 0
  num_cc = 0
  seen = set()
  for i in range(R):
    for j in range(C):
      if grid[i][j] == 0 and (i,j) not in seen:
        num_cc += 1
        explore_set = set()
        explore_set.add((i,j))
        while len(explore_set) != 0:
          r,c = explore_set.pop()
          seen.add((r,c))
          if c-1 >= 0 and grid[r][c-1] == 0 and (r,c-1) not in seen:
            explore_set.add((r,c-1))
          if c+1 < C and grid[r][c+1] == 0 and (r,c+1) not in seen:
            explore_set.add((r,c+1))
          if r-1 >= 0 and grid[r-1][c] == 0 and (r-1,c) not in seen:
            explore_set.add((r-1,c))
          if r+1 < R and grid[r+1][c] == 0 and (r+1,c) not in seen:
            explore_set.add((r+1,c))

  if num_cc == 1:
    # Print grid
    for r in range(R):
      print(grid[r])
    print()
    return True
  else:
    return False

def main(R, C, N):
  # 4 orientations of "L" pattern
  L_pat1 = (3, 2, [[1, 0],[1, 0],[1, 1]])
  L_pat2 = (3, 2, [[1, 1],[0, 1],[0, 1]])
  L_pat3 = (2, 3, [[1, 1, 1],[1, 0, 0]])
  L_pat4 = (2, 3, [[0, 0, 1],[1, 1, 1]])
  L_pats = [L_pat1, L_pat2, L_pat3, L_pat4]
  
  # 4 orientations of "J" pattern
  J_pat1 = (3, 2, [[0, 1],[0, 1],[1, 1]])
  J_pat2 = (3, 2, [[1, 1],[1, 0],[1, 0]])
  J_pat3 = (2, 3, [[1, 1, 1],[0, 0, 1]])
  J_pat4 = (2, 3, [[1, 0, 0],[1, 1, 1]])
  J_pats = [J_pat1, J_pat2, J_pat3, J_pat4]
  
  all_dicts = dict()
  instance_count = 0
  for x in itertools.combinations_with_replacement(list(range(4)), N):
    for y in itertools.combinations_with_replacement(list(range(4)), N):
      instance_count += 1
      instance_start = time.time()
  
      # Generate instance
      x_idx = sum([pow(4,i)*x[i] for i in range(len(x))])
      y_idx = sum([pow(4,i)*y[i] for i in range(len(y))])
      idx = "{0}_{1}".format(x_idx, y_idx)
      fname = "{0}_{1}__{2}.mzn".format(R, C, idx)
      L_patterns = [L_pats[x[i]] for i in range(N)]
      J_patterns = [J_pats[y[i]] for i in range(N)]
      Ln = sum([1 if (x[i] == 0 or x[i] == 1) else 0 for i in range(N)])
      Jn = sum([1 if (y[i] == 0 or y[i] == 1) else 0 for i in range(N)])
      if Ln != Jn or Ln == 1 or Ln == 4:
        continue
      all_dicts[idx] = create_minizinc(fname, R, C, N, L_patterns, J_patterns)
  
      # Run instance
      cmd = "minizinc {0} -a -o {0}.out".format(fname)
      subprocess.call(cmd, shell=True)
  
      # Process output
      done = False
      has_soln = False
      with open("{0}.out".format(fname), 'r') as fp:
        dashes = False
        for line in fp:
          if dashes:
            dashes = False
          else:
            if line[0] != '=': # != "=====UNSATISFIABLE=====\n":
              has_soln = True
              soln = [int(x[0]) for x in line[1:-2].split()]
              done = print_grid(R, C, N, all_dicts[idx], soln)
              if done:
                break
            dashes = True
      if not has_soln:
        cmd = "rm {0} {0}.out".format(fname)
        subprocess.call(cmd, shell=True)
      #print("Instance {0} done in {1:.2f} seconds".format(instance_count, time.time() - instance_start))
      if done:
        return()

if __name__ == "__main__":
  R = int(sys.argv[1])
  C = int(sys.argv[2])
  N = int(sys.argv[3])

  start_time = time.time()
  print("R = {0}, C = {1}, N = {2}".format(R, C, N))
  main(R, C, N)
  end_time = time.time()
  print("Time taken: {0:.2f} seconds".format(end_time - start_time))

