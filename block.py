import pygame
import random
import math

from globfuns import *
from component import *

pygame.init()


game = None
player = None

class Block:
	
	blocks = []
	is3D = True
	count = 0
	viewangle = 0
	padding = 8
	types = {
			'Stone': {
				'ID': 0,
				'Color1': (150, 150,150),
				'Color2' : (100, 100, 100),
			},
			'Ground': {
				'ID': 1,
				'Color1': (86, 200, 76),
				'Color2': (220, 200, 140),
			},
			'Dirt': {
				'ID': 2,
				'Color1': (220, 200, 140),
				'Color2' : (86, 200, 76),
			},
			'snow': {
				'ID': 3,
				'Color1': (245, 250, 255),
				'Color2': (200, 215, 255),
				'Player Speed': 0.5,
			},
			'Wood': {
				'ID': 4, 
				'Color1':  (230, 185, 120), 
				'Color2':  (210, 155, 100),	
			},
			'Ice': {
				'ID': 5, 
				'Color1': (100, 200, 230),
				'Color2':  (240, 185, 130),
				'Slipperyness': 0.6
			},
			'Light Stone': {
				'ID': 6,
				'Color1': (200, 200,200),
				'Color2' : (150, 150, 150),
			},
		}
		
	@classmethod
	def sortBlocks(cls):
		if Block.is3D > 0:
			cls.blocks.sort(key = lambda theblock: -theblock.y) #Orders 3d block by Y-position so they dont overlap.
		
	
	def __init__(self, name, x, y, width, height, world, solid=False, imagename='', replenish=False):
		Block.blocks.append(self)
		Block.count = len(Block.blocks)
		
		self.name = name
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.world = world
		self.deleted = False
		self.color1 = Block.types[name]['Color1']
		self.color2 = Block.types[name]['Color2']
		self.solid = solid
		self.screenX = -200
		self.screenY = -200
		self.rect = screenRect(self)
		self.playertouching = False
		self.depth = 0
		self.slip = 0
		self.playerspeed = 1
		self.onscreen = True
		self.visible = True
		self.tallness = 0
		self.replenish = replenish
		self.image = createImage(self, imagename)
		
	
	def update(self):
		self.screenX = player.x+(self.x-(self.width/2))+(game.width/2)
		self.screenY = player.y-(self.y+(self.height/2))+(game.height/2)
		self.rect = screenRect(self)
		self.onscreen = self.rect.colliderect(game.screen.get_rect())
		self.tallness = int(Block.is3D)*35
		
	
	def act(self):
		self.collision()
		
	
	def collision(self):
		if self.rect.colliderect(player.rect):
			player.touching.add(self)
		else:
			player.touching.discard(self)
		
	
	def draw(self):
		if not self.deleted:
			pygame.draw.rect(game.screen, self.color2, (self.screenX, self.screenY-self.tallness, self.width, self.height+self.tallness))
			pygame.draw.rect(game.screen, self.color1, (self.screenX + (Block.padding/2), self.screenY + (Block.padding/2)-self.tallness, self.width-Block.padding, self.height-Block.padding))
	
