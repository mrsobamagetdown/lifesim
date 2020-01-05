import pygame
import random
import math

from globfuns import *
from world import *
from block import *
from component import *
import proceduralgen


game = None
player = None


class Entity(Component):
	
	entities = []
	
	def __init__(self, name, x, y, width, height, color, world, angle, speed, Range, showname=False, elliptical=True, health=10000, solid=False, textsize=50, damage=0, damageplayer=True, bumphit=True, playerspeed=1, slip=0.5, imagename='', textcolor=(255, 255, 255), overrideshow=False, condition='True', command='pass', interactive=False, replenish=False, tp=None, noreturn=False, boomerang=False, restrictborder=False, startanimated=True):
		
		super().__init__(name, x, y, width, height, color, world, showname, elliptical, health, solid, textsize, damage, bumphit, playerspeed, slip, imagename, textcolor, overrideshow, condition, command, interactive, replenish, tp, noreturn)
			
		Entity.entities.append(self)
		Component.components.remove(self)
		
		self.animated = startanimated
		self.finished = False
		self.visible = startanimated
		self.distance = 0
		self.startx = x
		self.starty = y
		self.angle = angle
		self.speed = speed
		self.damageplayer = damageplayer
		self.range = Range
		self.forward = True
		self.boomerang = boomerang
		self.restrictborder = restrictborder
		
	
	def animate(self):
		self.animated = True
		self.visible = True
		
	
	def act(self):
		print(self.name + ' ' + str(self.x) + ' ' + str(self.y))
		super().collision(self.damageplayer)
		super().checkHealth()
		self.damagecooldown += 1
		
		if abs(self.distance) <= self.range:
			self.x = (math.sin(math.radians(self.angle))*self.distance)-self.startx
			self.y = (math.cos(math.radians(self.angle))*self.distance)+self.starty
			if self.restrictborder:
				self.x = restrict(self.x, -self.world.width/2, self.world.width/2)
			if self.forward:
				self.distance += self.speed
			else:
				self.distance -= self.speed
		elif self.boomerang:
			self.forward = not self.forward
			self.distance = self.range
		else:
			self.visible = False
			Entity.entities.remove(self)
			del self
			
			
	def goToPlayer(self):
		player = player
		self.x = player.x
		self.y = player.y
		self.world = player.world
		
	

daddybeast = Entity('daddybeast', 0, 0, 100, 80, (0, 50, 0), daddyland, 0, 0.3, 1000, boomerang=True, health=1000, replenish=True)
#arrow = Entity()
