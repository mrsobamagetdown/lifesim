import pygame
import random
import math

from globfuns import *

class World:
	
	game = None
	player = None
	
	worlds = []
	
	def __init__(self, name, width, height, color, outercolor=None, walled=False, outerdamage=0, outerspeed=1, slip=0.5):
		World.worlds.append(self)
		
		self.name = name
		self.width = width
		self.height = height
		self.screenX = -self.width
		self.screenY = -self.height
		self.rect = screenRect(self)
		self.innerrect = self.rect
		self.color = color
		self.outercolor = outercolor
		self.walled = walled
		self.tilesize = 100
		self.outerdamage = outerdamage
		self.outerspeed = outerspeed
		self.slip = slip
		
	
	def update(self):
		game = World.game
		player = World.player
		
		self.screenX = player.x - (self.width/2) + (game.width/2)
		self.screenY = player.y - (self.height/2) + (game.height/2)
		self.rect = screenRect(self)
		# Create a rectangle that contains all positions of the player where the edge of the screen is not visible.
		# When player is inside, the self's edge isn't drawn to increase framerate.
		self.innerrect = self.rect.copy().inflate((-game.width-player.width, -game.height-player.height))
		
	
	def draw(self):
		screen = World.game.screen
		if self.outercolor and not World.player.rect.colliderect(self.innerrect):
			screen.fill(self.outercolor)
			pygame.draw.rect(screen, self.color, self.rect)
		else:
			screen.fill(self.color)
		
	
	def randX(self):
		return(random.randint(int(-self.width/2), int(self.width/2)))
		
	def randY(self):
		return(random.randint(int(-self.height/2), int(self.height/2)))
	


town = World('Town', 12500, 12500, (86, 200, 93), (220, 200, 140))
houseinterior = World('House Interior', 1050, 850, (230, 210, 140), (100, 80, 50), walled=True)
shopinterior = World('Shop Interior', 1200, 750, (225, 225, 225), (250, 100, 100), walled=True)
schoolinterior = World('School Interior', 1200, 750, (200, 200, 200), (200, 110, 75), walled=True)
city = World('City', 7500, 7500, (170, 170, 170), (110, 220, 130))
apartmentinterior = World('Apartment Interior', 1125, 1575, (220, 200, 140), (200, 140, 50), walled=True)
farm = World("Farm", 6500, 6500, (80, 220, 120), (200, 190, 70), outerspeed=0.4)
snowland = World('Snowland', 6000, 6000, (180, 220, 230), (100, 75, 40))
heck = World('Heck', 4500, 4500, (100, 35, 30), (255, 150, 0), outerdamage=6, outerspeed=0.5) # No swearing on my christian minecraft server
cheeseland = World('Cheese Land', 3500, 3500, (255, 210, 75), (255, 175, 100))
caveland = World('Cave Land', 3000, 1000, (90, 90, 90), (25, 25, 25), walled=True)
daddyland = World('Daddyland', 6900, 4200, (255, 195, 240), (255, 50, 170), outerspeed=0.1, walled=True)
labinterior = World('Lab Interior', 1500, 1500, (120, 120, 120), walled=True)
desktop = World('Desktop', 1500, 1500, (0, 0, 0), (100, 100, 100), walled=True)
thinkplains = World('Thinkplains', 5000, 5000, (0, 0, 0), walled=True)



