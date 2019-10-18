#!/usr/bin/python
from random import *
import pygame
from sys import *




def roundto(x, base):
	return base*round(float(x)/base)

def restrict(minvalue, value, maxvalue):
    return max(minvalue, min(value, maxvalue))


fonts = {}
def write(surface, fontFace, size, x, y, text, colour):
	if (size in fonts):
		Font = fonts[size]
	else:
		Font = pygame.font.SysFont(fontFace, size)
		fonts[size] = Font
	text = Font.render(text, 1, colour)
	surface.blit(text, (x, y))



class Game(object):
	
	def __init__(self):
		pygame.init()
		pygame.key.set_repeat() 
		pygame.display.set_caption('Life Simulator')
		pygame.mouse.set_visible(0)
		self.screen = pygame.display.set_mode()
		self.screen = pygame.display.set_mode((pygame.display.get_surface().get_size()[0],pygame.display.get_surface().get_size()[1]-60), pygame.RESIZABLE)
		self.screenwidth, self.screenheight = pygame.display.get_surface().get_size()
		self.running = True
		self.events = 0
		self.keys = 0
		self.KEYTAPPED = False
		self.KEYPRESSED = False
		self.BUTTON1 = False
		self.BUTTON2 = False
		self.SHIFT = False
		self.CONTROL = False
		self.mouse = 0
		self.MOUSECLICKED = False
		self.MOUSEPRESSED = False
		self.LEFT = 0
		self.RIGHT = 2
		self.MIDDLE = 1
		self.seconds = 0
		self.minutes = 0
		
	def end(self):
		self.running = False
		
	def keepTime(self):
		self.seconds = int(pygame.time.get_ticks()/1000)%60
		self.minutes = int((pygame.time.get_ticks()/1000)/60)%60
		
	def checkKeys(self):
		if (game.keys[pygame.K_e] or game.keys[pygame.K_RETURN] or game.keys[pygame.K_KP_ENTER]\
		or game.keys[pygame.K_RCTRL] or game.keys[pygame.K_KP0] or game.mouse[game.LEFT]):
			self.BUTTON1 = True
		else:
			self.BUTTON1 = False
		if (game.keys[pygame.K_f] or game.keys[pygame.K_KP_PERIOD] or game.mouse[game.RIGHT]):
			self.BUTTON2 = True
		else:
			self.BUTTON2 = False
			
		if (game.keys[pygame.K_LSHIFT] or game.keys[pygame.K_RSHIFT]):
			self.SHIFT = True
		else:
			self.SHIFT = False
			
		if (game.keys[pygame.K_LCTRL] or game.keys[pygame.K_RCTRL]):
			self.CONTROL = True
		else:
			self.CONTROL = False
	
	def resetInput(self):
		self.MOUSECLICKED = False
		self.KEYTAPPED= False
	
	def displayMessages(self):
		if not (player.living):
			#game.screen.fill((255, 0, 0))
			write(game.screen, 'font.ttf', int(game.screenwidth*0.15), int(game.screenwidth*0.3), int(game.screenheight*0.4), 'You died', (255, 255, 255))
			player.speed = 0
			if (self.MOUSECLICKED):
				self.end()
			
	def checkEvents(self):
		self.events = pygame.event.get()
		self.keys = pygame.key.get_pressed()
		self.mouse = pygame.mouse.get_pressed()
		self.checkKeys()
		game.keepTime()
		
		for event in self.events:
			if (event.type == pygame.QUIT):
				self.end()
			elif (event.type == pygame.VIDEORESIZE):
				self.screenwidth, self.screenheight = event.size
				player.center()
			elif (event.type == pygame.MOUSEBUTTONDOWN):
				#print(pygame.mouse.get_pos())
				#player.mouseclickevents()
				self.MOUSECLICKED = True
				self.MOUSEPRESSED = True
			elif (event.type == pygame.MOUSEBUTTONUP):
				self.MOUSEPRESSEDED = False
			elif (event.type == pygame.KEYDOWN):
				#player.keydownevents()
				game.KEYTAPPED = True
				game.KEYPRESSED = True
			elif (event.type == pygame.KEYUP):
				game.KEYPRESSED = False
			if (self.keys[pygame.K_ESCAPE]):
				pygame.display.iconify()
			if (self.keys[pygame.K_F11]):
				pygame.display.toggle_fullscreen()
				self.screenwidth, self.screenheight = pygame.display.get_surface().get_size()
				player.center()
		
game = Game()


class World(object):
	
	worlds = []
	
	def __init__(self, name,  width, height, color, exteriorcolor, tilesize, walled, iscircle, miniature, borderdamage = 0, borderspeed = 1):
		World.worlds.append(self)
		self.name = name
		self.width = width
		self.height = height
		self.color = color
		self.exteriorcolor = exteriorcolor
		self.tilesize = tilesize
		self.screenX = 0
		self.screenY = 0
		self.walled = walled
		self.iscircle = iscircle
		self.randX = 0
		self.randY = 0
		self.miniature = miniature
		self.borderdamage = borderdamage
		self.borderspeed = borderspeed
		
	def draw(self):
		game.screen.fill(self.exteriorcolor)
		self.screenX = player.x-(self.width/2) + (game.screenwidth/2)
		self.screenY = player.y-(self.height/2) + (game.screenheight/2)
		if (self.iscircle):
			shape = pygame.draw.ellipse
		else:
			shape = pygame.draw.rect
		shape(game.screen, self.color, (self.screenX, self.screenY, self.width, self.height))
		
	def genRandCoords(self):
		self.randX = randint(int(-player.currentworld.width/2), int(player.currentworld.width/2))
		self.randY= randint(int(-player.currentworld.height/2), int(player.currentworld.height/2))
		
	def randCoords(self):
		return (randint(int(-player.currentworld.width/2), int(player.currentworld.width/2)), randint(int(-player.currentworld.height/2), int(player.currentworld.height/2)))


# world definitions
town = World('Town', 10125, 10125, (86, 200, 76), (220, 200, 140), 100, False, False, False)
house_interior = World('House Interior', 1050, 850, (230, 210, 140), (100, 100, 255), 50, True, False, True)
shop_interior = World('Shop Interior', 1200, 1000, (230, 210, 140), (250, 100, 100), 50, True, False, True)
city = World('City', 7500, 7500, (120, 120, 120), (0, 100, 20), 100, False, False, False)
heck = World('Heck', 4000, 4000, (100, 35, 30), (255, 150, 0), 100, False, False, False, 5, 0.25) #no swearing on my christian minecraft server
cheese_land = World('Cheese Land', 3500, 3500, (255, 210, 75), (255, 175, 100), 75, False, True, False)
cave_land = World('Cave Land', 2500, 600, (90, 90, 90), (25, 25, 25), 75, True, False, True)
daddyland = World('Daddyland', 4200, 6900, (255, 195, 240), (255, 50, 170), 75, True, False, True, 0.1)
#island = World('Island', 2500, 6000, (220, 200, 140), (0, 100, 200), 75, False, True, False, 0.05)
#jungle = World('Jungle', 4000, 3800, (0, 100, 50), (30, 180, 100), 100, True, False, False)
#lake = World('Lake', 3000, 2500, (0, 100, 200), (25, 200, 100), 75, False, True, False)



class Character(object):
	
	characters = []
	
	def __init__(self, name, x, y, radius, color, iscircle=True):
		Character.characters.append(self)
		self.name = name
		self.x = x
		self.y = y
		self.radius = radius
		self.iscircle = iscircle
		self.color = color
		self.living = True
		self.health = 1000
		self.age = 0
		self.happiness = 0
		self.money = 0
		self.intelligence = 1
		self.weight = 100
		self.energy = 1000
		self.speed = 0
		self.walkingspeed = 0
		self.strength = 1
		self.screenX = 0; self.screenY  = 0
		self.statX = 0; self.statY = 0
		self.tophitbox = 0
		self.bottomhitbox = 0
		self.righthitbox = 0
		self.lefthitbox = 0
		self.touching = set([])
		self.docheats = True
		self.sprinting = False
		self.swimming = False
		self.invincible = False
		self.invisible = False
		self.indoors = False
		self.overborder = False
		self.cangointodebt = False
		self.canchangeworlds = True
		self.onground = True
		self.currentworld = town
		self.tileX = 0
		self.tileY = 0
		self.slot = 1
		self.selected = 'Hand'
		self.blockholding = ''
		self.inventory = {
		'Hand': {'Slot': 1, 'Type': 'Default', 'Amount': 1},
		'Stone': {'Slot': 2, 'Type': 'Block', 'Amount': 100},
		'Ground': {'Slot': 3, 'Type': 'Block', 'Amount': 100},
		'Dirt': {'Slot': 4, 'Type': 'Block', 'Amount': 100},
		'Rainbow': {'Slot': 5, 'Type': 'Block', 'Amount': 100},
		'Wood': {'Slot': 6, 'Type': 'Block', 'Amount': 100},
		'Sword': {'Slot': 0, 'Type': 'Weapon',  'Damage': 100, 'Amount': 1},
		'Shield': {'Slot': 0, 'Type': 'Armor', 'Protection': 50, 'Amount': 1},
		'Chips': {'Slot': 7, 'Type': 'Consumable', 'Amount': 4},
		'Energy Drink': {'Slot': 8, 'Type': 'Consumable', 'Amount' : 3},
		'Time Machine': {'Slot': 9, 'Type': 'Item', 'Amount': 1}
	}

	def draw(self):
		if self == player:
			self.center()
		else:
			self.screenX = player.x+(-(self.radius/2)) + (game.screenwidth/2)
			self.screenY = player.y-((self.radius/2)) + (game.screenheight/2)
		self.tileX = roundto(self.x, self.currentworld.tilesize)
		self.tileY = roundto(self.y, self.currentworld.tilesize)
		self.tophitbox = self.screenY-self.radius
		self.bottomhitbox = self.screenY+self.radius
		self.righthitbox = self.screenX+self.radius
		self.lefthitbox = self.screenX-self.radius
		color = self.color
		x = self.screenX
		y = self.screenY
		if (self.invisible):
			stroke = 1
			pygame.draw.circle(game.screen, (0, 0, 0), (x, y), 5, 3)
			pygame.draw.circle(game.screen, (255, 255, 255), (x, y), 4, 1)
		else:
			stroke = 0

		if (self.iscircle):
			pygame.draw.circle(game.screen, color, (x, y), int(self.radius), stroke)
		else:
			pygame.draw.rect(game.screen, color, (int(x-self.radius, y-self.radius), int(self.radius*2), self.radius*2), stroke)
		self.drawItems()
		
		
	def control(self):
		if (game.keys[pygame.K_UP] or game.keys[pygame.K_KP8] or game.keys[pygame.K_w]):  
			self.y += self.speed
		if  (game.keys[pygame.K_DOWN] or game.keys[pygame.K_KP2]  or game.keys[pygame.K_KP5] or game.keys[pygame.K_s]):
			self.y -= self.speed
		if (game.keys[pygame.K_RIGHT] or game.keys[pygame.K_KP6] or game.keys[pygame.K_d]):
			self.x -= self.speed
		if  (game.keys[pygame.K_LEFT] or game.keys[pygame.K_KP4] or game.keys[pygame.K_a]):
			self.x += self.speed
		self.playerEvents()
		self.useItems()

	def center(self):
		self.screenX = int(game.screenwidth/2)
		self.screenY = int(game.screenheight/2)
		
	def checkBorder(self):
		if (self.x > self.currentworld.width/2-player.radius) or (self.x < -self.currentworld.width/2-player.radius)\
		or (self.y > self.currentworld.height/2-player.radius) or (self.y < -self.currentworld.width/2-player.radius):
			self.overborder = True
			#print('Over the border!')
			if  (self.onground):
				self.health -= self.currentworld.borderdamage
		else:
			self.overborder = False
		if (self.currentworld.walled):
			#self.x = max(min(player.currentworld.width/2-player.radius, self.x), -player.currentworld.width/2+player.radius)
			#self.y = max(min(player.currentworld.height/2-player.radius, self.y), -player.currentworld.height/2+player.radius)
			self.x = restrict(-player.currentworld.width/2+player.radius, self.x, player.currentworld.width/2-player.radius)
			self.y  = restrict(-player.currentworld.height/2+player.radius, self.y, player.currentworld.height/2-player.radius)

	def playerEvents(self):
		self.deleteBlock()
		#self.drawItems()
		if (self.get_selected_val('Amount') > 0):
			self.placeBlock()
			#self.useItems()
		if (game.MOUSECLICKED or game.KEYTAPPED):
			self.doCheats()
			self.worldPortals()
			self.selectSlot()
			
	def useItems(self):
		if (self.get_selected_val('Amount') > 0):
			if (self.selected == 'Hand'):
				self.canchangeworlds = True
			else:
				self.canchangeworlds = False
			if (self.selected == 'Time Machine'):
				if (game.BUTTON1):
					self.age += 0.25
				if (game.BUTTON2):
					self.age -= 0.25
			if (game.MOUSECLICKED or game.KEYTAPPED):
				if (game.BUTTON1):
					if (self.selected == 'Chips'):
						self.energy += 10
						self.depleteItem('Chips')
					if (self.selected == 'Energy Drink'):
						self.energy += 100
						self.depleteItem('Energy Drink')
		else:
			self.canchangeworlds = True
	
	def drawItems(self):
		if (self.get_selected_val('Type') == 'Block'):
			width = self.currentworld.tilesize
			height = self.currentworld.tilesize
			x = player.x+(-self.tileX-(width/2))+(game.screenwidth/2)
			y = player.y-(self.tileY+(height/2))+(game.screenheight/2)
			#x =self.tileX#self.screenX-(width/2)
			#y = self.tileY#self.screenY-(height/2)
			pygame.draw.rect(game.screen, (0, 0, 0), (x, y, width, height), 1)
			theblock = self.selected
			color1 = self.get_block_val(theblock, 'Color1')
			color2 = self.get_block_val(theblock, 'Color2')
			color1 = self.setColor(color1)
			color2 = self.setColor(color2)
			width = 20
			height = 20
			xOffset = self.radius
			yOffset = 0
			pygame.draw.rect(game.screen, color2, (self.screenX-(width/2)-xOffset-1, self.screenY-(height/2)+yOffset-1, width+2, height+2))
			pygame.draw.rect(game.screen, color1, (self.screenX-(width/2)-xOffset, self.screenY-(height/2)+yOffset, width, height))

			
	def gainItem(self, item):
		if not (self.invincible):
			self.inventory[item]['Amount'] += 1
	
	def depleteItem(self, item):
		if (self.get_selected_val('Amount') > 0 and not self.invincible):
			self.inventory[item]['Amount'] -= 1
	
	def die(self):
		if (self.invincible == False):
			if (self.health > 0):
				self.health -= 10
			else:
				self.health = 0
				self.living = False
	
	
	def doCheats(self):
		if (self.docheats):
			if (game.SHIFT or game.keys[pygame.K_KP0]):
				self.sprinting = not self.sprinting
			if (game.CONTROL):
				if (game.keys[pygame.K_1]):
					self.cycleWorlds(-1)
				if (game.keys[pygame.K_2]):
					self.cycleWorlds()
				if (game.keys[pygame.K_c]):
					self.iscircle = not self.iscircle
				if (game.keys[pygame.K_h]):
					self.invisible = not self.invisible
				if (game.keys[pygame.K_i]):
					self.invincible = not self.invincible
				if (game.keys[pygame.K_b]):
					Statdisplay.shown = not Statdisplay.shown
				if (game.keys[pygame.K_3]):
					Block.is3D = not Block.is3D
					Block.sortBlocks()
				if (game.keys[pygame.K_m]):
					Block.sickomode = not Block.sickomode
				if (game.keys[pygame.K_v]):
					variable = input ('Which variable to change')
					value = int(input ('To what value?'))
					exec("self.{} = {}".format(variable, value))
				if (game.keys[pygame.K_9]):
					self.clearBlocks()
				if (game.keys[pygame.K_0]):
					self.living = False
	
	def get_item_val(self, item, key):
		return self.inventory.get(item).get(key)
	
	def get_selected_val(self, key):
		return self.get_item_val(self.selected, key) 
	
	def selectSlot(self):
		keys = (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9)
		for key in keys:
			if (game.keys[key] and not game.CONTROL):
				self.slot = keys.index(key)+1
				for item in self.inventory:
					if (self.get_item_val(item, 'Slot') == self.slot):
						self.selected = item

						
	def manageStats(self):
		speedmultiplier = 1
		if (self.overborder and self.onground):
			speedmultiplier *= self.currentworld.borderspeed
		self.walkingspeed = ((self.energy*0.00825)+10)*speedmultiplier
		#self.radius = int(self.weight*0.15)+8
		
		if (self.energy <= 0 or self.weight <= 0 or self.health <= 0):
			self.die()
			
		if (self.sprinting == True):
			if (self.swimming or self.currentworld.miniature):
				self.speed = self.walkingspeed*1 # sprinting while slowed
				self.energy -= 0.15
			else:
				self.speed = self.walkingspeed*2 # normal sprinting
				self.energy -= 0.15
		else:
			if (self.swimming or self.currentworld.miniature):
				self.speed = self.walkingspeed*0.60 # walking while slowed/in a small world
				self.energy -= 0.10
			else:
				self.speed = self.walkingspeed # walking normally
				self.energy -= 0.10
				
		if (self.cangointodebt == False):
			self.money = max(self.money, 0)
			
		if (self.invincible == True):
			self.health = 1000
			self.energy = 1000
			self.cangointodebt = True
		else:
			self.age += 0.0125
			self.cangointodebt = False
			
		self.checkBorder()
		self.health = max(0, self.health)
		self.energy = max(0, self.energy)
		self.weight = max(0, self.weight)
		self.checkBorder()
	
	def randPos(self, component):
		component.x = self.currentworld.randX
		component.y = self.currentworld.randY
		
	def collision(self):
		if (restaurant in self.touching and (self.money > 0 or self.cangointodebt == True)):
			self.weight += 0.5
			self.happiness += 0.5
			self.money -= 0.5
			self.energy += 0.5
			self.radius += 0.1
		if (gym in self.touching and (self.money > 0 or self.cangointodebt == True)):
			self.weight -= 0.5
			self.money -= 0.5
			self.happiness -= 0.25
			self.energy -= 0.5
			self.strength += 0.5
			self.radius -= 0.1
		if (school in self.touching and ((self.age >= 18 and (self.money > 0 or self.cangointodebt == True)) or self.age < 18)):
			self.intelligence += 0.75
			self.happiness -= 0.25
			if (self.age > 18):
				self.money -= 0.5
		if (office in self.touching):
			self.money += (0.5 * (self.intelligence/12)) + 0.5
			self.happiness -= 0.25
			self.energy -= 0.25
		if (bed in self.touching):
			self.happiness += 0.5
			self.energy += 1
		if (hospital in self.touching and (self.money > 0 or self.cangointodebt == True)):
			self.health += 2
			self.money -= 0.5
			if (self.weight <= 0):
				self.weight += 0.5
			if (self.energy <= 0):
				self.energy += 0.5
		if (cash in self.touching):
			self.money += 100
			self.randPos(cash)
		if (coin in self.touching):
			self.money += 10
			self.randPos(coin)
		if (pond  in self.touching or ocean  in self.touching or lava in self.touching):
			#self.swimming = True
			if (lava in self.touching):
				self.health -= 5
				
	def setWorld(self, world):
		self.currentworld = world
	
	def setPos(self, position):
		try:
			self.x = -position.x
			self.y = position.y
		except:
			self.x = -position[0]
			self.y = position[1]
			
	def cycleWorlds(self, direction = 1):
		if (direction > 0):
			if (World.worlds.index(player.currentworld) < len(World.worlds)-1):
				self.setWorld(World.worlds[World.worlds.index(player.currentworld)+direction])
			else:
				self.setWorld(World.worlds[0])
		elif (direction < 0):
			if (World.worlds.index(player.currentworld) < len(World.worlds)):
				self.setWorld(World.worlds[World.worlds.index(player.currentworld)+direction])
			else:
				self.setWorld(World.worlds[len(World.worlds)-1])
		self.setPos((0, 0))
				
	def portalTo(self, world, touching, position):
		if (touching in self.touching):
			#print('teleporting')
			self.setPos(position)
			self.setWorld(world)
	
	def worldPortals(self):
		if (game.BUTTON1 and self.canchangeworlds):
			self.portalTo(town, house_door, house)
			self.portalTo(town, shop_door, shop)
			self.portalTo(heck, lava, (0, 0))
			self.portalTo(cheese_land, cheese_hut, (0, 0))
			self.portalTo(house_interior, house, house_door)
			self.portalTo(shop_interior, shop, shop_door)
			self.portalTo(cave_land, cave, (0,0))
			self.portalTo(town, cave_exit, cave)
			self.portalTo(city, metro, (0,0))
	
	def get_block_val(self, theblock, key):
		if (key == 'Color1' or key == 'Color2'):
			key = self.setColor(key)
		return Block.blocktypes[theblock].get(key)
		
	def setColor(self, color):
		if (color == 'Ground Color'):
			color = self.currentworld.color
		elif (color == 'Exterior Color'):
			color = self.currentworld.exteriorcolor
		elif (color == 'Random Color'):
			color = Block.get_rainbow()
			#color = (color1[0]/2, color1[1]/2, color1[2]/2)
		return color
	
	def placeBlock(self):
		if (self.get_selected_val('Type') == 'Block' and self.get_selected_val('Amount') > 0):
			world = self.currentworld
			theblock = self.selected
			width = self.currentworld.tilesize
			height = self.currentworld.tilesize
			solid = True
			iscircle = False
			color1 = self.get_block_val(theblock, 'Color1')
			color2= self.get_block_val(theblock, 'Color2')
			color1 = self.setColor(color1)
			color2 = self.setColor(color2)
			if (game.keys[pygame.K_c]):
				iscircle = True
			placeable = True
			
			if (game.BUTTON1):
				for item in Block.blocks:
					if (item.x == self.tileX and item.y == self.tileY and item.deleted == False and item.world == self.currentworld):
						placeable = False
				if (placeable):
					try:
						newblock = Block(theblock, self.tileX, self.tileY, width, height, color1, world, solid, iscircle, color2)
					except:
						newblock = Block(theblock, self.tileX, self.tileY, width, height, (0, 0, 0), world, solid, iscircle, (255, 255, 255))
					if (Block.is3D == True):
						Block.sortBlocks()
					self.depleteItem(theblock)
					
	def deleteBlock(self):
		if (game.BUTTON2):
			for item in Block.blocks:
				if (item.x > self.tileX-self.radius and item.x < self.tileX+self.radius\
				and item.y > self.tileY-self.radius and item.y < self.tileY+self.radius and self.currentworld == item.world):
					if  not (item.deleted):
						Block.blocks.remove(item)
						if not(self.invincible):
							self.gainItem(item.name)
						item.deleted = True
					
	def clearBlocks(self):
		for item in Block.blocks:
			if not (item.deleted):
				Block.blocks.clear()
				if not(self.invincible):
					self.gainItem(item.name)
				item.deleted = True
	

player = Character('Player', -0, 0, 25, (255, 255, 0), True)


def control(entity):
	entity.control()

def manageCharacterStats():
	player.manageStats()
	#cop1.manageStats()
	#cop2.manageStats()
	#cop3.manageStats()
	
player.currentworld.genRandCoords()



class Component(object):
	
	components = []
	
	def __init__(self, name, x ,y, width, height, color, world, showname, iscircle):
		Component.components.append(self)
		self.name = name
		self.x = x - player.x
		self.y = y - player.y
		self.width = width
		self.height = height
		self.color = color
		self.world = world
		self.showname = showname
		self.iscircle = iscircle
		self.leftwall = 0
		self.rightwall = 0
		self.upperwall = 0
		self.lowerwall = 0
		self.screenX = 0
		self.screenY = 0
		self.solid = False
		self.playertouch = False
		
	def draw(self):
		if (self.world == player.currentworld):
			self.screenX = player.x+(self.x-(self.width/2))+(game.screenwidth/2)
			self.screenY = player.y-(self.y+(self.height/2))+(game.screenheight/2)
			if (self.iscircle):
				shape = pygame.draw.ellipse
			else:
				shape = pygame.draw.rect
			shape(game.screen, self.color, (self.screenX, self.screenY, self.width, self.height))
			textsize = 30
			if (self ==  cash):
				label = '   $'
				color = (200, 250, 200)
			else:
				label = self.name
				color = (255, 255, 255)
			if (self.showname == True):
				write(game.screen, 'font.ttf', textsize, self.screenX, self.screenY, label, color)
				
	def collision(self):
		self.leftwall = self.screenX
		self.rightwall = self.screenX+(self.width)
		self.upperwall = self.screenY
		self.lowerwall = self.screenY+(self.height)
		if ((player.righthitbox > self.leftwall and player.lefthitbox < self.rightwall\
		and player.tophitbox < self.lowerwall and player.bottomhitbox > self.upperwall)\
		and player.currentworld ==  self.world):
			player.touching.add(self)
			#print(player.touching)
			player.collision()
			#for component in player.touching:
				#print(component.name)
		else:
			player.touching.discard(self)
		
# Town components
# roads

h_sidewalk = Component('Horizontal sidewalk', 0, 0, town.width, 300, (185, 185, 185), town, False, False)
v_sidewalk = Component('Horizontal sidewalk', 0, 0, 300, town.height, (185, 185, 185), town, False, False)
h_road = Component('Horizontal road', 0, 0, town.width, 200, (50, 50, 50), town, False, False)
v_road = Component('Vertical road', 0, 0, 200, town.height, (50, 50, 50), town, False, False)

# features
pond = Component('Pond', 2000, 1650, 600, 465, (20, 150, 185), town, False, True)
pond_beach = Component('Pond Beach', 1900, 1650, 1000, 850, (204, 198, 148), town, False, True)
ocean = Component('Ocean', -2600, 2750, 200, 300, (10, 140, 165), town, False, True)
ocean_beach = Component('Ocean Beach', -2600, 2750, 300, 400, (204, 198, 148), town, False, True)
lava = Component('Lava', 3800, -3800, 250, 250, (240, 185, 30), town, False, True)
volcano = Component('Volcano', 3800, -3800, 1250, 1250, (165, 128, 138), town, False, True)
cave = Component('Cave', 3000,  4000, 650, 300, (190, 190, 190), town, False, False)

# buildings
house = Component('House', 900, 350, 300, 200, (100, 80, 50), town, True, False)
restaurant = Component('Restaurant', -450, 350, 400, 200, (160, 160, 160), town, True, False)
gym = Component('Gym', -900, 450, 300, 400, (135, 130, 140), town, True, False)
school = Component('School', 450, -400, 200, 300, (200, 175, 150), town, True, False)
office = Component('Office',  -500, -400, 300, 300, (160, 180, 180), town, True, False)
hospital = Component('Hospital', -400, 700, 300, 300, (210, 210, 210), town, True, False)
shop = Component('Shop', -950, -400, 400, 300, (250, 100, 100),  town, True, False)
metro = Component('Metro', 2000, 600, 300, 400, (100,100, 100), town, True, False)

# items
cash = Component('Cash', town.randX, town.randY, 50, 23, (100, 150, 100), town, True, False)


# House components
bed = Component('Bed', 200, 200, 80, 120, (255, 0, 0), house_interior, False, False)
house_door = Component('House Door', -house_interior.width/2, 0, 20, 120, (110, 78, 48), house_interior, False, False)
# house items
coin = Component('Coin', house_interior.randX, house_interior.randY, 20, 20, (185, 185, 185), house_interior, False, True)

# Shop components
shop_door = Component('Shop Door', 0, shop_interior.height/2, 120, 20, (110, 78, 48), shop_interior, False, False)

# shop items


# City components


# city buildings
cheese_hut = Component('Cheese Hut', 1000, 5010,  200, 200, (255, 250, 75), city, True, True)
#bank = Component('Bank', 750, 800, 250, 300, (25, 150, 75), city, True, False)
#apartment = Component('Apartment',)
#university = Component
# city items

# Cave components
cave_exit = Component('Cave Exit', -cave_land.width/2, 0, 20, cave_land.height, (0, 0, 0), cave_land, False, False)


class Block(object):
	count = 0
	blocks = []
	is3D = True
	blocktypes = {
		'Stone': {
			'ID': 0,
			'Color1': (150, 150,150),
			'Color2' : (100, 100, 100)
		},
		'Ground': {
			'ID': 1,
			'Color1': 'Ground Color',
			'Color2': 'Exterior Color'
		},
		'Dirt': {
			'ID': 2,
			'Color1': 'Exterior Color',
			'Color2' : 'Ground Color'
		},
		'Rainbow': {
		'ID': 3,
		'Color1': 'Random Color',
		'Color2': 'Random Color'
		},
		'Wood': {
		'ID': 4,
		'Color1':  (230, 185, 120),
		'Color2':  (210, 155, 100)	
		}#,
	}
	rmin = 100
	rmax = 255
	#width = 100#world.width/200
	#height = 100#world.height/200
	thickness = 2
	sickomode = False
	
	@classmethod
	def sortBlocks(cls):
		if (Block.is3D):
			Block.blocks.sort(key = lambda theblock: -theblock.y) # orders 3d block by y so they dont overlap
	
	@classmethod
	def get_rainbow(cls):
		return (randint(Block.rmin, Block.rmax), randint(Block.rmin, Block.rmax), randint(Block.rmin, Block.rmax))
		
	
	def __init__(self, name, x, y, width, height, color1, world, solid, iscircle, color2):
		self.name = name
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.color1 = color1
		self.color2 = color2
		self.world = player.currentworld
		self.solid = solid
		self.iscircle = iscircle
		self.leftwall = 0
		self.rightwall = 0
		self.upperwall = 0
		self.lowerwall = 0
		self.screenX = 0
		self.screenY = 0
		self.playertouch = False
		self.deleted = False
		Block.count += 1
		Block.blocks.append(self)
		self.bordered = True
		self.tallness = 0
	
	def draw(self):
		if (self.bordered):
			thickness = Block.thickness
		else:
			thickness = 0
		self.tallness = int(player.currentworld.tilesize/3)
		if (self.world == player.currentworld and self.deleted == False):
			self.screenX = player.x+(-self.x-(self.width/2))+(game.screenwidth/2)
			self.screenY = player.y-(self.y+(self.height/2))+(game.screenheight/2)
			if (self.iscircle):
				shape = pygame.draw.ellipse
			else:
				shape = pygame.draw.rect
			if (Block.sickomode and self.name == 'Rainbow'):
				self.color1 = Block.get_rainbow()
				self.color2 = Block.get_rainbow()
			if (Block.is3D):
				shape(game.screen, self.color2, (self.screenX, self.screenY-self.tallness, self.width, self.height+self.tallness)) # block side
				shape(game.screen, self.color1, (self.screenX+(thickness/2), self.screenY+(thickness/2)-self.tallness, self.width-thickness, self.height-thickness)) #block top
			else:
				shape(game.screen, self.color2, (self.screenX, self.screenY, self.width, self.height)) # block border
				shape(game.screen, self.color1, (self.screenX+(thickness/2), self.screenY+(thickness/2), self.width-thickness, self.height-thickness)) # block
	
	def collision(self):
		self.leftwall = self.screenX
		self.rightwall = self.screenX+(self.width)
		self.upperwall = self.screenY
		self.lowerwall = self.screenY+(self.height)
		if ((player.righthitbox > self.leftwall and player.lefthitbox < self.rightwall\
		and player.tophitbox < self.lowerwall and player.bottomhitbox > self.upperwall)\
		and player.currentworld ==  self.world):
			player.touching.add(self)
			player.onground = False
			#print(player.touching)
			#player.collision()
		else:
			player.touching.discard(self)
		onground = True
		for item in player.touching:
			if (self.name in Block.blocktypes):
				onground = False
				break
		player.onground = onground
		#print(player.onground)
	


class Statdisplay(object):
	startposition = 3
	shown = True
	
	def __init__(self, name, stat):
		self.name = name
		self.stat = stat
		self.spacing = 17
		self.x = 5
		self.y = 0
		
	def draw(self, position):
		stat = self.stat
		self.y = game.screenheight-(position*self.spacing) - self.startposition
		#if (self.name == 'X' or self.name == 'Y'):##stat /= 10;
		#if (self.name == 'X'): # flips x because that's backwards for some reason
			#stat = -stat
		if (type(stat) == float or type(stat) == int):
			stat = int(stat)
		label = (self.name + ':  ' + str(stat))
		textsize = 25
		if (self.name == 'Time elapsed'):
			minutesFormatting = str(game.minutes)
			secondsFormatting = str(game.seconds)
			if (game.minutes <= 9):
				minutesFormatting = '0' + str(game.minutes)
			if (game.seconds <= 9):
				secondsFormatting = '0' + str(game.seconds)
			label = (self.name + ': ' + minutesFormatting + ':' + secondsFormatting)
		if (Statdisplay.shown):
			write(game.screen, 'font.ttf', textsize, self.x, self.y, label, (255, 255, 255))
		

def displayStats():
	timestat = Statdisplay('Time elapsed', game.seconds)
	worldstat = Statdisplay('World', player.currentworld.name)
	xstat = Statdisplay('X', -player.x)
	ystat = Statdisplay('Y', player.y)
	itemstat = Statdisplay('Item selected', player.selected+' ('+str(player.get_selected_val('Amount'))+')'+' Type: '+str(player.get_selected_val('Type')))
	healthstat = Statdisplay('Health', player.health)
	agestat = Statdisplay('Age', player.age)
	energystat = Statdisplay('Energy', player.energy)
	weightstat = Statdisplay('Weight', player.weight)
	strengthstat = Statdisplay('Strength', player.strength)
	happinessstat = Statdisplay('Happiness', player.happiness)
	intelstat = Statdisplay('Intelligence', player.intelligence)
	moneystat = Statdisplay('Cash', player.money)
	
	displayedstats = (
	timestat, worldstat, xstat, ystat, itemstat,
	healthstat, agestat, energystat, weightstat, strengthstat, happinessstat, intelstat, moneystat
	)
	
	for stat in displayedstats:
		stat.draw(len(displayedstats)-displayedstats.index(stat))



def draw(entity):
	if not (type(entity) == tuple or type(entity) == list):
		entity.draw()
	else:
		for item in entity:
			item.draw()

def collisions(entity):
	if not (type(entity) == tuple or type(entity) == list):
		entity.collision()
	else:
		for item in entity:
			item.collision()


def drawgame():
	draw(player.currentworld)
	draw(Component.components)
	draw(Block.blocks)
	draw(player)
	displayStats()
	game.displayMessages()

def testCollisions():
	collisions(Component.components)
	collisions(Block.blocks)


def debug(do):
	if (do):
		#print(player.touching)
		print(player.onground)
		print(player.speed)
		

while (game.running):
		
	game.checkEvents()
	player.currentworld.genRandCoords()
	control(player)
	manageCharacterStats()
	
	drawgame()
	testCollisions()
	#debug(True)
	
	
	game.resetInput()
	pygame.display.update()
print('Game ended')
pygame.quit()
