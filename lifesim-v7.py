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
		self.width = self.defaultwidth
		self.height = self.defaultheight
		flags = pygame.RESIZABLE
		self.screen = pygame.display.set_mode((self.width, self.height), flags)
		pygame.display.set_caption('Life Simulator')
		self.fullscreen = False
		
		self.running = True
		self.events = None
		self.KEYTAPPED = False
		self.KEYPRESSED = False
		self.CONTROL = False
		self.SHIFT = False
		self.drawcursor = False
		self.drawfinger = False
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
		self.projectiles = []
		self.blocks = []

	
	def play(self):
		self.loop()
		self.draw()
		
	
	def update(self):
		self.width, self.height = self.screen.get_size()
		self.mouseX, self.mouseY = pygame.mouse.get_pos()
		self.tileX = -roundTo(player.x - self.mouseX + (self.width/2), player.world.tilesize)
		self.tileY = roundTo(player.y - self.mouseY + (self.height/2), player.world.tilesize)
		self.drawfinger = False
		
	
	def loop(self):
		self.checkEvents()
		self.updateClasses()
		Stat.retrieveStats()
		self.keepTime()
		self.update()
		player.world.update()
		for time in range(2):
			for group in reversed(self.loopitems):
				for item in group:
					if time == 0:
						item.update()
					elif time == 1:
						item.loop()
		player.reset()
		self.reset()
		self.clock.tick()
		
	
	def draw(self):
		player.world.draw()
		for eachclass in self.loopitems:
			for item in eachclass:
				if item.world == player.world and item.onscreen and item.visible:
					item.draw()
		effects.drawCursor()
		Stat.drawStats()
		if self.message:
			self.displayMessage(self.message, int(self.width*0.15))
			self.message = ''
		if player.tpcooldown > 3:
			pygame.display.flip()
		
	
	def displayMessage(self, message, size=200):
		write(game.screen, 'font.ttf', size, int(self.width/2), int(self.height/2), message, (255, 255, 255), True)
		
	
	def keepTime(self):
		self.seconds = int(pygame.time.get_ticks()/1000)%60
		self.minutes = int((pygame.time.get_ticks()/1000)/60)%60
		self.clock.tick()
		self.frames += 1
		
	
	def updateClasses(self):
		for group in self.loopitems:
			for item in group + game.worlds + [Stat]:
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
				self.drawcursor = True
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
				Stat.detailed = not Stat.detailed
			if self.keys[pygame.K_2]:
				Stat.visible = not Stat.visible
			if self.keys[pygame.K_3]:
				Block.is3D = not Block.is3D
				Block.sortBlocks()
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



class Player:
	
	def __init__(self, name):
		self.name = name
		self.world = town
		self.x = 0
		self.y = 0
		self.width = 85
		self.height = 85
		self.screenX = 0
		self.screenY = 0
		self.rect = screenRect(self)
		self.shape = pygame.draw.ellipse
		self.color = (255, 255, 0)
		self.image = None
		self.images = {
		'coolio': None, 
		'happy': None, 
		'meep': None, 
		'cry': None, 
		'scared': None, 
		'pissed': None, 
		'meh': None, 
		'supercoolio': None, 
		'dead': None,
		}
		for image in self.images:
			self.images[image] = loadImage(image)
		
		self.living = True
		self.health = 1000
		self.age = 0
		self.happiness = 0
		self.money = 0
		self.intelligence = 1
		self.weight = 50
		self.energy = 1000
		self.strength =  1
		self.coolness = 0
		
		self.basespeed = 7
		self.speed = self.basespeed
		self.sprinting = False
		self.angle = 270
		self.xmomentum = 0
		self.ymomentum = 0
		self.moved = False
		
		self.unlimited = False
		self.invincible = False
		self.superstrength = False
		self.indoors = False
		self.overborder = False
		self.cangointodebt = False
		self.canteleport = True
		self.tpcooldown = 0
		self.worldto = None
		
		self.damage = 0
		self.lastdamage = 0
		self.damagecooldown = 0
		self.attackcooldown = 10
		self.damagetaken = 0
		self.lastdamagetaken = 0
		self.lasthealth = self.health
		
		self.visible = True
		self.onscreen = True
		self.onground = True
		self.onblock = False
		self.touching = set([])
		
		self.slot = 1
		self.selected= 'Hand'

		self.inventory = {
			'Hand': {
				'Slot': 1,
				'Type': 'Weapon',
				'Amount': 1,
				'Damage': 1,
				'Depletable': False,
			},
			'Stone': {
				'Slot': 7,
				'Type': 'Block',
				'Amount': 0,
				'Depletable': True,
			 },
			'Ground': { 
				'Slot': 8,
				'Type': 'Block',
				'Amount': 100,
				'Depletable': True,
			},
			'Dirt': {
				'Slot': 9,
				'Type': 'Block',
				'Amount': 100,
				'Depletable': True,
			},
			'Rainbow': {
				'Slot': 0,
				'Type': 'Block',
				'Amount': 100,
				'Depletable': True,
			},
			'Wood': {
				'Slot': 6,
				'Type': 'Block',
				'Amount': 100,
				'Depletable': True,
			},
			'Sword': {
				'Slot': 4,
				'Type': 'Weapon',
				'Damage': 100, 
				'Amount': 1,
				'Depletable': False,
				'Range': 0
			},
			'Shield': {
				'Slot': 0, 
				'Type': 'Armor',
				'Protection': 0.5,
				'Amount': 1,
				'Depletable': False,
			},
			'Chips': {
				'Slot': 3,
				'Type': 'Consumable',
				'Amount': 50,
				'Command': 'player.energy += 50',
				'Depletable': True,
			},
			'First Aid Kit': {
				'Slot': 2,
				'Type': 'Consumable', 
				'Amount' : 5,
				'Command': 'player.health += 200',
				'Depletable': True,
			},
			'Bow & Arrow': {
				'Slot': 5,
				'Type': 'Weapon',
				'Amount': 100,
				'Depletable': True,
				'Damage': 50,
				'Speed': 50,
				'Range': 10,
				'Color': (125, 100, 50),
				'Health': 50
			},
		}
		
	
	def update(self):
		self.screenX = (self.width/-2) + (game.width/2)
		self.screenY = (self.width/-2) + (game.height/2)
		self.moved = False
		self.rect = screenRect(self)
		self.damagecooldown += 1
		self.tpcooldown += 1
		
	
	def loop(self):
		self.chooseDirection()
		self.manageSpeed()
		self.control()
		self.manageStats()
		self.manageImage()
		self.checkborder()
		self.checkSolids()
		self.useItems()
		if game.MOUSECLICKED or game.KEYTAPPED:
			self.selectSlot()
		
	
	def draw(self):
		if self.onscreen:
			self.shape(game.screen, self.color, self.rect)
			if self.image:
				game.screen.blit(pygame.transform.scale(self.image, (int(self.width), int(self.height))), self.rect)
		
	
	def reset(self):
		self.moved = False
		self.lasthealth = self.health
		if self.damage > 0:
			self.lastdamage = self.damage
		self.damage = 0
		if self.lasthealth != self.health:
			self.damagetaken = self.lasthealth - self.health
			self.damagecooldown = 0
		if self.damagetaken > 0:
			self.lastdamagetaken = self.damagetaken
		
	
	def control(self):
		horizontal, vertical = False, False
		if game.keys[pygame.K_d]:
			self.xmomentum = self.speed
			self.x -= self.speed
			horizontal = True
		if game.keys[pygame.K_a]:
			self.xmomentum = -self.speed
			self.x += self.speed
			horizontal = True
		if game.keys[pygame.K_w]:
			self.y += self.speed
			self.ymomentum = -self.speed
			vertical = True
		if game.keys[pygame.K_s]:
			self.ymomentum = self.speed
			self.y -= self.speed
			vertical = True
			
		if horizontal or vertical:
			self.moved = True
		if self.moved and not game.MOUSEMOVED:
			game.drawcursor = False
		
		slip = 0
		if self.touching:
			for thing in self.touching:
				slip = thing.slip # actually tries to find slipperyness of the one the character is directly on top of (on the highest layer)
		else:
			slip = self.world.slip
			
		if not (horizontal):	
			self.x -= self.xmomentum
			self.xmomentum *= slip
		if not (vertical):
			self.ymomentum *= slip
			self.y -= self.ymomentum
		
	
	def chooseDirection(self):
		if game.MOUSEMOVED:
			# https://gamedev.stackexchange.com/questions/132163/how-can-i-make-the-player-look-to-the-mouse-direction-pygame-2d
			relativeX, relativeY = game.mouseX - self.screenX-(self.width/2), game.mouseY - self.screenY-(self.height/2)
			self.angle = math.degrees(math.atan2(relativeY, relativeX))+90
		
	
	def manageSpeed(self):
		speedmultiplier = 1
		if self.overborder and self.onground:
			speedmultiplier *= self.world.outerspeed
		for thing in self.touching:
			speedmultiplier *= thing.playerspeed
		self.walkingspeed = ((self.energy*0.013)+self.basespeed)*speedmultiplier
		if self.sprinting:
			self.speed = self.walkingspeed*2 # sprinting
			self.energy -= 0.15
		else:
			self.speed = self.walkingspeed # walking normally
			self.energy -= 0.075
		
	
	def manageStats(self):
		if self.energy <= 0 or self.weight <= 0:# or self.age >= 120:
			self.health -= 2
		if self.health <= 0:
			self.living = False
		if not self.living:
			game.message = 'You died!'
			self.speed = 0
			self.basespeed = 0
		if not self.cangointodebt:
			self.money = max(self.money, 0)
		if self.invincible:
			self.health = 1000
			self.energy = 1000
			self.cangointodebt = True
		else:
			self.age += 0.005
			#self.height *= 1.0002
			#self.height *= 1.0002
			self.cangointodebt = False
		self.onground = not self.touching
		self.health = max(0, self.health)
		self.energy = max(0, self.energy)
		self.weight = max(0, self.weight)
		
	
	def cycleWorlds(self, direction=1):
		worlds = game.worlds
		if direction > 0:
			if worlds.index(player.world) < len(worlds)-1:
				world = worlds[worlds.index(player.world)+direction]
			else:
				world = worlds[-120]
		elif direction < 0:
			if worlds.index(player.world) < len(worlds):
				world = worlds[worlds.index(player.world)+direction]
			else:
				world = worlds[len(worlds)-1]
		self.tp(world)
	
	
	def tp(self, position=(0, 0)):
		if self.tpcooldown > 4:
			if isinstance(position, World):
					self.x = 0
					self.y = 0
					self.world = position
			elif isinstance(position, Component):
					self.x = -position.x
					self.y = position.y
					self.world = position.world
			else:
				self.x = -position[0]
				self.y = position[1]
			self.tpcooldown = 0
		
	
	def checkborder(self):
		if not self.rect.colliderect(self.world.rect):
			self.overborder = True
			if self.onground:
				self.health -= self.world.outerdamage
		else:
			self.overborder = False
		if self.world.walled:
			self.x = restrict(self.x, -(self.world.width/2) + (self.width/2), (player.world.width/2) - (player.width/2))
			self.y = restrict(self.y, -(player.world.height/2) +(player.height/2), (player.world.height/2) - (player.height/2))
		
	
	def checkSolids(self):
		items = Component.components.copy()
		if game.blocks:
			items.extend(game.blocks)
		if True not in list(map(lambda a: a in self.touching and a.solid, items)):
			self.onblock = False
		
		if not self.onblock:
			for item in items:
				if self.rect.colliderect(item.rect) and item.onscreen and item.solid and not item.deleted:
					if self.screenY > item.screenY - (item.height/2) and self.screenY < item.screenY + (item.height/2):
						if self.screenX > item.screenX:
							self.x = min(-item.x - self.width, self.x)
						else:
							self.x = max(-item.x + self.width, self.x)
					if self.screenX > item.screenX - (item.width/2) and self.screenX < item.screenX + (item.width/2):
						if self.screenY > item.screenY:
							self.y = min(item.y - self.height, self.y)
						if self.screenY < item.screenY:
							self.y = max(item.y + self.height, self.y)
		
	
	def selectSlot(self):
		keys = (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9)
		for key in keys:
			if game.keys[key] and not game.CONTROL:
				self.slot = keys.index(key)+1
				for item in self.inventory:
					if self.getItemVal(item, 'Slot') == self.slot:
						self.selected = item
			
		
	def getItemVal(self, item, key):
		val = self.inventory.get(item).get(key)
		return val
	
	def getSelectedVal(self, key):
		val = self.getItemVal(self.selected, key)
		return val
		
	
	def depleteItem(self, item, amount=1):
		if self.getItemVal(item, 'Depletable') == True:
			if self.getItemVal(item, 'Amount') >= amount and not self.invincible:
				self.inventory[item]['Amount'] -= amount
				return True
		return False
		
	def gainItem(self, item, amount=1):
		self.inventory[item]['Amount'] += amount
		
	
	def canPay(self, amount=0):
		value = self.money > amount or self.cangointodebt
		return value
		
	
	def checkRanged(self):
		if 'Range' in self.inventory[self.selected].keys():
			if self.getSelectedVal('Range') > 0:
				return True
		return False
		
	
	def getDamage(self):
		basedamage = self.getSelectedVal('Damage')
		damage = basedamage + int(self.strength-0.5)
		self.damage = damage
		return damage
		
	
	def showDamage(self):
		if self.damagecooldown < 3 and self.lastdamagetaken > 0 and not self.invincible:
			self.displayText(self.lastdamagetaken, int((self.lastdamagetaken/2)+40), (255, 0, 0))
		
	
	def useItems(self):
		if self.selected == 'Hand' or self.getSelectedVal('Type') == 'Weapon' and (self.getSelectedVal('Amount') > 0 or self.unlimited):
			self.canteleport = True
		else:
			self.canteleport = False
		if self.getSelectedVal('Amount') > 0 or self.unlimited:
			if game.BUTTON1:
				if game.MOUSECLICKED or game.KEYTAPPED:
					if self.getSelectedVal('Type') == 'Consumable':
						command = self.getSelectedVal('Command')
						exec(command)
						self.depleteItem(self.selected)
				if game.MOUSEPRESSED or game.KEYPRESSED:
					if self.getSelectedVal('Type') == 'Block':
						self.placeBlock(self.selected, game.tileX, game.tileY)
			if game.BUTTON2:
				if game.MOUSECLICKED or game.KEYTAPPED:
					player.attackcooldown = 0
					if self.getSelectedVal('Type') == 'Weapon':
						self.damage = self.getDamage()
					if self.checkRanged():
						gs = self.getSelectedVal
						self.damage = self.getDamage() # <-- Possibly deletable because I think it's used earlier in every situation where this is called
						newprojectile = Projectile('Arrow', self.x, self.y, 15, 15, (125, 100, 50), self.world, self.angle, 30, 750, elliptical=True, damage=self.getDamage(), damageplayer=False)
						newprojectile.launch()
						self.depleteItem(self.selected)
			player.attackcooldown += 1
		else:
			self.canteleport = True
		if game.BUTTON2 and (game.MOUSEPRESSED or game.KEYPRESSED):
			if self.getSelectedVal('Type') == 'Block':
				self.breakBlock()
		
	
	def manageImage(self):
		if self.happiness >= 1000:
			image = 'coolio'
		elif self.happiness >= 500:
			image = 'happy'
		elif self.happiness > 250:
			image = 'meep'
		elif self.happiness <= -1000:
			image = 'cry'
		elif self.happiness <= -500:
			image = 'scared' 
		elif self.happiness <= -250:
			image = 'pissed'
		else:
			image = 'meh'
		if self.coolness == 69420:
			image = 'supercoolio'
		if not self.living:
			image = 'dead'
		self.image = self.images[image]
		
		
	def displayText(self, text, size=40, color=(255, 255, 255)):
		write(game.screen, 'font.ttf', size, game.width/2, game.height/2-self.height-size/2, str(text), color, True)
		
	
	def placeBlock(self, theblock, x, y):
		placeable = True
		for block in game.blocks:
			if x == block.x and y == block.y and self.world == block.world and not block.deleted:
				placeable = False # Prevents the block from overwriting another block.
		if placeable and self.world.tilesize > 0:
			width = self.world.tilesize
			height = self.world.tilesize
			newblock = Block(theblock, game.tileX, game.tileY, width, height, self.world, True)
			if Block.is3D:
				Block.sortBlocks()
			self.depleteItem(theblock)
			self.onblock = True
		
	
	def breakBlock(self):
		for block in game.blocks:
			if block.rect.collidepoint(game.mouseX, game.mouseY):
				if not block.deleted:
					#if not self.invincible:
					self.gainItem(block.name)
					if not block.replenish:
						block.deleted = True
						del block
					else:
						block.x, block.y = block.world.randX(), block.world.randY()
		
	
	def clearBlocks(self):
		for block in game.blocks:
			if not block.deleted:
				game.blocks.clear()
				if not self.invincible:
					self.gainblock(block.name)
				block.deleted = True
				del block
		
	

from worldclass import *
from componentclass import *
from blockclass import *
from stats import *
from projectile import *

player = Player('Player1')

import effects


game.worlds = World.worlds
game.components = Component.components
game.projectiles = Projectile.projectiles
game.blocks = Block.blocks

for aclass in [World, Component, Block, effects]:
	aclass.game = game
	aclass.player = player


# Reconfigure procedural init params first
'''
from proceduralgen import generation
#generator = generation()

for i in range(5):
	newworld = World(*generator.genWorld())
for i in range(40):
	newcomponent = Component(*generator.genComponent())
	print(newcomponent.rect)
	print(newcomponent.world)
'''



game.loopitems = [game.components, game.blocks, game.projectiles, [player]]


if __name__ == '__main__' or True:
	while game.running:
		game.play()
		debug()
pygame.quit()
sys.exit()
