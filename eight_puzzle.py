# eight_puzzle.py (Final project)
#
# driver/test code for state-space search on Eight Puzzles   
#
# name: Damla Duendar
# email: damlad@bu.edu
#


from searcher import *
from timer import *

def create_searcher(algorithm, param):
    """ a function that creates and returns an appropriate
        searcher object, based on the specified inputs. 
        inputs:
          * algorithm - a string specifying which algorithm the searcher
              should implement
          * param - a parameter that can be used to specify either
            a depth limit or the name of a heuristic function
        Note: If an unknown value is passed in for the algorithm parameter,
        the function returns None.
    """
    searcher = None
    
    if algorithm == 'random':
        searcher = Searcher(param)
    elif algorithm == 'BFS':
        searcher = BFSearcher(param)
    elif algorithm == 'DFS':
        searcher = DFSearcher(param)
    elif algorithm == 'Greedy':
        searcher = GreedySearcher(param)
    elif algorithm == 'A*':
        searcher = AStarSearcher(param)
    else:  
        print('unknown algorithm:', algorithm)

    return searcher

def eight_puzzle(init_boardstr, algorithm, param):
    """ a driver function for solving Eight Puzzles using state-space search
        inputs:
          * init_boardstr - a string of digits specifying the configuration
            of the board in the initial state
          * algorithm - a string specifying which algorithm you want to use
          * param - a parameter that is used to specify either a depth limit
            or the name of a heuristic function
    """
    init_board = Board(init_boardstr)
    init_state = State(init_board, None, 'init')
    searcher = create_searcher(algorithm, param)
    if searcher == None:
        return

    soln = None
    timer = Timer(algorithm)
    timer.start()
    
    try:
        soln = searcher.find_solution(init_state)
    except KeyboardInterrupt:
        print('Search terminated.')

    timer.end()
    print(str(timer) + ', ', end='')
    print(searcher.num_tested, 'states')

    if soln == None:
        print('Failed to find a solution.')
    else:
        print('Found a solution requiring', soln.num_moves, 'moves.')
        show_steps = input('Show the moves (y/n)? ')
        if show_steps == 'y':
            soln.print_moves_to()
            
            
def process_file(filename, algorithm, param):
    """takes as input a string filename specifying the name of a text file in which each
    line is a digit string for an eight puzzle, a string algorithm that specifies which state-space
    search algorithm should be used to solve the puzzles, and a third input param that is either a depth limit
     or a choice of heuristic function."""
     
    file = open(filename, 'r')
    
    num_moves_total = 0
    num_tested_total = 0
    solved_puzzles = 0
    
    for line in file:
        line = line[:-1]
        init_board = Board(line)
        init_state = State(init_board, None, 'init')
        searcher = create_searcher(algorithm, param)
        
        if searcher == None:
            return
        
        soln = None
        try:
            soln = searcher.find_solution(init_state)
            print(line + ': ', end='')
        except KeyboardInterrupt:
            print('search terminated, ', end='')
        if soln != None:
            print(soln.num_moves,'moves,',searcher.num_tested,'states','tested')
            num_tested_total += searcher.num_tested
            num_moves_total += soln.num_moves
            solved_puzzles += 1
        else: 
            print('no solution')
    print()        
    print('solved',solved_puzzles,'puzzles')
    
    if solved_puzzles != 0:
        print('averages:', num_moves_total / solved_puzzles,'moves,', num_tested_total / solved_puzzles , 'states','tested')
    file.close()
    
