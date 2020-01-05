#!/usr/bin/python
import pygame
import sys
import random
import math

from globfuns import *


pygame.init()
pygame.key.set_repeat()
pygame.mouse.set_visible(False)



def debug(do=True):
	if do:
		pass


class Game:
	
	def __init__(self):
		self.defaultwidth = 1915
		self.defaultheight = 1000
		flags = pygame.RESIZABLE
		self.screen = pygame.display.set_mode((self.defaultwidth, self.defaultheight), flags)
		pygame.display.set_caption('Life Simulator')
		self.fullscreen = False
		self.font = 'StayPuft.ttf'
		
		self.running = True
		self.events = None
		self.KEYTAPPED = False
		self.KEYPRESSED = False
		self.CONTROL = False
		self.SHIFT = False
		self.MOUSECLICKED = False
		self.MOUSEPRESSED = False
		self.MOUSEMOVED = False
		self.LEFT = 0
		self.RIGHT = 2
		self.MIDDLE = 1
		self.BUTTON1 = False
		self.BUTTON = False
		
		self.clock = pygame.time.Clock()
		self.frames = 0
		self.seconds = 0
		self.minutes = 0
		
		self.docheats = True
		self.message = ''
		
		self.loopitems = []
		self.worlds = []
		self.components = []
		self.entities = []
		self.blocks = []

	
	def update(self):
		self.width, self.height = self.screen.get_size()
		self.mouseX, self.mouseY = pygame.mouse.get_pos()
		self.tileX = -roundTo(player.x - self.mouseX + (self.width/2), player.world.tilesize)
		self.tileY = roundTo(player.y - self.mouseY + (self.height/2), player.world.tilesize)
		self.drawfinger = False
		
	
	def act(self):
		self.checkEvents()
		self.update()
		stats.Stat.retrieveStats()
		self.keepTime()
		player.world.update()
		for time in range(2):
			for group in reversed(self.loopitems):
				for item in group:
					if time == 0:
						item.update()
					elif time == 1:
						item.act()
		player.reset()
		self.reset()
		self.clock.tick()
		
	
	def draw(self):
		player.world.draw()
		for eachclass in self.loopitems:
			for item in eachclass:
				if item.world == player.world and item.onscreen and item.visible:
					item.draw()
		player.drawOverheadDisplay()
		effects.drawCursor()
		stats.Stat.drawStats()
		if self.message:
			self.displayMessage(self.message, int(self.width*0.15))
			self.message = ''
		if player.tpcooldown > 3:
			pygame.display.flip()
			
	
	def displayMessage(self, message, size=200):
		write(game.screen, game.font, size, int(self.width/2), int(self.height/2), message, (255, 255, 255), True)
		
	
	def keepTime(self):
		self.seconds = int(pygame.time.get_ticks()/1000)%60
		self.minutes = int((pygame.time.get_ticks()/1000)/60)%60
		self.clock.tick()
		self.frames += 1
		
	
	def passClassesByReference(self):
		for group in self.loopitems:
			for item in group + game.worlds + [stats.Stat]:
				if hasattr(item, 'game') or hasattr(item, 'player'):
					if not item.game:
						item.game = self
					if not item.player:
						item.player = player
		
	
	def checkEvents(self):
		self.events = pygame.event.get()
		self.keys = pygame.key.get_pressed()
		self.mouse = pygame.mouse.get_pressed()
		self.checkKeys()
		for event in self.events:
			if event.type == pygame.QUIT:
				self.running = False
			elif event.type == pygame.VIDEORESIZE:
				self.screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				self.MOUSECLICKED = True
				self.MOUSEPRESSED = True
			elif event.type == pygame.MOUSEBUTTONUP:
				self.MOUSEPRESSED = False
			if event.type == pygame.MOUSEMOTION:
				self.MOUSEMOVED = True
				effects.drawarrow = True
			elif event.type == pygame.KEYDOWN:
				self.KEYTAPPED = True
				self.KEYPRESSED = True
				self.cheats()
				self.options()
			elif event.type == pygame.KEYUP:
				self.KEYPRESSED = False
		
	
	def reset(self):
		self.MOUSECLICKED = False
		self.MOUSEMOVED = False
		self.KEYTAPPED = False
		
		if not stats.Stat.visible:
			effects.drawarrow = False
		#if player.moved and self.MOUSEMOVED:
		#	effects.drawarrow = False
		
	
	def checkKeys(self):
		if self.keys[pygame.K_e] or self.keys[pygame.K_RETURN] or self.mouse[self.LEFT]:
			self.BUTTON1 = True
		else:
			self.BUTTON1 = False
			
		if self.keys[pygame.K_f] or self.keys[pygame.K_BACKSPACE] or self.mouse[self.RIGHT]:
			self.BUTTON2 = True
			
		else:
			self.BUTTON2 = False
			
		if self.keys[pygame.K_LSHIFT] or self.keys[pygame.K_RSHIFT]:
			self.SHIFT = True
		else:
			self.SHIFT = False
		if self.keys[pygame.K_LCTRL] or self.keys[pygame.K_RCTRL]:
			self.CONTROL = True
		else:
			self.CONTROL = False
		
	
	def options(self):
		if self.keys[pygame.K_ESCAPE]:
			pygame.quit()
			sys.exit()
		if self.keys[pygame.K_F11]:
			self.fullscreen = not self.fullscreen
			if self.fullscreen:
				self.screen = pygame.display.set_mode((self.defaultwidth, self.defaultheight), pygame.RESIZABLE)
			else:
				self.screen = pygame.display.set_mode((1920, 1080), pygame.NOFRAME)
		if self.CONTROL:
			if self.keys[pygame.K_1]:
				stats.Stat.detailed = not stats.Stat.detailed
			if self.keys[pygame.K_2]:
				stats.Stat.visible = not stats.Stat.visible
			if self.keys[pygame.K_3]:
				block.Block.is3D = not block.Block.is3D
				block.Block.sortBlocks()
			if self.keys[pygame.K_4]:
				Component.showname = not Component.showname
		if self.SHIFT or self.keys[pygame.K_KP0]:
			player.sprinting = not player.sprinting
		
	
	def cheats(self):
		if self.docheats:
			if self.CONTROL:
				if self.keys[pygame.K_b]:
					player.cycleWorlds(-1)
				if self.keys[pygame.K_n]:
					player.cycleWorlds(1)
				if self.keys[pygame.K_i]:
					player.onscreen = not player.onscreen
				if self.keys[pygame.K_h]:
					player.invincible = not player.invincible
					if player.invincible:
						player.strength += 1000
					else:
						player.strength -= 1000
				if self.keys[pygame.K_COMMA]:
					player.clearBlocks()
				if self.keys[pygame.K_k]:
					player.living = not player.living
					if player.living:
						player.health += 1000
				if self.keys[pygame.K_u]:
					if player.coolness != 69420:
						player.coolness = 69420
					else:
						player.coolness = 0
	

game = Game()


import theplayer
import world
import component
import block
import stats
import entity


theplayer.game = game
player = theplayer.player1

import effects


for afile in [world, component, entity, block, effects, stats]:
	afile.game = game
	afile.player = player


game.worlds = world.World.worlds
game.components = component.Component.components
game.entities = entity.Entity.entities
game.blocks = entity.Block.blocks



game.loopitems = [game.components, game.blocks, game.entities, [player]]

#game.passClassesByReference()

while game.running:
	game.act()
	game.draw()
	debug()
pygame.quit()
sys.exit()
