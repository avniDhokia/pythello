# Example file showing a circle moving on screen
import pygame
import time
from Othello_Board import Othello_Board
import random

# sizing variables
board_square_length = 70
counter_radius = 30
between_squares_length = 10
total_board_length = (8*counter_radius*2) + (10*between_squares_length)

# game variables
board_colour = pygame.Color(22,201,50)
valid_square_colour = pygame.Color(200, 255, 0)
highlight_square_colour = pygame.Color(255, 140, 0)
empty_piece_colour =pygame.Color(22,153,41)
board = Othello_Board()
player_colour = 'W'
computer_colour = 'B'


# pygame setup
pygame.init()

screen = pygame.display.set_mode((total_board_length*1.75, total_board_length+2*between_squares_length))
clock = pygame.time.Clock()
running = True
dt = 0

game_open = True
computer_turn = True

# render the pygame board
def render_board(board, screen, board_square_length, radius, between_squares_length, empty_piece_colour, valid_piece_colour, valid_positions):
    colour = "green"

    for row_index in range(8):
        
        for piece_index in range(8):

            piece = board.get_piece(piece_index, row_index)
            colour = "green"

            if piece=='B':
                colour = "black"
            elif piece == 'W':
                colour = "white"
            elif computer_turn:
                colour = empty_piece_colour
            else:
                # it's the player's turn and it's an empty square

                # is this square a valid move
                if (piece_in_valid_moves(piece_index, row_index, valid_positions)):
                    colour = valid_piece_colour

                    # find where the mouse is hovering
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    mouse_over_piece = False
                    x_coord, y_coord = get_circle_center(piece_index, row_index, between_squares_length, board_square_length)

                    if point_within_circle(mouse_x, mouse_y, x_coord, y_coord, counter_radius):
                        colour = highlight_square_colour

                else:
                    colour = empty_piece_colour

            x, y = get_circle_center(piece_index, row_index, between_squares_length, board_square_length)

            drawCircle(screen, x, y, colour, radius)
    
    return

# given x [0 to 7] and y [0 to 7] coordinates, and an array of valid positions, check if [x, y] is a valid position
def piece_in_valid_moves(x, y, valid_positions):
    for pos in valid_positions:
        if (pos[0] == x) and (pos[1] == y):
            return True

    return False

# given the board coordinates, lengths between squares and the length of a board square, return the circle center coordinates in terms of pixels
def get_circle_center(x, y, between_squares_length, board_square_length):
    x_coord = (2*between_squares_length) + (x*board_square_length) + board_square_length/2
    y_coord = (2*between_squares_length) + (y*board_square_length) + board_square_length/2

    return x_coord, y_coord


# computer's turn
def take_computer_turn(board, colour):
    time.sleep(1)
    valid_positions = board.get_valid_positions(colour)

    if len(valid_positions) == 0:
        print("computer can't place anything!")
        return board

    index = random.randint(0, len(valid_positions)-1)

    chosen_pos = valid_positions[index]
    board.place_and_flip(chosen_pos[0], chosen_pos[1], colour)

    print("Computer placed at x=" + str(chosen_pos[0]) + ", y=" + str(chosen_pos[1]))
    return board

# is a point [x, y] within a circle of given radius and center [circle_x, circle_y]?
def point_within_circle(x, y, circle_x, circle_y, radius):
    distance_squared = (x-circle_x)**2 + (y-circle_y)**2
    return (distance_squared <= radius**2)

# given a surface, x and y coords, colour and radius, draw a circle
def drawCircle(surface, x, y, colour, radius):
    placement_vector = pygame.Vector2(x, y)
    pygame.draw.circle(screen, colour, placement_vector, radius)


while game_open:

    # set the screen background
    screen.fill("black")

    # draw othello board
    board_surface = pygame.Rect(between_squares_length, between_squares_length, total_board_length, total_board_length) 
    pygame.draw.rect(screen, board_colour, board_surface)

    valid_positions = board.get_valid_positions(player_colour)

    # render the board with pieces
    render_board(board, screen, board_square_length, counter_radius, between_squares_length, empty_piece_colour, valid_square_colour, valid_positions)
    pygame.display.flip()



    while running:

        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        # if it's the computer's turn, let the computer do its move
        if computer_turn:
            board = take_computer_turn(board, computer_colour)
            computer_turn = False

        else:
            # the player can take their turn
            valid_positions = board.get_valid_positions(player_colour)

            if len(valid_positions) > 0:

                # process if the player clicks
                if pygame.mouse.get_pressed()[0] and not computer_turn:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    for pos in valid_positions:
                        x_coord, y_coord = get_circle_center(pos[0], pos[1], between_squares_length, board_square_length)

                        if point_within_circle(mouse_x, mouse_y, x_coord, y_coord, counter_radius):

                            board.place_and_flip(pos[0], pos[1], player_colour)
                            
                            computer_turn = True
                            break

            else:
                computer_turn = True


        # render the board with pieces
        render_board(board, screen, board_square_length, counter_radius, between_squares_length, empty_piece_colour, valid_square_colour, valid_positions)


        # flip() the display to put your work on screen
        pygame.display.flip()


pygame.quit()
