import pygame
import random
import math

from globfuns import *
from world import *
from entity import *
from component import *
from block import *


game = None


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
		
		self.basespeed = 6.5
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
				'Command': 'self.energy += 50',
				'Depletable': True,
			},
			'First Aid Kit': {
				'Slot': 2,
				'Type': 'Consumable', 
				'Amount' : 5,
				'Command': 'self.health += 200',
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
		
	
	def act(self):
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
			self.x -= self.speed
			self.xmomentum = self.speed
			horizontal = True
		if game.keys[pygame.K_a]:
			self.x += self.speed
			self.xmomentum = -self.speed
			horizontal = True
		if game.keys[pygame.K_w]:
			self.y += self.speed
			self.ymomentum = -self.speed
			vertical = True
		if game.keys[pygame.K_s]:
			self.y -= self.speed
			self.ymomentum = self.speed
			vertical = True
		
		if horizontal or vertical:
			self.moved = True
		
		slip = 0
		if self.touching:
			for thing in self.touching:
				slip = thing.slip # actually tries to find slipperyness of the one the character is directly on top of (on the highest layer)
		else:
			slip = self.world.slip
			
		if not horizontal:	
			self.x -= self.xmomentum
			self.xmomentum *= slip
		if not vertical:
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
			if worlds.index(self.world) < len(worlds)-1:
				world = worlds[worlds.index(self.world)+direction]
			else:
				world = worlds[0]
		elif direction < 0:
			if worlds.index(self.world) < len(worlds):
				world = worlds[worlds.index(self.world)+direction]
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
			self.x = restrict(self.x, -(self.world.width/2) + (self.width/2), (self.world.width/2) - (self.width/2))
			self.y = restrict(self.y, -(self.world.height/2) +(self.height/2), (self.world.height/2) - (self.height/2))
		
	
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
					self.attackcooldown = 0
					if self.checkRanged():
						gs = self.getSelectedVal
						arrow = Entity('Arrow', self.x, self.y, 15, 15, (125, 100, 50), self.world, self.angle, 30, 750, elliptical=True, damage=self.getDamage(), damageplayer=False)
						#arrow = Component.arrow.copy()
						arrow.animate()
						self.depleteItem(self.selected)
					elif self.getSelectedVal('Type') == 'Weapon':
						self.damage = self.getDamage()
						
			self.attackcooldown += 1
		else:
			self.canteleport = True
		if game.BUTTON2 and (game.MOUSEPRESSED or game.KEYPRESSED):
			if self.getSelectedVal('Type') == 'Block':
				self.breakBlock()
				
			
		
	
	def drawOverheadDisplay(self):
		sizeBasedOnValue = lambda x: int((x/2.5)+40)
		
		if self.damagecooldown < 20:
			damagetakensize = sizeBasedOnValue(self.lastdamagetaken)
			write(game.screen, game.font, damagetakensize, game.width/2, game.height/2-self.height-damagetakensize/2, str(self.lastdamagetaken), (255, 0, 0), True)
		
		if self.attackcooldown < 20:
			damagedealtsize = sizeBasedOnValue(self.lastdamage)
			write(game.screen, game.font, damagedealtsize, game.width/2, game.height/2-self.height-damagedealtsize/2, str(self.lastdamage), (255, 255, 255), True)
		
	
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
			if block.world == self.world and not block.deleted:
				if not self.invincible:
					self.gainItem(block.name)
				block.deleted = True
				del block
		game.blocks.clear()
		
	


player1 = Player('Player 1 ')
