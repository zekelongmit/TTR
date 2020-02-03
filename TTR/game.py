import ttr_info as info
import ttr_classes as ttr
import pygame as pg
import math

game_map = ttr.Map(info.city_map,info.possible_tickets)
pg.init()
screen = pg.display.set_mode((1270,706))
FONT = pg.font.SysFont('Calibri', 20)
city_font = pg.font.SysFont('Calibri', 12)

### COLOR PALETTE ###
white = (255,255,255)
black = (0,0,0)
color_1 = (5,4,1) # black
color_2 = (48,48,54) # dark grey
color_3 = (48,188,237) # blue
color_4 = (255,250,255) # white
color_5 = (252,81,48) # red

red = (255, 0, 63)
green = (63, 255, 0)
blue = (0, 63, 255)
grey = (75,75,75)
yellow = (255, 192, 0)

background = color_1
normal_bakground = color_2
highlight_color = color_5
down_color = color_5
select_color = color_5

best_color = color_4
road_color = color_2
other_color = color_5
my_color = color_3

color_list = [green,red,blue,grey,yellow]
# Default button images/pygame.Surfaces.
IMAGE_NORMAL = pg.Surface((100, 20))
IMAGE_NORMAL.fill(normal_bakground)
IMAGE_HOVER = pg.Surface((100, 20))
IMAGE_HOVER.fill(highlight_color)
IMAGE_DOWN = pg.Surface((100, 20))
IMAGE_DOWN.fill(down_color)
IMAGE_SELECT = pg.Surface((100, 20))
IMAGE_SELECT.fill(select_color)


class City(pg.sprite.Sprite):

	def __init__(self, x, y, width, height, callback,
				 font = FONT, text = '', text_color = (0, 0, 0),
				 image_normal = IMAGE_NORMAL, image_hover = IMAGE_HOVER,
				 image_down = IMAGE_DOWN, selected = False):
		super().__init__()
		# Scale the images to the desired size (doesn't modify the originals).
		self.image_normal = pg.transform.scale(image_normal, (width, height))
		self.image_hover = pg.transform.scale(image_hover, (width, height))
		self.image_down = pg.transform.scale(image_down, (width, height))
		self.image_select = pg.transform.scale(IMAGE_SELECT, (width, height))
		self.width = width
		self.height = height
		self.pos = (x,y)
		self.x = x
		self.y = y
		self.text = text
		self.font = font
		self.text_color = text_color
		self.selected = selected
		if self.selected == False:
			self.image = self.image_normal  # The currently active image.
		if self.selected == True:
			self.image = self.image_select  # The currently active image.

		self.rect = self.image.get_rect(topleft = self.pos)
		self.image_center = self.image.get_rect().center

		self.text_surf = font.render(text, True, text_color)
		self.text_rect = self.text_surf.get_rect(center = self.image_center)
		# Blit the text onto the images.
		for image in (self.image_normal, self.image_hover, self.image_down):
			image.blit(self.text_surf, self.text_rect)

		# This function will be called when the button gets pressed.
		self.callback = callback
		self.button_down = False

	def handle_event(self, event):
		if event.type == pg.MOUSEBUTTONDOWN:
			if self.rect.collidepoint(event.pos):
				self.image = self.image_down
				self.button_down = True
		elif event.type == pg.MOUSEBUTTONUP:
			# If the rect collides with the mouse pos.
			if self.rect.collidepoint(event.pos) and self.button_down:
				self.callback(self.text)  # Call the function.
				self.image = self.image_hover
			self.button_down = False
		elif event.type == pg.MOUSEMOTION:
			collided = self.rect.collidepoint(event.pos)
			if collided and not self.button_down:
				self.image = self.image_hover
			elif not collided:
				self.image = self.image_normal


class Button(pg.sprite.Sprite):

	def __init__(self, x, y, width, height, callback,
				 font = FONT, text = '', text_color = (0, 0, 0),
				 image_normal = IMAGE_NORMAL, image_hover = IMAGE_HOVER,
				 image_down = IMAGE_DOWN, selected = False):
		super().__init__()
		# Scale the images to the desired size (doesn't modify the originals).
		self.image_normal = pg.transform.scale(image_normal, (width, height))
		self.image_hover = pg.transform.scale(image_hover, (width, height))
		self.image_down = pg.transform.scale(image_down, (width, height))
		self.image_select = pg.transform.scale(IMAGE_SELECT, (width, height))
		self.width = width
		self.height = height
		self.pos = (x,y)
		self.x = x
		self.y = y
		self.text = text
		self.font = font
		self.text_color = text_color
		self.selected = selected
		if self.selected == False:
			self.image = self.image_normal  # The currently active image.
		if self.selected == True:
			self.image = self.image_select  # The currently active image.

		self.rect = self.image.get_rect(topleft = self.pos)
		self.image_center = self.image.get_rect().center
		self.text_surf = font.render(text, True, text_color)
		self.text_rect = self.text_surf.get_rect(center=self.image_center)
		# Blit the text onto the images.
		for image in (self.image_normal, self.image_hover, self.image_down):
			image.blit(self.text_surf, self.text_rect)

		# This function will be called when the button gets pressed.
		self.callback = callback
		self.button_down = False

	def handle_event(self, event):
		if event.type == pg.MOUSEBUTTONDOWN:
			if self.rect.collidepoint(event.pos):
				self.image = self.image_down
				self.button_down = True
		elif event.type == pg.MOUSEBUTTONUP:
			# If the rect collides with the mouse pos.
			if self.rect.collidepoint(event.pos) and self.button_down:
				self.callback(self.text)  # Call the function.
				self.image = self.image_hover
			self.button_down = False
		elif event.type == pg.MOUSEMOTION:
			collided = self.rect.collidepoint(event.pos)
			if collided and not self.button_down:
				self.image = self.image_hover
			elif not collided:
				self.image = self.image_normal

class Game:

	def __init__(self, screen):
		self.done = False
		self.clock = pg.time.Clock()
		self.screen = screen
		self.setup = True
		self.screen_height = screen.get_height()
		self.screen_width = screen.get_width()
		self.other_lines = []
		self.other_lines_colors = []
		self.my_lines = []
		self.game_map = game_map
		self.height = 19
		self.width = 19
		self.margin = 3
		self.best_path_roads = []
		self.player_number = 0
		self.selected_tickets = set()
		self.current_road = []
		# Contains all sprites. Also put the button sprites into a
		# separate group in your own game.
		
		self.button_sprites = self.get_buttons(info.possible_tickets)
		self.city_sprites = self.get_cities(self.game_map.city_map)
		self.city_buttons = self.get_city_buttons()
		self.info_buttons = self.get_info_button()
		self.all_sprites = pg.sprite.Group()
		# Add the button sprites to the sprite group.
		for button in self.button_sprites:
			self.all_sprites.add(button)
		for city in self.city_sprites:
			self.all_sprites.add(city)
		for button in self.city_buttons:
			self.all_sprites.add(button)
		for information in self.info_buttons:
			self.all_sprites.add(information)

		

	def get_cities(self, city_map):
		box_width = 75
		box_height = 14
		num_cols = 56
		num_rows = 28
		cities = set()
		city_sprites = pg.sprite.Group()

		for city in self.game_map.nodes:
			cities.add(self.game_map.nodes[city].pixel)

		# for col in range(num_cols):
	 #		for row in range(num_rows):
	 #			new_city = City((width*col+margin*(col+1)),(height*row+margin*(row+1)),
	 #				width,height,self.click,FONT,'Non-City', (255,255,255))
	 #			city_sprites.add(new_city)
				
		for city in self.game_map.nodes:
			x = self.game_map.nodes[city].pixel[0]
			y = self.game_map.nodes[city].pixel[1]
			new_city = City(self.width*(x+1)+self.margin*(x+2),self.height*(y+1)+self.margin*(y+2),
				box_width,box_height,self.click_city,city_font,city, (255,255,255))
			city_sprites.add(new_city)

		
		city_sprites.add(new_city)
		return city_sprites



	def get_buttons(self, options):
		height = 30
		width = 300
		margin = 10
		counter = 0
		button_sprites = pg.sprite.Group()

		for i in options:
			new_button = Button(
				(self.screen_width/2-margin-width/2-width)+margin*math.floor(counter/10)+1 + width*math.floor(counter/10), 
				self.screen_height/10 + margin*(counter%10)+1 + height*(counter%10), width, height, self.click,
				FONT, str(i), (255,255,255))
			button_sprites.add(new_button)
			counter += 1

		# If you don't pass images, the default images will be used.
		quit_button = Button(
			self.screen_width/2 + 5, self.screen_height - 100, width, height, self.quit_game,
			FONT, 'Quit', (255, 255, 255))
		enter_button = Button(
		   	self.screen_width/2 - quit_button.width - 5, quit_button.y, 
			quit_button.width, quit_button.height, self.start_game,
			FONT, 'Enter', (255, 255, 255))

		button_sprites.add(quit_button,enter_button)
		return button_sprites

	def get_info_button(self):
		width = 25
		height = 25
		margin = 5
		button_sprites = pg.sprite.Group()
		new_button = Button(self.screen_width/4, 9*(self.screen_height/10), 
				700, height, self.do_nothing,
				FONT, str(self.selected_tickets), (255,255,255),IMAGE_NORMAL)
		button_sprites.add(new_button)
		return button_sprites

	def get_city_buttons(self):
		width = 25
		height = 25
		margin = 5
		button_sprites = pg.sprite.Group()
		for i in range(5):
			IMAGE_THIS_ONE = pg.Surface((100, 20))
			IMAGE_THIS_ONE.fill(color_list[i])
			new_button = Button(self.screen_width/10+margin*(i+1)+width*i, 9*(self.screen_height/10), 
				width, height, self.click_city_button,
				FONT, str(i+1), (255,255,255),IMAGE_THIS_ONE)
			button_sprites.add(new_button)
		return button_sprites

	def quit_game(self, text):
		self.done = True

	def do_nothing(self,text):
		pass

	def start_game(self, text):
		self.city_buttons = self.get_city_buttons()
		self.get_best_path()
		self.info_buttons = self.get_info_button()
		self.setup = False

	def get_best_path(self):
		print('thinking....')
		best_path,cars,value = self.game_map.best_path_tickets(self.selected_tickets)
		self.best_path_roads = []
		for i in range(len(best_path)-1):
			if best_path[i] != best_path[i+1]:
				city = best_path[i]
				dest = best_path[i+1]
				start_x = self.width*(self.game_map.nodes[city].pixel[0]+1) + self.margin*(self.game_map.nodes[city].pixel[0]+2) + self.width/2
				start_y = self.height*(self.game_map.nodes[city].pixel[1]+1) + self.margin*(self.game_map.nodes[city].pixel[1]+2) + self.height/2
				end_x = self.width*(self.game_map.nodes[dest].pixel[0]+1) + self.margin*(self.game_map.nodes[dest].pixel[0]+2) + self.width/2
				end_y = self.height*(self.game_map.nodes[dest].pixel[1]+1) + self.margin*(self.game_map.nodes[dest].pixel[1]+2) + self.height/2
				self.best_path_roads.append([(start_x,start_y),(end_x,end_y)])

	def click(self, text):
		for i in self.button_sprites:
			if i.text == text:
				if i.selected == True:
					self.button_sprites.add(Button(i.x, i.y, i.width, i.height, i.callback, i.font, 
						i.text, i.text_color, IMAGE_NORMAL, IMAGE_DOWN, IMAGE_HOVER))
					split_text = text.split("'")
					ticket = (split_text[1],split_text[3])
					self.selected_tickets.remove(ticket)
					i.kill()
				else:
					if len(self.selected_tickets) < 3:
						self.button_sprites.add(Button(i.x, i.y, i.width, i.height, i.callback, i.font, 
							i.text, i.text_color, IMAGE_SELECT, IMAGE_DOWN, IMAGE_HOVER, True))
						split_text = text.split("'")
						ticket = (split_text[1],split_text[3])
						self.selected_tickets.add(ticket)
					
						i.kill()

	def click_city(self,text):
		for i in self.city_sprites:
			if i.text == text:
				if i.selected == True:
					self.city_sprites.add(City(i.x, i.y, i.width, i.height, i.callback, i.font, 
						i.text, i.text_color, IMAGE_NORMAL, IMAGE_DOWN, IMAGE_HOVER))
					i.kill()
					self.current_road.remove(text)
				else:
					if len(self.current_road) == 0:
						self.city_sprites.add(City(i.x, i.y, i.width, i.height, i.callback, i.font, 
							i.text, i.text_color, IMAGE_SELECT, IMAGE_DOWN, IMAGE_HOVER, True))  
						self.current_road.append(text)	  			
						i.kill()
					if len(self.current_road) == 1 and text in self.game_map.nodes[self.current_road[0]].adj_list:
						self.city_sprites.add(City(i.x, i.y, i.width, i.height, i.callback, i.font, 
							i.text, i.text_color, IMAGE_SELECT, IMAGE_DOWN, IMAGE_HOVER, True))  
						self.current_road.append(text)	  			
						i.kill()
					if len(self.current_road) == 2:
						new_road = self.make_road()
						if self.player_number == 1:
							self.my_lines.append(new_road)
						else:
							self.other_lines.append(new_road)
							self.other_lines_colors.append(self.player_number)

	def click_city_button(self, text):
		width = 25
		height = 25
		margin = 5
		counter = 0
		for i in self.city_buttons:
			IMAGE_THIS_ONE = pg.Surface((100, 20))
			IMAGE_THIS_ONE.fill(color_list[counter])
			new_button = Button(self.screen_width/10+margin*(counter+1)+width*counter, 9*(self.screen_height/10), 
				width, height, self.click_city_button,
				FONT, str(counter+1), (255,255,255),IMAGE_THIS_ONE)
			if i.text == text:
				self.player_number = int(i.text)
				if i.selected == True:
					self.city_buttons.add(Button(i.x, i.y, i.width, i.height, i.callback, i.font, 
						i.text, i.text_color, IMAGE_NORMAL, IMAGE_DOWN, IMAGE_HOVER))
					i.kill()
				else:
					self.city_buttons.add(Button(i.x, i.y, i.width, i.height, i.callback, i.font, 
						i.text, i.text_color, IMAGE_SELECT, IMAGE_DOWN, IMAGE_HOVER, True))
					i.kill()
			else:
				self.city_buttons.add(new_button)
				i.kill()
			counter +=1
		counter = 0
							
						

	def make_road(self):

		city = self.current_road[0]
		dest = self.current_road[1]

		for i in self.city_sprites:
			if i.text == city or i.text == dest:
				if i.selected == True:
					self.city_sprites.add(City(i.x, i.y, i.width, i.height, i.callback, i.font, 
						i.text, i.text_color, IMAGE_NORMAL, IMAGE_DOWN, IMAGE_HOVER))
					i.kill()
					self.current_road.remove(i.text)

		start_x = self.width*(self.game_map.nodes[city].pixel[0]+1) + self.margin*(self.game_map.nodes[city].pixel[0]+2) + self.width/2
		start_y = self.height*(self.game_map.nodes[city].pixel[1]+1) + self.margin*(self.game_map.nodes[city].pixel[1]+2) + self.height/2
		end_x = self.width*(self.game_map.nodes[dest].pixel[0]+1) + self.margin*(self.game_map.nodes[dest].pixel[0]+2) + self.width/2
		end_y = self.height*(self.game_map.nodes[dest].pixel[1]+1) + self.margin*(self.game_map.nodes[dest].pixel[1]+2) + self.height/2

		if self.player_number != 1:
			self.game_map.remove_edge((city,dest))

		self.get_best_path()
		return [(start_x,start_y),(end_x,end_y)]

	def draw_roads(self):

		roads = []
		for city in self.game_map.city_map:
			start_x = self.width*(self.game_map.nodes[city].pixel[0]+1) + self.margin*(self.game_map.nodes[city].pixel[0]+2) + self.width/2
			start_y = self.height*(self.game_map.nodes[city].pixel[1]+1) + self.margin*(self.game_map.nodes[city].pixel[1]+2) + self.height/2
			for dest in self.game_map.city_map[city]:
				end_x = self.width*(self.game_map.nodes[dest].pixel[0]+1) + self.margin*(self.game_map.nodes[dest].pixel[0]+2) + self.width/2
				end_y = self.height*(self.game_map.nodes[dest].pixel[1]+1) + self.margin*(self.game_map.nodes[dest].pixel[1]+2) + self.height/2
				roads.append([(start_x,start_y),(end_x,end_y)])

		for i in roads:
			pg.draw.lines(screen, road_color, False, i, 2)
		for i in self.best_path_roads:
			pg.draw.lines(screen, best_color, False, i, 4) 
		for i in self.other_lines:
			pg.draw.lines(screen, other_color, False, i, 4)
		for i in self.my_lines:
			pg.draw.lines(screen, my_color, False, i, 4)
		



	def run(self):
		while not self.done:
			self.dt = self.clock.tick(30) / 1000
			if self.setup:
				self.handle_events_setup()
				self.run_logic_setup()
				self.draw_setup()
			else:
				self.handle_events_game()
				self.run_logic_game()
				self.draw_game()


	def handle_events_setup(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.done = True
			for button in self.button_sprites:
				button.handle_event(event)

	def run_logic_setup(self):
		self.button_sprites.update(self.dt)

	def draw_setup(self):
		self.screen.fill(background)
		self.button_sprites.draw(self.screen)
		pg.display.flip()



	def handle_events_game(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.done = True
			for city in self.city_sprites:
				city.handle_event(event)
			for city in self.city_buttons:
				city.handle_event(event)

	def run_logic_game(self):
		self.city_sprites.update(self.dt)
		self.city_buttons.update(self.dt)

	def draw_game(self):
		self.screen.fill(background)
		self.draw_roads()
		self.city_sprites.draw(self.screen)
		self.city_buttons.draw(self.screen)
		self.info_buttons.draw(self.screen)
		
		pg.display.flip()





if __name__ == '__main__':
	pg.init()
	new_game = Game(screen)
	new_game.run()
	pg.quit()