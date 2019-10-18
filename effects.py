import pygame
import random
import math

from globfuns import *


game = None
player = None


class Image:
	
	images = []
	
	def __init__(self, imagename, width, height, fileending='png'):
		self.name = imagename
		self.width = width
		self.height = height
		self.image = createImage(self, imagename, fileending)
		
	
	def draw(self, x, y):
		game.screen.blit(self.image, (x, y))
		

pointer = Image('pointer', 50, 50)
finger = Image('finger', 50, 50)
target = Image('target', 65, 65)



def drawEffects():
	
	pass
	

def drawCursor():
	if pygame.mouse.get_focused():
		if player.checkRanged():
			target.draw(game.mouseX-(target.width/2), (game.mouseY-target.height/2))
		else:
			if player.getSelectedVal('Type') == 'Block':
				tilesize = player.world.tilesize
				thickness = 2
				x = player.x - roundTo((-game.tileX + (tilesize/2)), tilesize/2) + (game.width/2)
				y = player.y - roundTo((game.tileY + (tilesize/2)), tilesize/2) + (game.height/2)
				pygame.draw.rect(game.screen, (0, 0, 0), (x, y, tilesize, tilesize), thickness)
				
			if (player.getSelectedVal('Type') == 'Block' or game.drawcursor) and not game.drawfinger:
				pointer.draw(game.mouseX, game.mouseY)
			if game.drawfinger:
				finger.draw(game.mouseX, game.mouseY)
				
	


from lifesim import *
