import ttr_info as info
import ttr_classes as ttr
import pygame

game_map = ttr.Map(info.city_map,info.possible_tickets)

# Define some colors
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)
color_list = [red,green,blue,darkBlue,white,black,pink]
height = width = 19
margin = 6
thickness = 1
rect_color = black
num_pressed = 0
x_scale = 18
y_scale = 18
num_rows = 28
num_cols = 54

pygame.init()

# Set the width and height of the screen [width, height]
size = (1700,706)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Ticket To Ride Visualization")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()


def get_cities():
    cities = set()
    for city in game_map.nodes:
        cities.add(game_map.nodes[city].pixel)
    return cities

def get_roads():
    roads = []
    for city in game_map.city_map:
        start_x = width*game_map.nodes[city].pixel[0] + margin*(game_map.nodes[city].pixel[0]+1) + width/2
        start_y = height*game_map.nodes[city].pixel[1] + margin*(game_map.nodes[city].pixel[1]+1) + height/2
        for dest in game_map.city_map[city]:
            end_x = width*game_map.nodes[dest].pixel[0] + margin*(game_map.nodes[dest].pixel[0]+1) + width/2
            end_y = height*game_map.nodes[dest].pixel[1] + + margin*(game_map.nodes[dest].pixel[1]+1) + height/2
            roads.append([(start_x,start_y),(end_x,end_y)])
    return roads

def draw_roads(added_lines):
    for i in get_roads():
        pygame.draw.lines(screen, black, False, i, 3) 

    for i in added_lines:
        if type(i) == list:
            pygame.draw.lines(screen, green, False, i, 3)

def better_map():
    cities = get_cities()
    for col in range(num_cols):
        for row in range(num_rows):
            pygame.draw.rect(screen,black,(width*col+margin*(col+1),height*row+margin*(row+1),width,height),thickness)

    for city in game_map.nodes:
        x = game_map.nodes[city].pixel[0]
        y = game_map.nodes[city].pixel[1]
        pygame.draw.rect(screen,red,(width*x+margin*(x+1),height*y+margin*(y+1),width,height),0)
        fontObj = pygame.font.Font('freesansbold.ttf', height-1)
        textSurfaceObj = fontObj.render(city, True, white, black)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.topleft = (width*(x+1)+margin*(x+1),height*y+margin*(y+1))
        screen.blit(textSurfaceObj, textRectObj)

def check_mouse(pos):
    for city in game_map.nodes:
        x = game_map.nodes[city].pixel[0]
        y = game_map.nodes[city].pixel[1]
        if ((pos[0] - (width*x+margin*(x+1)))**2 + (pos[1] - (height*y+margin*(y+1)))**2)**0.5 < 20:
            pygame.draw.rect(screen,green,(width*x+margin*(x+1),height*y+margin*(y+1),width,height),0)
            fontObj = pygame.font.Font('freesansbold.ttf', height-1)
            textSurfaceObj = fontObj.render(city, True, black, white)
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.topleft = (width*(x+1)+margin*(x+1),height*y+margin*(y+1))
            screen.blit(textSurfaceObj, textRectObj)
            return city
    return False

def use_road(current_road):
    start = current_road[0]
    end = current_road[1]

    if end in game_map.nodes[start].adj_list:
        game_map.remove_edge((start,end))
        start_x = width*game_map.nodes[start].pixel[0] + margin*(game_map.nodes[start].pixel[0]+1) + width/2
        start_y = height*game_map.nodes[start].pixel[1] + margin*(game_map.nodes[start].pixel[1]+1) + height/2
        end_x = width*game_map.nodes[end].pixel[0] + margin*(game_map.nodes[end].pixel[0]+1) + width/2
        end_y = height*game_map.nodes[end].pixel[1] + + margin*(game_map.nodes[end].pixel[1]+1) + height/2
        print(current_road)
        return [(start_x,start_y),(end_x,end_y)]

    return



cities = get_cities()
current_road = []
added_lines = []
# -------- Main Program Loop -----------
while not done:
    screen.fill(white)
# --- Main event loop
    for event in pygame.event.get(): # User did something
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop


        if event.type == pygame.MOUSEBUTTONUP and check_mouse(pos):
            if len(current_road) == 1:
                current_road.append(check_mouse(pos))
                added_lines.append(use_road(current_road))
                current_road = []
            elif len(current_road) == 0:
                
                current_road.append(check_mouse(pos))

                

    
    draw_roads(added_lines)
    better_map()
    check_mouse(pos)
    




    fontObj = pygame.font.Font('freesansbold.ttf', 19)
    textSurfaceObj = fontObj.render("Mouse Pos: " + str(pos), True, white, black)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.topleft = (1360,6)
    screen.blit(textSurfaceObj, textRectObj)

    fontObj = pygame.font.Font('freesansbold.ttf', 14)
    textSurfaceObj = fontObj.render("Current Road: " + str(current_road), True, white, black)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.topleft = (1360,6+19*1)
    screen.blit(textSurfaceObj, textRectObj)


    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.update()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()

