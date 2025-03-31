
class Othello_Board:

    '''
    the othello game board is made up of 8 squares by 8 squares (64 in total)
    each square will either hold a white counter (W), a black counter (B) or be empty (e)
    each square is initialised to be empty

    an Othello_Board object can:

        - place pieces (black or white)
        - check if a space is free
        - find what piece is in a given position
        - flip a counter from one colour to the other
        - test if a given position is a valid place to put a piece

        - print itself, unpretty

        - test if a particular direction (vector) leads to a 'sandwich'
        - get all 'sandwich' directions of a given position (returned as a boolean array of 8 values - referring to 8 bearings starting from vertically up)

        - and MORE! :D
    '''

    def __init__(self):
        self.board_array = [['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e'],
                            ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e'],
                            ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e'],
                            ['e', 'e', 'e', 'B', 'W', 'e', 'e', 'e'],
                            ['e', 'e', 'e', 'W', 'B', 'e', 'e', 'e'],
                            ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e'],
                            ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e'],
                            ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e']]      

        #    compass directions:  N       NE       E      SE      S     SW     W      NW
        self.direction_array = [ [0,-1], [1,-1], [1,0], [1,1], [0,1], [-1,1], [-1,0], [-1, 1] ]

        #self.valid_moves = self.get_valid_positions()
        
        return

    # given the colour of the piece and position, place a piece on the board
    # this method does NOT check if there is already a piece in this position, or if this is a valid placement
    def place_piece(self, colour, x, y):
        if colour=='W' or colour=='white':
            self.board_array[y][x] = 'W'
        elif colour=='B' or colour=='black':
            self.board_array[y][x] = 'B'
        else:
            print("Error: counter colour must be 'W', 'white', 'B' or 'black'. '" + colour + "' is invalid")
        
        return

    # return true if a space is FREE (no counter)
    # return false if there is a counter in the space
    def is_space_free(self, x, y):
        if self.board_array[y][x] == 'e':
            return True
        else:
            return False
        

    # given the position, return the type of piece at that space
    def get_piece(self, x, y):
        if self.valid_coords(x, y):
            return self.board_array[y][x]
        else:
            print("Error, trying to access space not on board. x="+x+", y="+y)

        return 'e'


    # flip the counter (B -> W  or  W -> B) at a given position
    def flip(self, x, y):

        if self.board_array[y][x]=='W':
            self.board_array[y][x] = 'B'

        elif self.board_array[y][x]=='B':
            self.board_array[y][x] = 'W'

        else:
            print("Error, trying to flip counter at empty space: x=" + x + ", y=" + y)
        
        return
    

    # print the game board
    def print_board(self):

        print("\t0_____\t1_____\t2_____\t3_____\t4_____\t5_____\t6_____\t7_____")

        for row_index in range(len(self.board_array)):
            
            print(str(row_index) + " | \t" + self.board_array[row_index][0] + "\t" + self.board_array[row_index][1]
                                 + "\t" + self.board_array[row_index][2] + "\t" + self.board_array[row_index][3] 
                                 + "\t" + self.board_array[row_index][4] + "\t" + self.board_array[row_index][5]
                                 + "\t" + self.board_array[row_index][6] + "\t" + self.board_array[row_index][7])


    # return true if given coordinates are valid
    def valid_coords(self, x, y):
        return (x >= 0 and y >= 0 and x <= 7 and y <= 7)


    # return an array of boolean values, each corresponding to whether a particular direction leads to a sandwich
    #    returns an array of only false if there is already a piece at this location
    def get_sandwich_directions(self, x, y, colour):

        # compass directions:  N    NE     E      SE     S     SW      W     NW
        bool_directions = [False, False, False, False, False, False, False, False]

        if not self.is_space_free(x, y):
            return bool_directions

        # check if there is at least 1 sandwich forms (indirectly checking for at least 1 immediate neighbour)
        for direction_index in range(len(self.direction_array)):
            if self.direction_makes_sandwich(colour, x, y, self.direction_array[direction_index]):
                bool_directions[direction_index] = True
            
        return bool_directions


    # return true if it's possible to make a sandwich from the given position
    # method is used by get_valid_positions(colour)
    def sandwich_possible(self, x, y, colour):
        #colour = self.board_array[y][x]

        # check if there is at least 1 sandwich forms
        for direction_index in range(len(self.direction_array)):
            if self.direction_makes_sandwich(colour, x, y, self.direction_array[direction_index]):
                return True
        
        return False


    '''
    checks if a sandwich is made from a given position and a given direction
    bread_colour refers to the colour of the two outer counters of the sandwich
    direction = [x, y]   where x and y are either 0, 1 or -1

    method is used by:
        - sandwich_possible(x,y,colour)
        - get_sandwich_directions(x,y,colour)
    '''
    def direction_makes_sandwich(self, bread_colour, current_x, current_y, direction):
        
        filling_found = False
        bread_found = False
        next_x = current_x + direction[0]
        next_y = current_y + direction[1]

        while self.valid_coords(next_x, next_y):
            current_piece = self.get_piece(next_x, next_y)

            # empty space, so no sandwich
            if current_piece=='e':
                return False
            
            # filling of sandwich found
            elif (bread_colour=='B' and current_piece=='W') or (bread_colour=='W' and current_piece=='B'):
                filling_found = True
            
            else:
                bread_found = True
                if not filling_found:
                    return False

            if bread_found and filling_found:
                return True

            next_x = next_x + direction[0]
            next_y = next_y + direction[1]

        return False


    # get all valid positions to place a piece of given colour
    def get_valid_positions(self, colour):
        position_array = []

        for row_index in range(8):
            
            for piece_index in range(8):
                
                if (self.sandwich_possible(piece_index, row_index, colour)):
                    valid_coord = [piece_index, row_index]
                    position_array.append(valid_coord)
        
        return position_array
    

    # from a given position and colour, flip a line of pieces
    # this assumes that the line has already been verified
    def flip_line(self, start_x, start_y, bread_colour, direction):
        
        bread_found = False
        next_x = start_x + direction[0]
        next_y = start_y + direction[1]
        
        while self.valid_coords(next_x, next_y):
            current_piece = self.get_piece(next_x, next_y)

            # empty space, so no sandwich
            if current_piece=='e':
                print("Error: trying to flip with empty piece")
                return

            if (current_piece==bread_colour):
                return

            if (bread_colour=='B' and current_piece=='W') or (bread_colour=='W' and current_piece=='B'):
                self.flip(next_x, next_y)

            next_x = next_x + direction[0]
            next_y = next_y + direction[1]

        return


    # place a piece, and flip all necessary filler pieces
    def place_and_flip(self, x, y, colour):
        bool_directions = self.get_sandwich_directions(x,y,colour)
        direction_index = 0

        self.place_piece(colour, x, y)

        for direction in bool_directions:

            # if the direction makes a sandwich
            if direction:
                self.flip_line(x, y, colour, self.direction_array[direction_index])

            direction_index = direction_index + 1
        
        return