import itertools
import sys

'''
matrix[i][j] = 0 means ball i not used in weigh j
matrix[i][j] = 1 means ball i on left scale in weigh j
matrix[i][j] = 2 means ball i on right scale in weigh j

Define row i as "ball i's id"
Define col j as "weigh j's id"
These ids can be viewed as a ternary number
'''

def num_to_vec(num, sz):
  vec = []
  while len(vec) != sz:
    vec.append(int(num % 3))
    num = (num - (num % 3)) // 3
  return vec

def vec_to_num(vec):
  return sum([pow(3, len(vec)-i) * vec[i] for i in range(len(vec))])

# Check if weighs 0, ... , col are valid
# Condition 1: No ball has id = 0
# Condition 2: For each weigh, #1's = #2's
# Condition 3: Ball ids are ordered (i.e. A < B < ...)
# Condition 4: Weighs so far can "distinguishing enough"
def valid(matrix, col):
  N = len(matrix)
  M = len(matrix[0])

  #
  # Condition 1
  #
  # Trivially satisfied since we skip state = 0

  #
  # Condition 2
  #
  num_left = sum([1 if matrix[i][col] == 1 else 0 for i in range(N)])
  num_right = sum([1 if matrix[i][col] == 2 else 0 for i in range(N)])
  if num_left != num_right:
    return False

  #
  # Condition 3
  #
  ball_ids = [vec_to_num(matrix[i][:col+1]) for i in range(N)]
  for i in range(1, N):
    if ball_ids[i-1] > ball_ids[i]:
      return False

  #
  # Condition 4
  #
  # For each possible pair of fake balls,
  #   simulate each weigh and increment bucket count
  # If there is a bucket that has too many balls,
  #   then we cannot distinguish all possible cases
  buckets = [0] * pow(3, col+1)
  for fake in itertools.combinations(range(N), 2):
    idx = 0
    for j in range(col+1):
      idx *= 3
      left = [i for i in range(N) if matrix[i][j] == 1]
      right = [i for i in range(N) if matrix[i][j] == 2]
      left_weight = sum([1 if i not in fake else 0 for i in left])
      right_weight = sum([1 if i not in fake else 0 for i in right])
      if left_weight < right_weight:
        idx += 0
      elif left_weight == right_weight:
        idx += 1
      elif left_weight > right_weight:
        idx += 2
      else:
        print("Error")
        exit()
    buckets[idx] += 1
  if max(buckets) > pow(3, M-col-1):
    return False

  # All conditions met
  return True

# Initialize matrix
def init(N, M):
  matrix = []
  for _ in range(N):
    row = []
    for _ in range(M):
      row.append(-1)
    matrix.append(row)
  return matrix

# Fill column (i.e. pick a weighing)
def fill_col(matrix, col, state):
  N = len(matrix)
  if state == pow(3, N):
    for i in range(N):
      matrix[i][col] = -1
    return matrix, 1
  else:
    row_vec = num_to_vec(state, N)
    for i in range(N):
      matrix[i][col] = row_vec[i]
    return matrix, state + 1

def fill_matrix_by_column(matrix):
  N = len(matrix)
  M = len(matrix[0])

  col = 0
  states = [1] * N
  while 0 <= col and col < M:
    matrix, state = fill_col(matrix, col, states[col])
    states[col] = state
    if state == 1: # Backtrack
      col -= 1
      #print("Backtracking to column {0}".format(col))
    elif valid(matrix, col): # Proceed to next column
      col += 1
      #print("Proceeding to column {0}".format(col))
    else: # Try fill column again
      pass

  if col < 0: # No solution
    return None, False
  else:
    return matrix, True

def print_solution(matrix):
  N = len(matrix)
  M = len(matrix[0])

  for i in range(N):
    print(matrix[i])
  for j in range(M):
    left = [chr(i+65) for i in range(N) if matrix[i][j] == 1]
    right = [chr(i+65) for i in range(N) if matrix[i][j] == 2]
    weigh = ""
    for ball in left:
      weigh += ball
    weigh += "-"
    for ball in right:
      weigh += ball
    print(weigh)

def main(N, M):
  matrix = init(N, M)
  matrix, solvable = fill_matrix_by_column(matrix)
  if solvable:
    print_solution(matrix)
  else:
    print("No solution")

if __name__ == "__main__":
  N = int(sys.argv[1])
  M = int(sys.argv[2])
  main(N, M)

