import ttr_info as info
import ttr_classes as ttr
import pygame
pygame.init()
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)

# Set the width and height of the screen [width, height]
size = (600,800)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Setup")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

def display_list(pos, possible_tickets, taken_tickets):
    counter = 0
    for i in possible_tickets:
        fontObj = pygame.font.Font('freesansbold.ttf', 19)
        textSurfaceObj = fontObj.render("Mouse Pos: " + str(i), True, white, black)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.topleft = (10,10 + 24*counter)   
        if pos[0] >= textRectObj[0] and pos[0] <= textRectObj[2] and pos[1] >= textRectObj[1] and pos[1] <= textRectObj[3]:
            textSurfaceObj = fontObj.render("Mouse Pos: " + str(i), True, white, black)
        else:
            textSurfaceObj = fontObj.render("Mouse Pos: " + str(i), True, black,white)
        textRectObj = textSurfaceObj.get_rect()
        screen.blit(textSurfaceObj, textRectObj)
        
        
        counter += 1
    return taken_tickets

def check_mouse_setup(pos, rects, taken_tickets):
    for i in rects:
        if pos[0] >= textRectObj[0] and pos[0] <= textRectObj[2] and pos[1] >= textRectObj[1] and pos[1] <= textRectObj[3]:
            taken_tickets.add(i[0])
    return taken_tickets

taken_tickets = set()
while not done:
    screen.fill(white)
# --- Main event loop

    for event in pygame.event.get(): # User did something
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
        
        if event.type == pygame.MOUSEBUTTONUP:
            taken_tickets = display_list(pos,info.possible_tickets,taken_tickets)


    taken_tickets = display_list(pos,info.possible_tickets, taken_tickets)


    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.update()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()