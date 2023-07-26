# board.py (Final project)
#
# A Board class for the Eight Puzzle
#
# name: Damla Duendar
# email: damlad@bu.edu
#
# If you worked with a partner, put their contact info below:
# partner's name:
# partner's email:
#

# a 2-D list that corresponds to the tiles in the goal state
GOAL_TILES = [['0', '1', '2'],
              ['3', '4', '5'],
              ['6', '7', '8']]

class Board:
    """ A class for objects that represent an Eight Puzzle board.
    """
    def __init__(self, digitstr):
        """ a constructor for a Board object whose configuration
            is specified by the input digitstr
            input: digitstr is a permutation of the digits 0-9
        """
        # check that digitstr is 9-character string
        # containing all digits from 0-9
        assert(len(digitstr) == 9)
        for x in range(9):
            assert(str(x) in digitstr)

        self.tiles = [[''] * 3 for x in range(3)]
        self.blank_r = -1
        self.blank_c = -1
        
        
        # Put your code for the rest of __init__ below.
        # Do *NOT* remove our code above.
        for r in range(len(digitstr)//3):
            for c in range(len(digitstr)//3):
                self.tiles[r][c] = digitstr[3*r+c]
                if self.tiles[r][c] == '0':
                    self.blank_r = r
                    self.blank_c = c
    
            
    ### Add your other method definitions below. ###
    def __repr__(self):
        """returns a string representation of a Board object where each tile is represented 
        by the appropriate single-character string followed by a single space and the blank cell 
        is represented by an underscore character and the rows are on separate lines.  """
        
                
        string_board = ''
        for r in range(len(self.tiles)):
            for c in range(len(self.tiles[0])):
                tile_string = self.tiles[r][c]
                if tile_string == '0':
                    tile_string = '_'
                string_board += str(tile_string+ ' ')
                if c == 2:
                    string_board += '\n'
        return string_board
    
    
    def move_blank(self, direction):
        """takes as input a string direction that specifies the direction in 
        which the blank should move, and that attempts to modify the contents
        of the called Board object accordingly."""
        
        if direction not in ['up','down','left','right']:
            return False

        
        r_blank = self.blank_r
        c_blank = self.blank_c
        
        if direction == 'up':
            r_blank = self.blank_r - 1
        elif direction == 'down':
            r_blank = self.blank_r + 1
        elif direction == 'right':
            c_blank = self.blank_c + 1
        elif direction == 'left':
            c_blank = self.blank_c - 1

        
        if not(0<=r_blank<=2 and 0<=c_blank<=2):
            return False
        
        else:
            self.tiles[self.blank_r][self.blank_c] = self.tiles[r_blank][c_blank]
            self.tiles[r_blank][c_blank] = '0'
            self.blank_r = r_blank
            self.blank_c = c_blank
            return True
        
        
        
    def  digit_string(self):
        """creates and returns a string of digits that corresponds to the current 
        contents of the called Board object’s tiles attribute."""
        string_digits = ''
        for r in range(len(self.tiles)):
            for c in range(len(self.tiles[0])):
                string_digits += self.tiles[r][c]
        return string_digits
        
    
    def copy(self):
        """returns a newly-constructed Board object that is a deep copy of the called 
        object (i.e., of the object represented by self)."""
        deep_copy = Board(self.digit_string())
        return deep_copy
        
    def num_misplaced(self):
        """counts and returns the number of tiles in the called Board object that are
        not where they should be in the goal state."""
        num_misplaced = 0
        for r in range(3):
            for c in range(3):
                if not (self.tiles[r][c]==GOAL_TILES[r][c]) and not(self.tiles[r][c] == '0'):
                    num_misplaced += 1
        return num_misplaced
        
    def __eq__(self, other):
        """returns True if the called object (self) and the argument 
        (other) have the same values for the tiles attribute, and False otherwise."""
        return self.tiles == other.tiles

    def empty_final(self):
        return self.blank_r + self.blank_c
    
    def new_misplaced(self):
        blank_row = ''
        for r in range(3):
            for c in range(3):
                if self.digit_string()[3*r+c] == '0':
                    if  r>0:
                        if self.copy().tiles[1][c]== '0':
                            self.copy().tiles[1][c] = self.copy().tiles[0][c]
                            self.copy().tiles[0][c] ='0'
                            blank_row = '0'
                        else:
                            self.copy().tiles[2][c] = self.copy().tiles[1][c]
                            self.copy().tiles[1][c] = self.copy().tiles[0][c]
                            self.copy().tiles[0][c] = '0'
                            blank_row = '0'
                            
                    if  3*r+c == 0:
                        break
                    
                    if blank_row== '0' or r == 0:
                            if self.copy().tiles[0][1]== '0':
                                self.copy().tiles[0][1]= self.copy().tiles[0][0]
                                self.copy().tiles[0][0]= '0'
                                break
                            if self.copy().tiles[0][2] == '0':
                                self.copy().tiles[0][2] = self.copy().tiles[0][1]
                                self.copy().tiles[0][1] = self.copy().tiles[0][0]
                                self.copy().tiles[0][0]= '0'
                                break
        
        return self.copy().num_misplaced()
    
    def distance_to_final(self):
        """computes the distance between the current location of the tiles in the board and their final 
        location"""
        distance = 0

        for r in range(3):
             for c in range(3):
               if self.tiles[r][c] != 0 and self.tiles[r][c] != GOAL_TILES[r][c]:
                   if self.tiles[r][c] == '1':
                      distance +=  abs(r-0) + abs(c-1)
                   if self.tiles[r][c] == '2':
                       distance += abs(r-0) + abs(c-2)
                   if self.tiles[r][c] == '3':
                       distance += abs(r-1) + abs(c-0)
                   if self.tiles[r][c] == '4':
                       distance += abs(r-1) + abs(c-1)
                   if self.tiles[r][c] == '5':
                       distance += abs(r-1) + abs(c-2)
                   if self.tiles[r][c] == '6':
                       distance += abs(r-2) + abs(c-0)
                   if self.tiles[r][c] == '7':
                       distance += abs(r-2) + abs(c-1)
                   if self.tiles[r][c] == '8':
                       distance += abs(r-2) + abs(c-2)
                       
        return distance
                       
    
 
                  
