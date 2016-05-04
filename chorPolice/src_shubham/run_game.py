import pygame
from Game import Game
from docutils.nodes import row
 
# Define some colors
BLANK = (255, 255, 255)
WALL = (0, 0, 0)
colors = [(0, 255, 0), (51, 51, 255), (255, 0, 128), (255, 0, 0), (255, 255, 100), (0, 0, 255)]

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 20
HEIGHT = 20
 
# This sets the margin between each cell
MARGIN = 5
 
# Initialize pygame
pygame.init()
 
# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [800, 400]
screen = pygame.display.set_mode(WINDOW_SIZE)
 
# Set title of screen
pygame.display.set_caption("Chor Police")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the Game
game = Game("arena.txt")
id_chor = game.init_player((1, 1), "chor")
id_police1 = game.init_player((5,7), "police")
id_police2 = game.init_player((7, 7), "police")
game.start_game()

# Initialize release status of key
released = True
 
# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Exit the loop
        
        elif event.type == pygame.KEYDOWN:
            if (released):
                released = False
                if event.key == pygame.K_LEFT:  # Left arrow key
                    game.move(game.current_turn, "left")
                elif event.key == pygame.K_RIGHT:
                    game.move(game.current_turn, "right")
                elif event.key == pygame.K_UP:
                    game.move(game.current_turn, "up")
                elif event.key == pygame.K_DOWN:
                    game.move(game.current_turn, "down")
                elif event.key == pygame.K_RETURN:
                    game.move(game.current_turn, "none")
 
        # User let up on a key
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or \
                event.key == pygame.K_DOWN or event.key == pygame.K_UP or \
                event.key == pygame.K_RETURN:
                released = True
 
    # Set the screen background
    screen.fill(BLANK)
 
    # Draw the grid
    for row in range(game.rows):
        for column in range(game.cols):
            if game.arena[row][column] == "x":
                pygame.draw.rect(screen,
                                 WALL,
                                 [(MARGIN + WIDTH) * column + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])

    # Draw players
    (row, column) = game.get_position(id_chor)
    pygame.draw.rect(screen, colors[0],
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])
    
    (row, column) = game.get_position(id_police1)
    pygame.draw.rect(screen, colors[1],
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])
    
    (row, column) = game.get_position(id_police2)
    pygame.draw.rect(screen, colors[2],
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT]) 
    
    # Limit to 60 frames per second
    clock.tick(60)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()

if __name__ == "__main__":
    print "Finish"