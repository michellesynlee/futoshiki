"""
Each futoshiki board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8

Empty values in the board are represented by 0

An * after the letter indicates the inequality between the row represented
by the letter and the next row.
e.g. my_board['A*1'] = '<'
means the value at A1 must be less than the value
at B1

Similarly, an * after the number indicates the inequality between the
column represented by the number and the next column.
e.g. my_board['A1*'] = '>' 
means the value at A1 is greater than the value
at A2

Empty inequalities in the board are represented as '-'

"""
import sys
import numpy as np
import time
#======================================================================#
#*#*#*# Optional: Import any allowed libraries you may need here #*#*#*#
#======================================================================#

#=================================#
#*#*#*# Your code ends here #*#*#*#
#=================================#

ROW = "ABCDEFGHI"
COL = "123456789"

class Board:
    '''
    Class to represent a board, including its configuration, dimensions, and domains
    '''
    def get_board_dim(self, str_len):
        '''
        Returns the side length of the board given a particular input string length
        '''
        d = 4 + 12 * str_len
        n = (2+np.sqrt(4+12*str_len))/6
        if(int(n) != n):
            raise Exception("Invalid configuration string length")
        
        return int(n)
        
    def get_config_str(self):
        '''
        Returns the configuration string
        '''
        return self.config_str
        
    def get_config(self):
        '''
        Returns the configuration dictionary
        '''
        return self.config
        
    def get_variables(self):
        '''
        Returns a list containing the names of all variables in the futoshiki board
        '''
        variables = []
        for i in range(0, self.n):
            for j in range(0, self.n):
                variables.append(ROW[i] + COL[j])
        return variables
    
    def convert_string_to_dict(self, config_string):
        '''
        Parses an input configuration string, retuns a dictionary to represent the board configuration
        as described above
        '''
        config_dict = {}

        for i in range(0, self.n):
            #print("i = ", i)
            for j in range(0, self.n):
                cur = config_string[0]
                config_string = config_string[1:]
                #print("[j = ", j)
                config_dict[ROW[i] + COL[j]] = int(cur)
                if(j != self.n - 1):
                    #print("in j, j is: ", j)
                    #print("self.n - 1 is: ", (self.n - 1))
                    cur = config_string[0]
                    config_string = config_string[1:]
                    #add conditions here so that not all of them have * after
                    #print("cur in j = ", cur)
                    config_dict[ROW[i] + COL[j] + '*'] = cur
                    
            if(i != self.n - 1):
                for j in range(0, self.n):
                    cur = config_string[0]
                    config_string = config_string[1:]
                    #add conditions here so that not all of them have * in between
                    #print("cur in i = ", cur)
                    config_dict[ROW[i] + '*' + COL[j]] = cur
        #test
        #print(config_dict)

        return config_dict
        
    def print_board(self):
        '''
        Prints the current board to stdout
        '''
        #config_dict = self.config
        config_dict = self.convert_string_to_dict(self.config_str)
        #print("SO CONFIG DICT IS: ", config_dict)
        for i in range(0, self.n):
            for j in range(0, self.n):
                cur = config_dict[ROW[i] + COL[j]]
                if(cur == 0):
                    print('_', end=' ')
                else:
                    print(str(cur), end=' ')
                
                if(j != self.n - 1):
                    cur = config_dict[ROW[i] + COL[j] + '*']
                    if(cur == '-'):
                        print(' ', end=' ')
                    else:
                        print(cur, end=' ')
            print('')
            if(i != self.n - 1):
                for j in range(0, self.n):
                    cur = config_dict[ROW[i] + '*' + COL[j]]
                    if(cur == '-'):
                        print(' ', end='   ')
                    else:
                        print(cur, end='   ')
            print('')
    
    def __init__(self, config_string):
        '''
        Initialising the board
        '''
        self.config_str = config_string
        self.n = self.get_board_dim(len(config_string))
        if(self.n > 9):
            raise Exception("Board too big")
            
        self.config = self.convert_string_to_dict(config_string)
        self.domains = self.reset_domains()
        
        self.forward_checking(self.get_variables())
        
        
    def __str__(self):
        '''
        Returns a string displaying the board in a visual format. Same format as print_board()
        '''
        print("str")
        output = ''
        config_dict = self.config
        for i in range(0, self.n):
            for j in range(0, self.n):
                cur = config_dict[ROW[i] + COL[j]]
                if(cur == 0):
                    output += '_ '
                else:
                    output += str(cur)+ ' '
                
                if(j != self.n - 1):
                    cur = config_dict[ROW[i] + COL[j] + '*']
                    if(cur == '-'):
                        output += '  '
                    else:
                        output += cur + ' '
            output += '\n'
            if(i != self.n - 1):
                for j in range(0, self.n):
                    cur = config_dict[ROW[i] + '*' + COL[j]]
                    if(cur == '-'):
                        output += '    '
                    else:
                        output += cur + '   '
            output += '\n'
        return output
        
    def reset_domains(self):
        '''
        Resets the domains of the board assuming no enforcement of constraints
        '''
        domains = {}
        variables = self.get_variables()
        for var in variables:
            if(self.config[var] == 0):
                domains[var] = [i for i in range(1,self.n+1)]
            else:
                domains[var] = [self.config[var]]
                
        self.domains = domains
                
        return domains

def is_consistent(assignment, var, val, csp, boardDim):
    #print("is_consistent")
    #1. need to see if var satisfies row constraints:
        #See if its an A, cross reference with all A vars? if keys are valid ur food
    #2. need to see if var satisfies column constraints:
        #See if var A1

    #row and column constraints. making sure (var, val) is not already repeated in dict csp row or column
    #extracts var from (var, val) tuple converted string using slicing
    str_var = str(var)
    if '*' in str_var:
        str_var = str_var[2:5]
    str_var = str_var[2:4]
    str_val = str(val)
    # first character: A, B, C
    row = str_var[0]
    # second character: 1, 2, 3
    if '*' == str_var[1]:
        col = str_var[2]
    else:
        col = str_var[1]
    #row constraint
    #for csp_var, csp_val in csp.items():
    for csp_var, csp_val in assignment.items():
        if (csp_var[0] == row) and (csp_var != str_var) and (str(csp_val) == str_val):
            return False  # value already exists in this row
    #column constraint
    for csp_var, csp_val in assignment.items():
        #if csp_var[1] == '1' or csp_var[1] == '2' or csp_var[1] == '3':
        if (csp_var[1] == col) and (csp_var != str_var) and (str(csp_val) == str_val):
            return False # value already exists in this column
        #INEQUALITY CONSTRAINTS
        else:
            row_ineq = str_var + "*"
            col_ineq = row + "*" + col
            for c_var, c_val in csp.items():
                if c_var == row_ineq:
                    neighbor_row = chr(ord(row) + 1)
                    neighbor_var = neighbor_row + col
                    #print("neighbor_row", neighbor_row)
                    #print("neighbor_var", neighbor_var)
                    if neighbor_var in assignment:
                        neighbor_val = assignment[neighbor_var]
                        if c_val == '<' and not (val < neighbor_val):
                            return False
                        elif c_val == '>' and not (val > neighbor_val):
                            return False
                if c_var == col_ineq:
                    neighbor_col = str(int(col) + 1)
                    neighbor_var = row + neighbor_col
                    # print("neighbor_col", neighbor_col)
                    # print("neighbor_var", neighbor_var)
                    if neighbor_var in assignment:
                        neighbor_val = assignment[neighbor_var]
                        if c_val == '<' and not (val < neighbor_val):
                            return False
                        elif c_val == '>' and not (val > neighbor_val):
                            return False
    return True

def select_unassigned_variables(assignment, csp):
    #print("select_unassigned_variables")
    for key, val in csp.items():
        if val == 0:
            if key not in assignment:
                #print("selected unassigned variable (: ", key, val, ")")
                #return (key, val)
                return {key: val}
    return None

def ORDER_DOMAIN_VALUES(var, assignment, csp, boardDim):
    #print("boardDim:", list(range(1, boardDim + 1)))
    return list(range(1, boardDim + 1))

#move to actual config string thing
def config_string_board(csp, board, assignment):
    csp_string = ""
    for key, val in csp.items():
        if len(key) == 3:
            csp_string += val
        if len(key) == 2 and key in assignment:
            #print("assignment[key]: ", str(assignment[key]))
            csp_string += str(assignment[key])
    #print("csp string:", csp_string)
    board.config_str = csp_string
    return csp_string

def backtracking(csp, assignment, boardDim):
    '''
    Performs the backtracking algorithm to solve the board
    Returns only a solved board
    '''
    for key, val in csp.items():
        if val != 0 and len(key) == 2:
            #print("assigned variable (", key, ", ", val, ")")
            assignment[key] = int(val)
    #print("BACKTRACKING ALG")
    var = select_unassigned_variables(assignment, csp)
    if var is None:
        return assignment
    # for each value in ORDER _DOMAIN_VALUES (var, assignment, csp)
    domain_vals = ORDER_DOMAIN_VALUES(var, assignment, csp, boardDim)
    if not domain_vals:
        return None

    for val in domain_vals:
        if is_consistent(assignment, var, val, csp, boardDim):
            assignment[next(iter(var))] = val
            #assignment[var.key()] = val
            result = backtracking(csp, assignment, boardDim)
                if result is not None:
                    return result
            assignment.popitem()

    #check over inequalities
    #Update config string -> add a function at the end? conoverting dict to string and then assigning to string

    return None # Replace with return values
    
def solve_board(board):
    '''
    Runs the backtrack helper and times its performance.
    Returns the solved board and the runtime
    '''
    #parse = 0
    #print("WHAT IS BOARD:", board, "OHHH")
    assignment = {}
    start_time = time.time()
    boardDim = board.get_board_dim(len(board.get_config_str()))
    test = backtracking(board.convert_string_to_dict(board.get_config_str()), assignment, boardDim)
    end_time = time.time()
    time_taken = end_time - start_time
    config_string_board(board.convert_string_to_dict(board.get_config_str()), board, assignment)
    #config_string_assist(board.config, board, assignment)
    return board, time_taken # Replace with return values

def print_stats(runtimes):
    '''
    Prints a statistical summary of the runtimes of all the boards
    '''
    min = 100000000000
    max = 0
    sum = 0
    n = len(runtimes)

    for runtime in runtimes:
        sum += runtime
        if(runtime < min):
            min = runtime
        if(runtime > max):
            max = runtime

    mean = sum/n

    sum_diff_squared = 0

    for runtime in runtimes:
        sum_diff_squared += (runtime-mean)*(runtime-mean)

    std_dev = np.sqrt(sum_diff_squared/n)

    print("\nRuntime Statistics:")
    print("Number of Boards = {:d}".format(n))
    print("Min Runtime = {:.8f}".format(min))
    print("Max Runtime = {:.8f}".format(max))
    print("Mean Runtime = {:.8f}".format(mean))
    print("Standard Deviation of Runtime = {:.8f}".format(std_dev))
    print("Total Runtime = {:.8f}".format(sum))


if __name__ == '__main__':
    if len(sys.argv) > 1:

        # Running futoshiki solver with one board $python3 futoshiki.py <input_string>.
        print("\nInput String:")
        print(sys.argv[1])
        
        print("\nFormatted Input Board:")
        board = Board(sys.argv[1])
        board.print_board()
        
        solved_board, runtime = solve_board(board)

        print("\nSolved String:")
        print(solved_board.get_config_str())
        
        print("\nFormatted Solved Board:")
        solved_board.print_board()
        
        print_stats([runtime])

        # Write board to file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(solved_board.get_config_str())
        outfile.write('\n')
        outfile.close()

    else:
        # Running futoshiki solver for boards in futoshiki_start.txt $python3 futoshiki.py

        #  Read boards from source.
        src_filename = 'futoshiki_start.txt'
        try:
            srcfile = open(src_filename, "r")
            futoshiki_list = srcfile.read()
            srcfile.close()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        
        runtimes = []

        # Solve each board using backtracking
        for line in futoshiki_list.split("\n"):
            
            print("\nInput String:")
            print(line)
            
            print("\nFormatted Input Board:")
            board = Board(line)
            board.print_board()
            
            solved_board, runtime = solve_board(board)
            runtimes.append(runtime)
            
            print("\nSolved String:")
            print(solved_board.get_config_str())

            print("\nFormatted Solved Board:")
            solved_board.print_board()

            # Write board to file
            outfile.write(solved_board.get_config_str())
            outfile.write('\n')

        # Timing Runs
        print_stats(runtimes)
        
        outfile.close()
        print("\nFinished all boards in file.\n")
