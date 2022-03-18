import sys; args = sys.argv[1:]
puzzles = open(args[0], "r").read().splitlines()
import time

      
def solve(puzzle, neighbors):
   variables, puzzle = initialize_ds(puzzle, neighbors)  
   return recursive_backtracking(puzzle, variables, neighbors)

def recursive_backtracking(assignment, variables, neighbors):
   if "." not in assignment:
      return assignment
   
   var_index = min([(len(v), k) for k,v in variables.items()])[1]
   for number in variables[var_index]:
      assignment_copy = assignment[:var_index] + number + assignment[var_index+1:]
      variables_copy = { k:{x for x in v} for k, v in variables.items() }
      variables_copy.pop(var_index)
      for x in neighbors[var_index]:
         if x in variables_copy and number in variables_copy[x]:
            variables_copy[x].remove(number)
      result = recursive_backtracking(assignment_copy, variables_copy, neighbors)
      if result != None: return result
   return None

def sudoku_csp(n=9):
   csp_table = []
   for i in range(9):
      csp_table.append([x for x in range(i*9,(i+1)*9)])
   for i in range(9):
      csp_table.append([i+x*9 for x in range(9)])
   temp = [0,1,2,9,10,11,18,19,20]
   csp_table += [[i+k for k in temp] for i in [0,3,6,27,30,33,54,57,60]]
   return csp_table

def sudoku_neighbors(csp_table):
   neighbors = {k:set() for k in range(81)}
   for k in neighbors:
      for table in csp_table:
         if k in table:
            for value in table:
               neighbors[value].add(k)
   return neighbors

def initialize_ds(puzzle, neighbors):
   variables={}
   for var_index in range(81):
       if puzzle[var_index]==".":
           l = [str(x) for x in range(1, 10)]
           for neighbor in neighbors[var_index]:
              if puzzle[neighbor] in l:
                 l.remove(puzzle[neighbor])
           variables[var_index]=l
   return variables, puzzle

def display(solution):
    s = ""
    for i in range(27):
      s += solution[i*3:(i+1)*3]
      s += " "
      if (i+1)%3==0 and i!=0:
         s += '\n'
      if (i+1)%9==0 and i!=0:
         s += '\n'
    return s

# sum of all ascii code of each char - (length of the solution * ascii code of min char)
def checksum(solution):
   return sum([ord(i) for i in solution]) - ord('1')*81

def main():
   csp_table = sudoku_csp() 
   neighbors = sudoku_neighbors(csp_table)
   start_time = time.time()
   for line, puzzle in enumerate(puzzles):
      line, puzzle = line+1, puzzle.rstrip()
      print ("{}: {}".format(line, puzzle)) 
      solution = solve(puzzle, neighbors)
      if solution == None:print ("No solution found."); break
      print ("{}{} {}".format(" "*(len(str(line))+2), solution, checksum(solution)))
   print ("Duration:", (time.time() - start_time))

if __name__ == '__main__': main()
