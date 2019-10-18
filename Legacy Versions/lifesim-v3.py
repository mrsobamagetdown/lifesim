#!/usr/bin/python
from random import *
import pygame
#from sys import *



def roundto(x, base):
	return base*round(float(x)/base)
	
def restrict(minvalue, value, maxvalue):
    return max(minvalue, min(value, maxvalue))


fonts = {}
def write(surface, fontFace, size, x, y, text, colour, center=False):
	if size in fonts:
		Font = fonts[size]
	else:
		Font = pygame.font.SysFont(fontFace, size)
		fonts[size] = Font
	text = Font.render(text, 1, colour)
	if center:
		text_rect = text.get_rect(center=(x, y))
	else:
		text_rect = (x, y)
	surface.blit(text, text_rect)
	
	

class Game(object):
	
	def __init__(self):
		pygame.init()
		pygame.key.set_repeat() 
		pygame.display.set_caption('Life Simulator')
		pygame.mouse.set_visible(0)
		self.widthreduc = 6
		self.heightreduc = 32
		self.screen = pygame.display.set_mode()
		self.fullscreen = False
		self.screen = pygame.display.set_mode((pygame.display.get_surface().get_size()[0]-self.widthreduc,\
			pygame.display.get_surface().get_size()[1]-self.heightreduc), pygame.RESIZABLE)
		self.screenwidth, self.screenheight = pygame.display.get_surface().get_size()
		self.smallwidth, self.smallheight = self.screenwidth, self.screenheight
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
		self.COOLDOWN = 0
		self.LEFT = 0
		self.RIGHT = 2
		self.MIDDLE = 1
		self.seconds = 0
		self.minutes = 0
		self.clock = pygame.time.Clock()
		self.frames = 0
		self.toggleFullscreen(self.fullscreen)
		self.hacking = False
		self.command = ''
		self.docheats = True
		self.message = ''
		self.loopitems = []
	
	def play(self):
		self.loop()
		self.draw()

	def draw(self):
		player.world.draw()
		for thing in self.loopitems:
			for item in thing:
				if item.world == player.world:
					item.draw()
		Stat.drawStats()
		if self.message:
			self.displayMessage(self.message, int(self.screenwidth*0.15))
			self.message = ''
		pygame.display.update()
		
	def loop(self):
		self.checkEvents()
		Block.retrieveBlocktypes()
		Stat.retrieveStats()
		for thing in reversed(self.loopitems):
			for item in thing:
				#if item.world == player.world:
				item.loop()
		debug()
		player.resetAttackStats()
		self.resetInput()
			
	def get_screen_size(self):
		return pygame.display.get_surface().get_size()
		
	def setScreenSize(self):
		self.screenwidth, self.screenheight = self.get_screen_size()

	def toggleFullscreen(self, full):
		if full:
			self.screen = pygame.display.set_mode((1920, 1080), pygame.NOFRAME)
		else:
			self.screen = pygame.display.set_mode((1920-self.widthreduc,  1080-(self.heightreduc*2)), pygame.RESIZABLE)
		self.setScreenSize()
		
	def keepTime(self):
		self.seconds = int(pygame.time.get_ticks()/1000)%60
		self.minutes = int((pygame.time.get_ticks()/1000)/60)%60
		self.frames += 1
		self.clock.tick()
		
	def checkKeys(self):
		if game.keys[pygame.K_e] or game.keys[pygame.K_RETURN] or game.keys[pygame.K_KP_ENTER]\
		or game.keys[pygame.K_RCTRL] or game.keys[pygame.K_KP0] or game.mouse[game.LEFT]:
			self.BUTTON1 = True
			#self.COOLDOWN = 0
		else:
			self.BUTTON1 = False
		if game.keys[pygame.K_f] or game.keys[pygame.K_KP_PERIOD] or game.mouse[game.RIGHT]:
			self.BUTTON2 = True
			self.COOLDOWN = 0
		else:
			self.BUTTON2 = False
		if game.keys[pygame.K_LSHIFT] or game.keys[pygame.K_RSHIFT]:
			self.SHIFT = True
		else:
			self.SHIFT = False
		if game.keys[pygame.K_LCTRL] or game.keys[pygame.K_RCTRL]:
			self.CONTROL = True
		else:
			self.CONTROL = False
	
	def resetInput(self):
		self.MOUSECLICKED = False
		self.KEYTAPPED = False
	
	def displayMessage(self, message, size=200):
		write(game.screen, 'font.ttf', size, int(self.screenwidth/2), int(self.screenheight/2), message, (255, 255, 255), True)
	
	def pause(self):
		pause = input('Game paused. Press enter to resume.')
	
	def keyDown(self):
		if self.keys[pygame.K_ESCAPE]:
			pygame.display.iconify()
			#self.pause()
		if self.keys[pygame.K_F11]:
			self.fullscreen = not self.fullscreen
			self.toggleFullscreen(self.fullscreen)
			player.center()
			
	def hack(self, anevent):
		if self.hacking == True:
			#print('hacking')
			self.command += anevent.unicode
			print('>> ' + self.command)
			if self.keys[pygame.K_RETURN]:
				print(self.command)
				try:
					exec("{}".format(self.command))
					print('Command executed successfully.')
				except:
					print("Command failed.")
				self.hacking= False
				self.command = ''
	
	def cheats(self):
		if self.docheats:
			if self.SHIFT or self.keys[pygame.K_KP0]:
				player.sprinting = not player.sprinting
			if self.CONTROL:
				if self.keys[pygame.K_1]:
					player.cycleWorlds(-1)
				if self.keys[pygame.K_2]:
					player.cycleWorlds()
				if self.keys[pygame.K_3]:
					player.elliptical = not player.elliptical
				if self.keys[pygame.K_4]:
					player.invisible = not player.invisible
				if self.keys[pygame.K_5]:
					player.invincible = not player.invincible
					player.superstrength = not player.superstrength
					if player.superstrength:
						player.strength += 1000
					else:
						player.strength -= 1000
				if self.keys[pygame.K_6]:
					Stat.shown = not Stat.shown
				if self.keys[pygame.K_7]:
					#Component.showname = not Component.showname
					Stat.detailed = not Stat.detailed
				if self.keys[pygame.K_8]:
					Block.is3D = not Block.is3D
					Block.sortBlocks()
				if self.keys[pygame.K_9]:
					player.clearBlocks()
				if self.keys[pygame.K_0]:
					player.living = not player.living
				if self.keys[pygame.K_m]:
					Block.sickomode = not Block.sickomode
				if self.keys[pygame.K_n]:
					self.hacking = True
	
	def timeMachine(self):
		if self.keys[pygame.K_MINUS]:
			player.age -= 0.5
		if self.keys[pygame.K_EQUALS]:
			player.age += 0.5
	
	def checkEvents(self):
		self.events = pygame.event.get()
		self.keys = pygame.key.get_pressed()
		self.mouse = pygame.mouse.get_pressed()
		self.checkKeys()
		self.keepTime()
		self.timeMachine()
		self.COOLDOWN += 1
		#self.setScreenSize()
		#if not(self.fullscreen):
			#self.smallwidth, self.smallheight = self.get_screen_size()
		for event in self.events:
			if event.type == pygame.QUIT:
				self.running = False
			elif event.type == pygame.VIDEORESIZE:
				self.screenwidth, self.screenheight = event.size
				self.smallwidth, self.smallheight = event.size
				player.center()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				#print(pygame.mouse.get_pos())
				self.MOUSECLICKED = True
				self.MOUSEPRESSED = True
			elif event.type == pygame.MOUSEBUTTONUP:
				self.MOUSEPRESSED = False
			elif event.type == pygame.KEYDOWN:
				self.KEYTAPPED = True
				self.KEYPRESSED = True
				self.keyDown()
				self.hack(event)
				self.cheats()
			elif event.type == pygame.KEYUP:
				self.KEYPRESSED = False


game = Game()



class World(object):
	
	worlds = []
	shownworlds = []
	defaultslip = 0.3
	
	def __init__(self, name,  width, height, color, exteriorcolor, wallcolor, tilesize, walled, elliptical, miniature, wallwidth=0, borderdamage=0, borderspeed=1, slip=defaultslip):
		World.worlds.append(self)
		self.name = name
		self.width = width
		self.height = height
		self.color = color
		self.exteriorcolor = exteriorcolor
		self.wallcolor = wallcolor
		self.tilesize = tilesize
		self.screenX = 0
		self.screenY = 0
		self.walled = walled
		self.elliptical = elliptical
		self.miniature = miniature
		self.wallwidth = wallwidth
		self.borderdamage = borderdamage
		self.borderspeed = borderspeed
		self.slip = slip
		World.shownworlds.append(self)
		
			
	def draw(self):
		game.screen.fill(self.exteriorcolor)
		self.screenX = player.x-(self.width/2) + (game.screenwidth/2)
		self.screenY = player.y-(self.height/2) + (game.screenheight/2)
		
		if self.elliptical:
			shape = pygame.draw.ellipse
		else:
			shape = pygame.draw.rect
		if self.wallwidth and self.wallcolor:
			shape(game.screen, self.wallcolor, (self.screenX-self.wallwidth, self.screenY-self.wallwidth, self.width+self.wallwidth*2, self.height+self.wallwidth*2))
		shape(game.screen, self.color, (self.screenX, self.screenY, self.width, self.height))
		
	def randCoords(self):
		return (randint(int(-self.width/2), int(self.width/2)), randint(int(-self.height/2), int(self.height/2)))
	
	def randX(self):
		return(randint(int(-self.width/2), int(self.width/2)))
	
	def randY(self):
		return(randint(int(-self.height/2), int(self.height/2)))
		

# world definitions
town = World('Town', 6500, 6500, (86, 200, 76), (220, 200, 140), (220, 200, 140), 100, False, False, False)
house_interior = World('House Interior', 1050, 850, (230, 210, 140), town.color, (100, 80, 25), 50, True, False, True, 75)
shop_interior = World('Shop Interior', 1200, 750, (230, 210, 140), town.color, (250, 100, 100), 50, True, False, True, 75)
city = World('City', 5500, 5500, (170, 170, 170), (110, 220, 130), (), 100, False, False, False)
apartment_interior = World('Apartment Interior', 1000, 1500, (220, 200, 140), city.color, (200, 140, 50), 50, True, False, True, 75)
farm = World("Farm", 5000, 5000, (80, 220, 120), (200, 190, 70), (), 100, False, False, False, 0, 0, 0.5)
snowland = World('Snowland', 6000, 6000, (180, 220, 230), (100, 75, 40), (), 100, False, False, False)
heck = World('Heck', 4000, 4000, (100, 35, 30), (255, 150, 0), (), 100, False, False, False, False, 6, 0.5) #no swearing on my christian minecraft server
cheese_land = World('Cheese Land', 3500, 3500, (255, 210, 75), (255, 175, 100), (), 75, False, True, False)
cave_world = World('Cave World', 3000, 1000, (90, 90, 90), (25, 25, 25), (), 75, True, False, True)
daddyland = World('Daddyland', 6900, 4200, (255, 195, 240), (255, 50, 170),  (), 75, True, False, False, True, 0.1)
#island = World('Island', 2500, 6000, (220, 200, 140), (0, 100, 200), 75, False, True, False, 0.05)
#jungle = World('Jungle', 4000, 3800, (0, 100, 50), (30, 180, 100), 100, True, False, False)
#lake = World('Lake', 3000, 2500, (0, 100, 200), (25, 200, 100), 75, False, True, False)



class Character(object):
	
	characters = []
	
	def __init__(self, name, x, y, radius, color, elliptical=True, imagename='meh.png', basespeed=4):
		Character.characters.append(self)
		self.name = name
		self.x = x
		self.y = y
		self.radius = radius
		self.elliptical = elliptical
		self.color = color
		self.living = True
		self.health = 1000
		self.age = 0
		self.happiness = 0
		self.money = 0
		self.intelligence = 1
		self.weight = 100
		self.energy = 1000
		self.basespeed = basespeed
		self.speed = 0
		self.xmomentum = 0
		self.ymomentum = 0
		self.walkingspeed = 0
		self.strength = 1
		self.screenX = 0; self.screenY  = 0
		self.statX = 0; self.statY = 0
		self.tophitbox = 0
		self.bottomhitbox = 0
		self.righthitbox = 0
		self.lefthitbox = 0
		self.touching = set([])
		self.imagename = imagename
		if imagename:
			self.image = pygame.image.load(self.imagename)
		self.sprinting = False; self.swimming = False
		self.invincible = False; self.superstrength = False; self.invisible = False
		self.indoors = False
		self.overborder = False
		self.cangointodebt = False; self.canteleport = True
		self.onground = True
		self.damage = 0
		self.lastdamage = 0
		self.damagetaken = 0
		self.lastdamagetaken = 0
		self.damagecooldown = 0
		self.lasthealth = 0
		#self.coolness = 0
		self.world = town
		self.tileX = 0; self.tileY = 0
		self.slot = 1
		self.selected = 'Hand'
		self.blockholding = ''
		self.inventory = {
			'Hand': { 
				'Slot': 1,
				'Type': 'Weapon',
				'Amount': 1,
				'Damage': 1,
				'Depletable': False
			},
			'Stone': {
				'Slot': 2,
				'Type': 'Block',
				'Amount': 0, 
				'Depletable': True,
			 },
			'Ground': { 
				'Slot': 3,
				'Type': 'Block',
				'Amount': 100,
				'Depletable': True,
			},
			'Dirt': {
				'Slot': 4,
				'Type': 'Block',
				'Amount': 100,
				'Depletable': True,
			},
			'Rainbow': {
				'Slot': 5,
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
				'Slot': 8,
				'Type': 'Weapon',
				'Damage': 100, 
				'Amount': 1,
				'Depletable': False,
			},
			'Shield': {
				'Slot': 0, 
				'Type': 'Armor',
				'Protection': 0.5,
				'Amount': 1,
				'Depletable': False,
			},
			'Chips': {
				'Slot': 7,
				'Type': 'Consumable',
				'Amount': 50,
				'Stat': 'self.energy', 
				'Value': 100,
				'Depletable': True,
			},
			'First Aid Kit': {
				'Slot': 9,
				'Type': 'Consumable', 
				'Amount' : 5,
				'Stat': 'self.health',
				'Value': 200,
				'Depletable': True,
			},
		}


	def draw(self):
		if self is player:
			self.center()
		else:
			self.screenX = player.x+(-(self.radius/2)) + (game.screenwidth/2)
			self.screenY = player.y-((self.radius/2)) + (game.screenheight/2)
		self.tileX = roundto(self.x, self.world.tilesize)
		self.tileY = roundto(self.y, self.world.tilesize)
		self.tophitbox = self.screenY-self.radius
		self.bottomhitbox = self.screenY+self.radius
		self.righthitbox = self.screenX+self.radius
		self.lefthitbox = self.screenX-self.radius
		color = self.color
		x = self.screenX
		y = self.screenY
		if self.invisible:
			stroke = 2
			pygame.draw.circle(game.screen, (0, 0, 0), (x, y), 5, 3)
			pygame.draw.circle(game.screen, (255, 255, 255), (x, y), 4, 1)
		else:
			stroke = 0
		if self.elliptical:
			pygame.draw.circle(game.screen, color, (x, y), int(self.radius), stroke)
		else:
			pygame.draw.rect(game.screen, color, (int(x-self.radius), int(y-self.radius), int(self.radius*2), int(self.radius*2)), stroke)
		if self.imagename:
			self.image = pygame.transform.scale(self.image, (int(self.radius*2), int(self.radius*2)))
			game.screen.blit(self.image, (x-self.radius, y-self.radius))#, self.radius, self.radius))
		self.drawItems()
	
	def loop(self):
		player.control()
		player.manageSpeed()
		self.manageStats()
		self.manageImage()
		self.onground = not self.touching
		player.collectables()
		if game.MOUSEPRESSED or game.KEYPRESSED:
			player.useItems()
			player.deleteBlock()
			player.placeBlock()
		if self.touching:
			self.collision()
		if (game.MOUSECLICKED or game.KEYTAPPED):
			player.portals()
			player.selectSlot()
		self.checkBorder()
		
	def control(self):
		xmoved = False
		ymoved = False
		if game.keys[pygame.K_UP] or game.keys[pygame.K_KP8] or game.keys[pygame.K_w]:  
			self.ymomentum = -self.speed
			self.y += self.speed
			ymoved = True
		if  game.keys[pygame.K_DOWN] or game.keys[pygame.K_KP2]  or game.keys[pygame.K_KP5] or game.keys[pygame.K_s]:
			self.ymomentum = self.speed
			self.y -= self.speed
			ymoved = True
		if game.keys[pygame.K_RIGHT] or game.keys[pygame.K_KP6] or game.keys[pygame.K_d]:
			self.xmomentum = self.speed
			self.x -= self.speed
			xmoved = True
		if  game.keys[pygame.K_LEFT] or game.keys[pygame.K_KP4] or game.keys[pygame.K_a]:
			self.xmomentum = -self.speed
			self.x += self.speed
			xmoved = True
		slip = 0
		if self.touching:
			for thing in self.touching:
				#if component.slip > slip: # tries to find max slipperyness regardless of which thing is on top
				slip = thing.slip # actually tries to find slipperyness of the one the character is directly on top of (on the highest layer)
		else:
			slip = self.world.slip
		if not xmoved:	
			self.x -= self.xmomentum
			self.xmomentum *= slip
		if not ymoved:
			self.ymomentum *= slip
			self.y -= self.ymomentum
	
	
	def center(self):
		self.screenX = int(game.screenwidth/2)
		self.screenY = int(game.screenheight/2)
	
	def checkBorder(self):
		if (self.x > self.world.width/2-player.radius) or (self.x < -self.world.width/2-player.radius)\
		or (self.y > self.world.height/2-player.radius) or (self.y < -self.world.width/2-player.radius):
			self.overborder = True
			#print('Over the border!')
			if  self.onground:
				self.health -= self.world.borderdamage
		else:
			self.overborder = False
		if self.world.walled:
			#self.x = max(min(player.world.width/2-player.radius, self.x), -player.world.width/2+player.radius)
			#self.y = max(min(player.world.height/2-player.radius, self.y), -player.world.height/2+player.radius)
			self.x = restrict(-player.world.width/2 + player.radius, self.x, player.world.width/2 - player.radius)
			self.y  = restrict(-player.world.height/2 + player.radius, self.y, player.world.height/2 - player.radius)
			
	def useItems(self):
		if self.get_selected_val('Amount') > 0:
			if self.selected == 'Hand':
				self.canteleport = True
			else:
				self.canteleport = False
			if game.MOUSECLICKED or game.KEYTAPPED:
				if game.BUTTON1:
					if self.get_selected_val('Type') == 'Consumable':
						exec(self.get_selected_val("Stat") + ' += self.get_selected_val("Value")')
					if self.get_selected_val('Depletable') == True:
						self.depleteItem(self.selected)
				if game.BUTTON2:
					if self.get_selected_val('Type') == 'Weapon':
						basedamage = self.get_selected_val('Damage')
						damage = basedamage + int(self.strength-0.5)
						self.damage = damage
		else:
			self.canteleport = True
	
	def drawItems(self):
		if self.get_selected_val('Type') == 'Block':
			width = self.world.tilesize
			height = self.world.tilesize
			x = player.x + (-self.tileX - width/2) + (game.screenwidth/2)
			y = player.y - (self.tileY + height/2) + (game.screenheight/2)
			#x =self.tileX#self.screenX-(width/2)
			#y = self.tileY#self.screenY-(height/2)
			pygame.draw.rect(game.screen, (0, 0, 0), (x, y, width, height), 1)
			theblock = self.selected
			color1 = self.get_block_val(theblock, 'Color1')
			color2 = self.get_block_val(theblock, 'Color2')
			width = 20
			height = 20
			xOffset = -(self.radius - 10) 
			yOffset = 20
			pygame.draw.rect(game.screen, color2, (self.screenX - width/2 - xOffset-1, self.screenY - height/2 + yOffset-1, width+2, height+2))
			pygame.draw.rect(game.screen, color1, (self.screenX - width/2 - xOffset, self.screenY - height/2 + yOffset, width, height))
		if self.get_selected_val('Type') == 'Weapon':
			self.showAttack()
		self.showDamage()

	def displayText(self, text, size=40, color=(255, 255, 255)):
		write(game.screen, 'font.ttf', size, game.screenwidth/2, game.screenheight/2-self.radius-size/2, str(text), color, True)
		
	def gainItem(self, item, amount=1):
		self.inventory[item]['Amount'] += amount
	
	def depleteItem(self, item, amount=1):
		if self.get_selected_val('Amount') >= amount and not self.invincible:
			self.inventory[item]['Amount'] -= amount
			return True
		return False
	
	def get_item_val(self, item, key):
		return self.inventory.get(item).get(key)
	
	def get_selected_val(self, key):
		return self.get_item_val(self.selected, key) 
	
	def selectSlot(self):
		keys = (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9)
		for key in keys:
			if game.keys[key] and not game.CONTROL:
				self.slot = keys.index(key)+1
				for item in self.inventory:
					if self.get_item_val(item, 'Slot') == self.slot:
						self.selected = item

	def manageSpeed(self):
		speedmultiplier = 1
		if self.overborder and self.onground:
			speedmultiplier *= self.world.borderspeed
		for thing in self.touching:
			self.speed = thing.playerspeed
		speedmultiplier *= (((self.world.width+self.world.height)/2)/9150)+1
		self.walkingspeed = ((self.energy*0.012)+self.basespeed)*speedmultiplier
		if self.sprinting == True:
				self.speed = self.walkingspeed*2 # normal sprinting
				self.energy -= 0.30
		else:
				self.speed = self.walkingspeed # walking normally
				self.energy -= 0.15
				
	def manageStats(self):
		if self.energy <= 0 or self.weight <= 0:# or self.age >= 120:
			self.health -= 2
		if self.health <= 0:
			self.living = False
		if self.living == False:
			game.message = 'You died!'
			self.speed = 0
			self.basespeed = 0
		if self.cangointodebt == False:
			self.money = max(self.money, 0)
		if self.invincible:
			self.health = 1000
			self.energy = 1000
			self.cangointodebt = True
		else:
			self.age += 0.01
			self.cangointodebt = False
		self.health = max(0, self.health)
		self.energy = max(0, self.energy)
		self.weight = max(0, self.weight)
	
	def showAttack(self):
		if game.COOLDOWN  < 3:
			self.displayText(self.lastdamage, int((self.lastdamage/2)+40))
		
	def showDamage(self):
		if self.damagecooldown < 3 and self.lastdamagetaken > 0 and not self.invincible:
			self.displayText(self.lastdamagetaken, int((self.lastdamagetaken/2)+40), (255, 0, 0))
		self.damagecooldown += 1
		
	def resetAttackStats(self):
		if self.damage > 0:
			self.lastdamage = self.damage
		self.damage = 0
		if self.lasthealth != self.health:
			self.damagetaken = self.lasthealth - self.health
			self.damagecooldown = 0
		self.lasthealth = self.health
		if self.damagetaken > 0:
			self.lastdamagetaken = self.damagetaken
	
	def manageImage(self):
		if self.happiness >= 200:
			image = 'coolio'
		elif self.happiness >= 100:
			image = 'happy'
		elif self.happiness > 50:
			image = 'meep'
		elif self.happiness <= -200:
			image = 'cry'
		elif self.happiness <= -100:
			image = 'scared' 
		elif self.happiness <= -50:
			image = 'pissed'
		else:
			image = 'meh'
		if not self.living:
			image = 'dead'
		self.imagename = image + '.png'
		self.image = pygame.image.load(self.imagename)

	def collision(self):
		canafford = (self.money > 0 or self.cangointodebt == True)
		if restaurant in self.touching and (self.money > 0 or self.cangointodebt == True):
			self.weight += 0.5
			self.happiness += 1
			self.money -= 0.5
			self.energy += 0.5
			self.radius += 0.1
		if gym in self.touching and (self.money > 0 or self.cangointodebt == True):
			self.weight -= 0.5
			self.money -= 0.5
			self.happiness -= 0.25
			self.energy -= 0.5
			self.strength += 0.5
			self.radius -= 0.025
		if school in self.touching:
			self.intelligence += 0.75
			self.happiness -= 0.25
		if university in self.touching and (self.age > 18):
			self.money -= 0.75
			self.intelligence += 1.5
			self.happiness -= 0.5
		if office in self.touching:
			self.money += (0.5 * (self.intelligence/12)) + 0.5
			self.happiness -= 0.5
			self.energy -= 0.5
		if bed in self.touching:
			self.happiness += 1
			self.energy += 1
		if hospital in self.touching and (self.money > 0 or self.cangointodebt == True):
			self.health += 2.5
			self.money -= 0.5
			if self.weight <= 0:
				self.weight += 1
			if self.energy <= 0:
				self.energy += 1
		if dl_sign in self.touching and game.KEYTAPPED and game.BUTTON1:
			print("Don't ask")
			
	def collectables(self):
		for stone in (stone1, stone2, stone3):
			self.inventory['Stone']['Amount'] += self.coin(stone, self.inventory['Stone']['Amount'], 1, 10)
		self.money += self.coin(cash, self.money, 100)
		self.money += self.coin(cash2, self.money, 100)
		self.money += self.coin(quarter, self.money, 5)
		self.money += self.coin(credit_card, self.money, randint(1, 500))
		self.money += self.coin(gold, self.money, 1000)
		self.money += self.coin(silver, self.money, 500)
		self.money += self.coin(copper, self.money, 250)
	
	def coin(self, component, variable, value, timer=100, tp=True):
		if component.touchtimer > timer: #and (not component.shown):
			component.shown = True
		if component in self.touching:
			if tp:
				component.randPos()
			component.shown = False
			component.touchtimer = 0
			return value
		return 0
	
	def cycleWorlds(self, direction = 1):
		worlds = World.shownworlds
		if direction > 0:
			if worlds.index(player.world) < len(worlds)-1:
				self.world = worlds[worlds.index(player.world)+direction]
			else:
				self.world = worlds[0]
		elif direction < 0:
			if worlds.index(player.world) < len(worlds):
				self.world = worlds[worlds.index(player.world)+direction]
			else:
				self.world = worlds[len(worlds)-1]
		self.tp((0, 0))
				
	def tp(self, position, world=False, var=0, amount=0):
		if world == False: # if world isnt specified, default to position's world if its an object, and to the same world if position var is coordinate
			try:
				world = position.world
			except:
				world = self.world
		if self.cangointodebt or int(var) >= amount:
			try:
				self.x = -position.x
				self.y = position.y
			except:
				self.x = -position[0]
				self.y = position[1]
			self.world = world
			return var
		else:
			return 0
	
	def portals(self):
		if game.BUTTON1 and self.canteleport and self.touching:
			if house_door in self.touching:
				self.tp(house)
			if shop_door in self.touching:
				self.tp(shop)
			if cheese_hut in self.touching:
				self.tp((0, 0), cheese_land)
			if lava in self.touching:
				self.tp((0, 0), heck)
			if house in self.touching:
				self.tp(house_door)
			if shop in self.touching:
				self.tp(shop_door)
			if cave in self.touching:
				self.tp((0,0), cave_world)
			if cave_exit in self.touching:
				self.tp((cave.x+cave.width/2, cave.y), town)
			if apartment in self.touching:
				self.tp(apartment_door)
			if apartment_door in self.touching:
				self.tp(apartment)
			if club in self.touching:
				self.money -= self.tp(dl_sign, daddyland, self.money, 500)
			if dl_sign in self.touching:
				self.tp(club)
			if town_metro in self.touching:
				self.money -=self.tp(city_metro, city, self.money, 100)
			if city_metro in self.touching:
				self.money -=self.tp(town_metro, town, self.money, 100)
				
	
	def get_block_val(self, theblock, key):
		return Block.blocktypes[theblock][key]
	
	def placeBlock(self):
		if self.get_selected_val('Type') == 'Block' and self.get_selected_val('Amount') > 0 and game.BUTTON1:
			world = self.world
			theblock = self.selected
			width = self.world.tilesize
			height = self.world.tilesize
			solid = True
			elliptical = False
			color1 = self.get_block_val(theblock, 'Color1')
			color2= self.get_block_val(theblock, 'Color2')
			if game.keys[pygame.K_c]:
				elliptical = True
			placeable = True
			for item in Block.blocks:
				if item.x == self.tileX and item.y == self.tileY and item.deleted == False and item.world == self.world:
					placeable = False
			if placeable:
				try:
					newblock = Block(theblock, self.tileX, self.tileY, width, height, color1, world, solid, elliptical, color2)
				except:
					newblock = Block(theblock, self.tileX, self.tileY, width, height, (0, 0, 0), world, solid, elliptical, (255, 255, 255))
				if Block.is3D == True:
					Block.sortBlocks()
				self.depleteItem(theblock)
					
	def deleteBlock(self):
		if game.BUTTON2:
			for item in Block.blocks:
				if item.x > self.tileX-self.radius and item.x < self.tileX+self.radius\
				and item.y > self.tileY-self.radius and item.y < self.tileY+self.radius and self.world == item.world:
					if  not item.deleted:
						Block.blocks.remove(item)
						if not self.invincible:
							self.gainItem(item.name)
						item.deleted = True
					
	def clearBlocks(self):
		for item in Block.blocks:
			if not item.deleted:
				Block.blocks.clear()
				if not self.invincible:
					self.gainItem(item.name)
				item.deleted = True
	
	
player = Character('Player', -0, 0, 40, (255, 255, 0), True)




class Component(object):
	
	components = []
	showname = True
	maxhealth = 10000
	defaultslip = 0.2
	
	def __init__(self, name, x ,y, width, height, color, world, showname, elliptical=False, health=maxhealth, textsize=50, damage=0, playerspeed=1, slip=defaultslip, imagename='', movespeed=0, pos2=()):
		Component.components.append(self)
		self.name = name
		self.x = x - player.x
		self.y = y - player.y
		self.width = width
		self.height = height
		self.color = color
		self.world = world
		self.showname = showname
		self.elliptical = elliptical
		self.textsize = textsize
		self.leftwall = 0
		self.rightwall = 0
		self.upperwall = 0
		self.lowerwall = 0
		self.screenX = 0
		self.screenY = 0
		self.solid = False
		self.playertouch = False
		self.damage = damage
		self.health = health
		self.playerspeed = playerspeed
		self.slip = slip
		self.imagename = imagename
		self.shown = True
		self.autostate = False
		self.pos1 = (x, y)
		self.pos2 = pos2
		self.movespeed = movespeed
		if self.imagename:
			self.image = pygame.image.load(self.imagename)
			self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
		self.touchtimer = 0
		
	def draw(self):
		if self.world == player.world:
			self.screenX = player.x+(self.x-(self.width/2))+(game.screenwidth/2)
			self.screenY = player.y-(self.y+(self.height/2))+(game.screenheight/2)
			if self.shown:
				if self.imagename:
					game.screen.blit(self.image, (self.screenX, self.screenY, self.width, self.height))
				else:
					if self.elliptical:
						shape = pygame.draw.ellipse
					else:
						shape = pygame.draw.rect
					shape(game.screen, self.color, (self.screenX, self.screenY, self.width, self.height))
			textsize = self.textsize
			if self ==  cash or self == cash2:
				label = '   $'
				color = (175, 250, 175)
				overrideshow = True
			else:
				label = self.name
				color = (255, 255, 255)
				overrideshow = False
			if ((self.showname and Component.showname) or overrideshow) and self.shown:
				write(game.screen, 'font.ttf', textsize, self.screenX+self.width/2, self.screenY+self.height/2, label, color, True)
		
	def loop(self):
		self.collision()
		self.checkHealth()
		if self.pos2:
			self.autonomous()
		
	def checkHealth(self):
		if self.health <= 0:
			self.shown = False
	
	def randPos(self):
		#component.x = self.world.randX()
		#component.y = self.world.randY()
		self.x, self.y = self.world.randCoords()
		
	def collision(self):
		self.leftwall = self.screenX
		self.rightwall = self.screenX+(self.width)
		self.upperwall = self.screenY
		self.lowerwall = self.screenY+(self.height)
		if (player.righthitbox > self.leftwall and player.lefthitbox < self.rightwall\
		and player.tophitbox < self.lowerwall and player.bottomhitbox > self.upperwall)\
		and player.world ==  self.world and self.shown:
			player.touching.add(self)
			#print(player.touching)
			#player.collision()
			#for component in player.touching:
				#print(component.name)
			player.health -= self.damage
			self.health -= player.damage
		else:
			player.touching.discard(self)
			self.touchtimer += 1
			
	def autonomous(self): # programs component to move like a goomba
		if not self.pos2:
			speed = self.movespeed
			if self.autostate == False: # Used slope, which might not work
				self.x += (self.pos2[1]/self.pos2[0])*speed
				self.y += (self.pos2[1]/self.pos2[0])*speed
				if self.x >= self.pos2[0] and self.y >= self.pos2[1]:
					self.autostate = True
			else:
				self.x -= (self.pos1[1]/self.pos1[0])*speed
				self.y -= (self.pos1[1]/self.pos1[0])*speed
				if self.x <= self.pos1[0] and self.y <= self.pos1[1]:
					self.autostate = False
			

# Town components
# roads

'''
h_sidewalk = Component('Horizontal Sidewalk', 0, 0, town.width, 300, (185, 185, 185), town, False, False)
v_sidewalk = Component('Horizontal Sidewalk', 0, 0, 300, town.height, (185, 185, 185), town, False, False)
'''
h_road = Component('Horizontal Road', 0, 0, town.width*1.2, 200, (50, 50, 50), town, False, False)
v_road = Component('Vertical Road', 0, 0, 200, town.height*1.2, (50, 50, 50), town, False, False)

# features
#pond_beach = Component('Pond Beach', 1950, 1625, 1000, 950, (204, 188, 148), town, False, True)
#pond = Component('Pond', 1975, 1650, 600, 565, (20, 150, 185), town, False, True)
volcano = Component('Volcano', 2250, -2250, 1250, 1250, (165, 128, 138), town, False, True)
lava = Component('Lava', 2250, -2250, 250, 250, (240, 185, 30), town, False, True, Component.maxhealth, 0, 5)
cave = Component('Cave', -2500,  2600, 650, 300, (190, 190, 190), town, False, False)
#tree = Component('Tree', -1000, -1000, 180, 180, (50, 150, 60), town, False, True)

# buildings
house = Component('House', 900, 350, 300, 200, (100, 80, 50), town, True, False)
restaurant = Component('Restaurant', -450, 350, 400, 200, (160, 160, 160), town, True, False)
gym = Component('Gym', -900, 450, 300, 400, (135, 130, 140), town, True, False)
school = Component('School', 450, -400, 200, 300, (200, 175, 150), town, True, False)
office = Component('Office',  -500, -400, 300, 300, (160, 180, 180), town, True, False)
hospital = Component('Hospital', -400, 700, 300, 300, (210, 210, 210), town, True, False)
shop = Component('Shop', -950, -400, 400, 300, (250, 100, 100),  town, True, False)
town_metro = Component('Metro - $100', 400, 2000, 300, 400, (100,100, 100), town, True, False)

# items
cash = Component('Cash', town.randX(), town.randY(), 50, 23, (100, 150, 100), town, True, False, Component.maxhealth, 33)
cash2 = Component('Cash 2', town.randX(), town.randY(), 50, 23, (100, 150, 100), town, True, False, Component.maxhealth, 33)

# House components
bed = Component('Bed', 200, 200, 80, 120, (255, 0, 0), house_interior, False, False)
house_door = Component('House Door', -house_interior.width/2, 0, 20, 120, (190, 170, 80), house_interior, False, False)
# house items
quarter = Component('Quarter', house_interior.randX(), house_interior.randY(), 20, 20, (185, 185, 185), house_interior, False, True)

# Shop components
shop_door = Component('Shop Door', 0, shop_interior.height/2, 120, 20, (110, 78, 48), shop_interior, False, False)

# shop items

# City components
# streets
h_street = Component('Horizontal Street', 0, 0, city.width*2, 300, (50, 50, 50), city, False, False)
v_street = Component('Vertical Street', 0, 0, 300, city.height*2, (50, 50, 50), city, False, False)

# city features
ocean_beach = Component('Ocean Beach', -4200, 0, 2910, 3500, (204, 188, 148), city, False, True)
ocean = Component('Ocean', -4200, 0, 2000, 2500, (10, 140, 165), city, False, True)

# city buildings
bank = Component('Bank', 400, 425, 300, 350, (25, 150, 75), city, True, False)
apartment = Component('Apartment', -400, -400,  300, 300, (200, 140, 50), city, True, False)
university = Component('University', -450, 450, 400, 400, (220, 190, 120), city, True, False)
city_metro = Component('Metro - $100', 400, 2000, 300, 400, (100,100, 100), city, True, False)
club = Component('Club - $500', 2000, -425, 300, 350, (255, 50, 170), city, True, False)

# city items
credit_card = Component('Credit Card', city.randX(), city.randY(), 55, 32, (220, 200, 150), city, True, False, Component.maxhealth, 15)

#Apartment components
apartment_door = Component('Apartment Door', apartment_interior.width/2, (-apartment_interior.height/2)+100, 20, 120, (110, 78, 48), apartment_interior, False, False)

# Farm components
barn = Component('Barn', 0, 500, 350, 350, (220, 75, 25),  farm, True, False)
field1 = Component('Field 1', 750, 500, 700, 700, (70, 60, 0),  farm, True, False)
field2 = Component('Field 2', -750, 500, 700, 700, (70, 60, 0),  farm, True, False)
cheese_hut = Component('Cheese Hut', -1500, -1500,  300, 300, (250, 230, 50), farm, False, True)

# Snowland components
ice1 = Component('Ice 1', -1500, -1500, 1500, 1500, (100, 200, 230), snowland, False, False, Component.maxhealth, 0, 0, 1, 0.97)

# Cave components
cave_exit = Component('Cave Exit', cave_world.width/2, 0, 30, cave_world.height, (0, 0, 0), cave_world, False, True)
stone1 = Component('Stone 1', cave_world.randX(), cave_world.randY(), 70, 70, (140, 141, 143), cave_world, False, False)
stone2 = Component('Stone 2', cave_world.randX(), cave_world.randY(), 70, 70, (150, 151, 153), cave_world, False, False)
stone3 = Component('Stone 3', cave_world.randX(), cave_world.randY(), 70, 70, (145, 146, 148), cave_world, False, False)
gold = Component('Gold', cave_world.randX(), cave_world.randY(), 34, 32, (190, 170, 50), cave_world, False, True)
silver = Component('Silver', cave_world.randX(), cave_world.randY(), 35, 37, (170, 170, 170), cave_world, False, True)
copper = Component('Copper', cave_world.randX(), cave_world.randY(), 38, 40, (160, 120, 50), cave_world, False, True)

dl_sign = Component('Daddyland Sign', 0, daddyland.height/2-500, 300, 200, (255, 255, 255), daddyland, False, False, Component.maxhealth, 0, 0, 0, 0, 'daddyland.jpeg', 100, (100, 100))




class Block(object):
	count = 0
	blocks = []
	is3D = True
	blocktypes={}
	
	@classmethod
	def retrieveBlocktypes(cls):
		Block.blocktypes = {
			'Stone': {
				'ID': 0,
				'Color1': (150, 150,150),
				'Color2' : (100, 100, 100),
			},
			'Ground': {
				'ID': 1,
				'Color1': player.world.color,
				'Color2': player.world.exteriorcolor,
			},
			'Dirt': {
				'ID': 2,
				'Color1': player.world.exteriorcolor,
				'Color2' : player.world.color,
			},
			'Rainbow': {
				'ID': 3,
				'Color1': cls.get_rainbow(),
				'Color2': cls.get_rainbow(),
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
			},
		}
		
	rmin = 100
	rmax = 255
	#width = 100#world.width/200
	#height = 100#world.height/200
	thickness = 2
	sickomode = False
	
	@classmethod
	def sortBlocks(cls):
		if Block.is3D:
			Block.blocks.sort(key = lambda theblock: -theblock.y) # orders 3d block by y so they dont overlap
	
	@classmethod
	def get_rainbow(cls):
		return (randint(Block.rmin, Block.rmax), randint(Block.rmin, Block.rmax), randint(Block.rmin, Block.rmax))
		
	
	def __init__(self, name, x, y, width, height, color1, world, solid, elliptical, color2):
		self.name = name
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.color1 = color1
		self.color2 = color2
		self.world = player.world
		self.solid = solid
		self.elliptical = elliptical
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
		self.slip = 0
		self.playerspeed = 0
	
	def draw(self):
		if self.bordered:
			thickness = Block.thickness
		else:
			thickness = 0
		self.tallness = int(player.world.tilesize*0.5)
		if self.world == player.world and self.deleted == False:
			self.screenX = player.x+(-self.x-(self.width/2))+(game.screenwidth/2)
			self.screenY = player.y-(self.y+(self.height/2))+(game.screenheight/2)
			if self.elliptical:
				shape = pygame.draw.ellipse
			else:
				shape = pygame.draw.rect
			if Block.sickomode and self.name == 'Rainbow':
				self.color1 = Block.get_rainbow()
				self.color2 = Block.get_rainbow()
			if Block.is3D:
				shape(game.screen, self.color2, (self.screenX, self.screenY-self.tallness, self.width, self.height+self.tallness)) # block side
				shape(game.screen, self.color1, (self.screenX+(thickness/2), self.screenY+(thickness/2)-self.tallness, self.width-thickness, self.height-thickness)) #block top
			else:
				shape(game.screen, self.color2, (self.screenX, self.screenY, self.width, self.height)) # block border
				shape(game.screen, self.color1, (self.screenX+(thickness/2), self.screenY+(thickness/2), self.width-thickness, self.height-thickness)) # block
	
	def loop(self):
		Block.retrieveBlocktypes()
		self.collision()
	
	def collision(self):
		self.leftwall = self.screenX
		self.rightwall = self.screenX+(self.width)
		self.upperwall = self.screenY
		self.lowerwall = self.screenY+(self.height)
		if (player.righthitbox > self.leftwall and player.lefthitbox < self.rightwall\
		and player.tophitbox < self.lowerwall and player.bottomhitbox > self.upperwall)\
		and player.world ==  self.world:
			player.touching.add(self)
		else:
			player.touching.discard(self)
	
	
class Stat(object):
	startposition = 3
	textsize = 28
	shown = True
	detailed = False
	stats = []
	
	@classmethod
	def retrieveStats(cls):
		Stat.stats.clear()
		worldstat = Stat('World', player.world.name)
		xstat = Stat('X', -player.x)
		ystat = Stat('Y', player.y)
		itemstat = Stat('Item selected', str(player.get_selected_val('Amount'))+' * '+player.selected) #+' Type: '+str(player.get_selected_val('Type')))
		healthstat = Stat('Health', player.health)
		agestat = Stat('Age', player.age)
		energystat = Stat('Energy', player.energy)
		weightstat = Stat('Weight', player.weight)
		strengthstat = Stat('Strength', player.strength)
		happinessstat = Stat('Happiness', player.happiness)
		intelstat = Stat('Intelligence', player.intelligence)
		moneystat = Stat('Cash', player.money)
		speedstat = Stat('Speed', player.speed, True)
		touchingstat=Stat('Touching', cls.get_names(player.touching), True)
		timestat = Stat('Time elapsed', game.seconds)
		framestat = Stat('Frames', game.frames, True)
		fpsstat = Stat('FPS', game.clock.get_fps(), True)
		
	@staticmethod
	def get_names(var):
		strings = list(map(lambda x: x.name, var))
		string = ', '.join(strings)
		if not var:
			return 'None'
		return string
	
	@classmethod
	def drawStats(cls):
		for stat in Stat.stats:
			if stat.do:
				stat.draw(len(Stat.stats)-Stat.stats.index(stat))
	
	
	def __init__(self, name, stat, detailed=False):
		self.detailed = detailed
		self.do = (not self.detailed) or (self.detailed and Stat.detailed)
		if self.do:
			Stat.stats.append(self)
		self.name = name
		self.stat = stat
		self.spacing = 18
		self.x = 5
		self.y = 0
	
	def draw(self, position):
		stat = self.stat
		self.y = game.screenheight-(position*self.spacing) - self.startposition
		if type(stat) == float or type(stat) == int:
			stat = int(round(stat))
		label = self.name + ':  ' + str(stat)
		if (self.name == 'Time elapsed'):
			minutesFormatting = str(game.minutes)
			secondsFormatting = str(game.seconds)
			if (game.minutes <= 9):
				minutesFormatting = '0' + str(game.minutes)
			if (game.seconds <= 9):
				secondsFormatting = '0' + str(game.seconds)
			label = (self.name + ': ' + minutesFormatting + ':' + secondsFormatting)
		if Stat.shown:
			write(game.screen, 'font.ttf', Stat.textsize, self.x, self.y, label, (255, 255, 255))


def debug(do=False):
	if (do):
		#for thing in player.touching:
			#print(thing.name)
		print(player.damage)
			

game.loopitems = [Component.components, Block.blocks, Character.characters]

while game.running:
	game.play()
print('Game over')
pygame.quit()
