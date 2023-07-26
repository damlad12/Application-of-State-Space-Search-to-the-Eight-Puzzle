# searcher.py (Final project)
#
# classes for objects that perform state-space search on Eight Puzzles  
#
# name: Damla Duendar
# email: damlad@bu.edu
#

import random
from state import *

class Searcher:
    """ A class for objects that perform random state-space
        search on an Eight Puzzle.
        This will also be used as a superclass of classes for
        other state-space search algorithms.
    """
 
    def __init__(self, depth_limit):
        """constructs a new Searcher object by initializing an attribute states for the 
        Searcher‘s list of untested states that is initialized to an empty list,
        an attribute num_tested that will keep track of how many states the Searcher tests;,
        an attribute depth_limit that specifies how deep in the state-space search tree the Searcher
        will go; it should be initialized to the value specified by the parameter depth_limit. 
        (A depth_limit of -1 will be used to indicate that the Searcher does not use a depth limit.)"""
        self.states = []
        self.num_tested = 0
        self.depth_limit = depth_limit
    
    def add_state(self, new_state):
        """takes a single State object called new_state and adds it to the Searcher‘s list 
        of untested states. """
        self.states += [new_state]
    
    def should_add(self, state):
        """takes a State object called state and returns True if the called Searcher 
        should add state to its list of untested states, and False otherwise."""
        
        if state.creates_cycle():
            return False
        elif self.depth_limit != -1 and state.num_moves > self.depth_limit:
            return False
        else:
            return True
    
    def add_states(self, new_states):
        """takes a list State objects called new_states, and that processes the elements of new_states
        one at a time and adds them to the Searcher's list of untested states"""
        for state in new_states:
            if self.should_add(state):
                self.add_state(state)  
                
                
    def next_state(self):
        """ chooses the next state to be tested from the list of 
        untested states at random, removing it from the list and returning it
        """
        s = random.choice(self.states)
        self.states.remove(s)
        return s
    
    def find_solution(self, init_state):
        """performs a full state-space search that begins at the specified initial 
        state init_state and ends when the goal state is found or when the Searcher 
        runs out of untested states."""
        
        self.add_state(init_state)
        while len(self.states) > 0:
            self.num_tested += 1
            s = self.next_state()
            if s.is_goal():
                return s
            else:
                self.add_states(s.generate_successors())
        
        return None
        
        
    def __repr__(self):
        """ returns a string representation of the Searcher object
            referred to by self.
        """
        # You should *NOT* change this method.
        s = type(self).__name__ + ': '
        s += str(len(self.states)) + ' untested, '
        s += str(self.num_tested) + ' tested, '
        if self.depth_limit == -1:
            s += 'no depth limit'
        else:
            s += 'depth limit = ' + str(self.depth_limit)
        return s




class BFSearcher(Searcher):
    
    def next_state(self):
        """ chooses the next state to be tested from the list of 
        untested states based on FIFO ordering, removing it from the list and returning it
        """
        s = self.states[0]
        self.states.remove(s)
        return s
    
class DFSearcher(Searcher):
    
    def next_state(self):
        """ chooses the next state to be tested from the list of 
        untested states based on LIFO ordering, removing it from the list and returning it
        """
        s = self.states[-1]
        self.states.remove(s)
        return s
def h0(state):
    """ a heuristic function that always returns 0 """
    return 0



def h1(state):
    """takes a State object called state, and that computes and returns an estimate 
    of how many additional moves are needed to get from state to the goal state that is equal
    to the number of misplaced tiles in the Board object associated with that state."""
    return state.board.num_misplaced()

def h3(state):
    """takes a State object called state, and that computes and returns the number
    of moves it would take the empty square to reach its final position, plus the number of
    misplaced tiles when only the empty square is in the final position."""
    return  -1 * (state.board.empty_final() - state.board.new_misplaced())
    
def h2(state):
    """computes the min number of moves that each numbered tile must make to end up in 
    its position in the final state"""
    return state.board.distance_to_final()
    
class GreedySearcher(Searcher):
    """ A class for objects that perform an informed greedy state-space
        search on an Eight Puzzle.
    """
   
    
    def __init__(self, heuristic):
        """ constructs a new GreedySearcher object."""
        super().__init__(-1)
        self.heuristic = heuristic
        
    def __repr__(self):
        """ returns a string representation of the GreedySearcher object
            referred to by self.
        """
   
        s = type(self).__name__ + ': '
        s += str(len(self.states)) + ' untested, '
        s += str(self.num_tested) + ' tested, '
        s += 'heuristic ' + self.heuristic.__name__
        return s
    
    def priority(self, state):
        """ computes and returns the priority of the specified state,
        based on the heuristic function used by the searcher
        """
        return -1 * self.heuristic(state)
    
    def add_state(self, state):
        """overrides the add_state method that is inherited from Searcher. Adds a sublist that is a
        [priority, state] pair to the list of untested states."""
        self.states += [[self.priority(state),state]]
    
    def next_state(self):
        """overrides (i.e., replaces) the next_state method that is inherited from Searcher.
        Chooses one of the states with the highest priority."""
        s = max(self.states)
        self.states.remove(s)
        return s[1]
        


class AStarSearcher(GreedySearcher):
    """A class for searcher objects that perform an informed A* search on an Eight Puzzle"""
    
    def priority(self, state):
        """ computes and returns the priority of the specified state,
        based on the heuristic function used by the searcher
        """
        return -1 * (self.heuristic(state) + state.num_moves)
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

 state.py
 Download
#
# state.py (Final project)
#
# A State class for the Eight Puzzle
#
# name: Damla Duendar
# email: damlad@bu.edu
#
# If you worked with a partner, put their contact info below:
# partner's name:
# partner's email:
#

from board import *

# the list of possible moves, each of which corresponds to
# moving the blank cell in the specified direction
MOVES = ['up', 'down', 'left', 'right']

class State:
    """ A class for objects that represent a state in the state-space 
        search tree of an Eight Puzzle.
    """
    ### Add your method definitions here. ###
    
    def __init__(self, board, predecessor, move):
        """ a constructor for a State object
            that initializes an attribute board that stores a reference to the Board object 
            associated with this state, as specified by the parameter board, an attribute 
            predecessor that stores a reference to the State object that comes before this 
            state in the current sequence of moves, as specified by the parameter predecessor,
            an attribute move that stores a string representing the move that was needed to 
            transition from the predecessor state to this state, as specified by the parameter move,
            and an attribute num_moves that stores an integer representing the number of 
            moves that were needed to get from the initial state (the state at the root of the tree)
            to this state.
        """
        self.board = board
        self.predecessor = predecessor
        self.move = move
        if self.predecessor == None:
            self.num_moves = 0
        else:
            self.num_moves = self.predecessor.num_moves + 1 
            
    def is_goal(self):
        """ returns True if the called State object is a goal state, and False otherwise."""
        return self.board.tiles == GOAL_TILES
    
    def generate_successors(self):
        """creates and returns a list of State objects for all successor states of the 
        called State object. """
        
        successors = []
        for move in MOVES:
            copy_board = self.board.copy()
            c = copy_board.move_blank(move)
            if c:
                successor = State(copy_board,self,move)  
                successors += [successor]
        return successors
        
    def print_moves_to(self):
        """prints the sequence of moves that lead from the initial state to the called State object
        (i.e., to self).""",
        if self.predecessor == None:
            print('initial state:')
            print(self.board)
        else:
            self.predecessor.print_moves_to()
            print ('move the blank', self.move + ':')
            print(self.board)

        
    def __repr__(self):
        """ returns a string representation of the State object
            referred to by self.
        """
        # You should *NOT* change this method.
        s = self.board.digit_string() + '-'
        s += self.move + '-'
        s += str(self.num_moves)
        return s
    
    def creates_cycle(self):
        """ returns True if this State object (the one referred to
            by self) would create a cycle in the current sequence of moves,
            and False otherwise.
        """
        # You should *NOT* change this method.
        state = self.predecessor
        while state != None:
            if state.board == self.board:
               return True
            state = state.predecessor
        return False

    def __gt__(self, other):
        """ implements a > operator for State objects
            that always returns True. This will be needed to break
            ties when we use max() on a list of [priority, state] pairs.
            If we don't have a > operator for State objects,
            max() will fail with an error when it tries to compare
            two [priority, state] pairs with the same priority.
        """
        # You should *NOT* change this method.
        return True
