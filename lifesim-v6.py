#!/usr/bin/python
import pygame
import math
import random
import sys
from proceduralgen import generation
generator = generation()



def debug(do=True):
	if do:
		#for i in game.components:
		#	if i.world == player.world:
		#		print(str(i.rect) + ' ')
		pass
		#for p in game.projectiles:
		#	print(p.rect)
	

def roundto(x, base):
	return base*round(float(x)/base)
	

def restrict(value, minvalue, maxvalue):
    return max(minvalue, min(value, maxvalue))


def loadImage(imagename):
	image = pygame.image.load('Images/' + imagename + '.png').convert_alpha()
	return image


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




class Game:
	
	def __init__(self):
		pygame.init()
		pygame.key.set_repeat()
		self.defaultwidth = 1400
		self.defaultheight = 950
		self.screen = pygame.display.set_mode((self.defaultwidth, self.defaultheight), pygame.RESIZABLE)
		pygame.display.set_caption('Life Simulator')
		self.fullscreen = False
		
		self.running = True
		self.events = None
		pygame.event.set_allowed([pygame.QUIT, pygame.VIDEORESIZE, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP])
		self.keys = None
		self.MOUSECLICKED = False
		self.MOUSEPRESSED = False
		self.MOUSEMOVED = False
		self.KEYTAPPED = False
		self.KEYPRESSED = False
		self.LEFT = 0
		self.RIGHT = 2
		self.MIDDLE = 1
				
		self.seconds = 0
		self.minutes = 0
		self.clock = pygame.time.Clock()
		self.frames = 0
		self.hacking = False
		self.command = ''
		self.docheats = True
		self.message = ''
		
		#self.cursor = loadImage('cursor.png')
		self.target = loadImage('target')
		
		self.worlds = []
		self.characters = []
		self.projectiles = []
		self.components = []
		self.blocks = []
		
		self.loopitems = []
		self.doproceduralgen = True
		self.worldgennum = 8
		self.componentgennum = 8
		
	
	def play(self):
		self.loop()
		self.draw()
		
	
	def draw(self):
		player.world.draw()
		for group in self.loopitems:
			for item in group:
				if item.world == player.world and item.onscreen and item.shown:
					item.draw()
		for stat in Stat.stats:
			if stat.do:
				stat.draw(len(Stat.stats)-Stat.stats.index(stat))
				
		if self.message:
			self.displayMessage(self.message, int(self.get_screenwidth()*0.15))
			self.message = ''

		self.clock.tick()
		pygame.display.flip()	
		
	
	def loop(self):
		#player.world.loop()
		self.checkEvents()
		Stat.retrieveStats()
		self.keepTime()
		for group in reversed(self.loopitems):
			for item in group:
				item.loop()
		self.resetInput()
		player.resetAttackStats()
		
	
	def checkEvents(self):
		self.events = pygame.event.get()
		self.keys = pygame.key.get_pressed()
		self.mouse = pygame.mouse.get_pressed()
		self.mouseX = pygame.mouse.get_pos()[0]
		self.mouseY = pygame.mouse.get_pos()[1]
		self.checkKeys()
		for event in self.events:
			if event.type == pygame.QUIT:
				self.running = False
			elif event.type == pygame.VIDEORESIZE:
				self.screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				#print(pygame.mouse.get_pos())
				self.MOUSECLICKED = True
				self.MOUSEPRESSED = True
			elif event.type == pygame.MOUSEBUTTONUP:
				self.MOUSEPRESSED = False
			if event.type == pygame.MOUSEMOTION:
				self.MOUSEMOVED = True
			elif event.type == pygame.KEYDOWN:
				self.KEYTAPPED = True
				self.KEYPRESSED = True
				self.hack(event)
				self.cheats()
				self.options()
			elif event.type == pygame.KEYUP:
				self.KEYPRESSED = False
		
	
	def resetInput(self):
		self.MOUSECLICKED = False
		self.MOUSEMOVED = False
		self.KEYTAPPED = False
		
	
	def checkKeys(self) :
		if self.keys[pygame.K_e] or self.keys[pygame.K_RETURN] or self.mouse[self.LEFT]:
			self.BUTTON1 = True
		else:
			self.BUTTON1 = False
			
		if self.keys[pygame.K_g] or self.keys[pygame.K_BACKSPACE] or self.mouse[self.RIGHT]:
			self.BUTTON2 = True
			player.attackcooldown = 0
		else:
			self.BUTTON2 = False
			player.attackcooldown += 1
			
		if self.keys[pygame.K_LSHIFT] or self.keys[pygame.K_RSHIFT]:
			self.SHIFT = True
		else:
			self.SHIFT = False
		if self.keys[pygame.K_LCTRL] or self.keys[pygame.K_RCTRL]:
			self.CONTROL = True
		else:
			self.CONTROL = False	
		
	
	def displayMessage(self, message, size=200):
		write(game.screen, 'font.ttf', size, int(self.get_screenwidth()/2), int(self.get_screenheight()/2), message, (255, 255, 255), True)
		
	
	def screensize(self):
		return pygame.display.get_surface().get_size()
		
	
	def get_screenwidth(self):
		return self.screensize()[0]
		
	
	def get_screenheight(self):
		return self.screensize()[1]
		
	
	def keepTime(self):
		self.seconds = int(pygame.time.get_ticks()/1000)%60
		self.minutes = int((pygame.time.get_ticks()/1000)/60)%60
		self.clock.tick()
		self.frames += 1
		
	
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
				Stat.shown = not Stat.shown
			if self.keys[pygame.K_3]:
				Block.viewangle += 25
				if Block.viewangle > int(player.world.tilesize):
					Block.viewangle = 0
				Block.sortBlocks()
			if self.keys[pygame.K_4]:
				Component.showname = not Component.showname
			if self.keys[pygame.K_5]:
				player.elliptical = not player.elliptical
		if self.SHIFT or self.keys[pygame.K_KP0]:
			player.sprinting = not player.sprinting
		
	
	def cheats(self):
		if self.docheats:
			if self.CONTROL:
				if self.keys[pygame.K_b]:
					player.cycleWorlds(-1)
				if self.keys[pygame.K_n]:
					player.cycleWorlds()
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
				if self.keys[pygame.K_j]:
					self.command = ''
					self.hacking = True
				if self.keys[pygame.K_u]:
					if player.coolness != 69420:
						player.coolness = 69420
					else:
						player.coolness = 0
		
	
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
		else:
			self.command = ''
		
	

game = Game()



class World:
	
	def __init__(self, name, width, height, color, exteriorcolor=None, walled=False, borderdamage=0, borderspeed=1, slip=0.5):
		game.worlds.append(self)
		self.name = name
		self.width = width
		self.height = height
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.innerrect = pygame.Rect(0, 0, self.width, self.height)
		self.color = color
		self.exteriorcolor = exteriorcolor
		self.walled = walled
		self.tilesize = 100
		self.borderdamage = borderdamage
		self.borderspeed = borderspeed
		self.slip = slip
		
	
	def loop(self):
		swidth = game.get_screenwidth()
		sheight = game.get_screenheight()
		self.screenX = player.x - (self.width/2) + (swidth/2)
		self.screenY = player.y - (self.height/2) + (sheight/2)
		self.rect = pygame.Rect(self.screenX, self.screenY, self.width, self.height)
		self.innerrect = pygame.Rect(self.screenX+(swidth/2), self.screenY+(sheight/2), self.width-(swidth/2), self.height-(sheight/2))
		
	
	def draw(self):
		width = self.width
		height = self.height
		swidth = game.get_screenwidth()
		sheight = game.get_screenheight()
		self.screenX = player.x - (self.width/2) + (swidth/2)
		self.screenY = player.y - (self.height/2) + (sheight/2)
		self.rect = pygame.Rect(self.screenX, self.screenY, self.width, self.height)
		self.innerrect = pygame.Rect(self.screenX+(swidth/2), self.screenY+(sheight/2), self.width-(swidth), self.height-(sheight))
		
		
		if self.exteriorcolor and not player.rect.colliderect(self.innerrect):
			game.screen.fill(self.exteriorcolor)
			pygame.draw.rect(game.screen, self.color, self.rect)
		else:
			game.screen.fill(self.color)
		
	
	def randCoords(self):
		return (self.randX(), self.randY())
		
	
	def randX(self):
		return(random.randint(int(-self.width/2), int(self.width/2)))
		
	
	def randY(self):
		return(random.randint(int(-self.height/2), int(self.height/2)))
		
	

town = World('Town', 7500, 7500, (86, 190, 93), (220, 200, 140))
house_interior = World('House Interior', 1050, 850, (230, 210, 140), (100, 80, 50), walled=True)
shop_interior = World('Shop Interior', 1200, 750, (225, 225, 225), (250, 100, 100), walled=True)
school_interior = World('School Interior', 1200, 750, (200, 200, 200), (200, 110, 75), walled=True)
city = World('City', 5000, 5000, (170, 170, 170), (110, 220, 130))
apartment_interior = World('Apartment Interior', 1125, 1575, (220, 200, 140), (200, 140, 50), walled=True)
farm = World("Farm", 5000, 5000, (80, 220, 120), (200, 190, 70), borderspeed=0.5)
snowland = World('Snowland', 6000, 6000, (180, 220, 230), (100, 75, 40))
heck = World('Heck', 4500, 4500, (100, 35, 30), (255, 150, 0), borderdamage=6, borderspeed=0.5) # No swearing on my christian minecraft server
cheese_land = World('Cheese Land', 3500, 3500, (255, 210, 75), (255, 175, 100))
cave_world = World('Cave World', 3000, 1000, (90, 90, 90), (25, 25, 25), walled=True)
daddyland = World('Daddyland', 6900, 4200, (255, 195, 240), (255, 50, 170), borderspeed=0.1, walled=True)
lab_interior = World('Lab Interior', 1500, 1500, (120, 120, 120), walled=True)
desktop = World('Desktop', 1500, 1500, (0, 0, 0), (100, 100, 100), walled=True)



class Character:
	
	def __init__(self, name):
		game.characters.append(self)
		self.name = name
		self.world = town
		self.x = 0
		self.y = 0
		
		self.width = 85
		self.height = 85
		self.elliptical = True
		
		self.screenX = -(self.width/2)+(game.get_screenwidth()/2)
		self.screenY = -(self.height/2)+(game.get_screenheight()/2)
		self.rect = pygame.Rect(self.screenX, self.screenY, self.width, self.height)
		
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
			self.images[image] = pygame.image.load('Images/' + image + '.png').convert_alpha()
			
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
				
		self.basespeed = 3
		self.speed = self.basespeed
		self.sprinting = False
		self.xmomentum = 0
		self.ymomentum = 0
		self.angle = 270
		
		self.invincible = False
		self.superstrength = False
		self.invisible = False
		self.indoors = False
		self.overborder = False
		self.cangointodebt = False
		self.canteleport = True
		
		self.shown = True
		self.onscreen = True
		self.touching = set([])
		self.onground = True
		self.tileX = 0
		self.tileY = 0
		self.uponblock = False
		
		self.damage = 0
		self.lastdamage = 0
		self.damagecooldown = 0
		self.attackcooldown = 10
		self.damagetaken = 0
		self.lastdamagetaken = 0
		self.lasthealth = self.health
		
		self.slot = 1
		self.selected= 'Hand'
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
				'Slot': 8,
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
			'Bow': {
				'Slot': 5,
				'Type': 'Weapon',
				'Amount': 100,
				'Depletable': True,
				'Damage': 50,
				'Range': 10,
			},
		}
		
	
	def loop(self):
		self.screenX = -(self.width/2)+(game.get_screenwidth()/2)
		self.screenY = -(self.height/2)+(game.get_screenheight()/2)
		self.rect = pygame.Rect(self.screenX, self.screenY, self.width, self.height)
		
		# Used to position the block you place
		self.tileX = roundto(self.x + (-game.mouseX ) + (game.get_screenwidth()/2), self.world.tilesize)
		self.tileY = roundto(self.y - (game.mouseY ) + (game.get_screenheight()/2), self.world.tilesize)
		
		self.face()
		self.control()
		self.manageStats()
		self.manageImage()
		self.manageSpeed()
		self.collectables()
		self.checkBorder()
		self.checkSolid()
		if game.MOUSEPRESSED or game.KEYPRESSED:
			self.deleteBlock()
			if self.get_selected_val('Type') == 'Block':
				self.placeBlock()
			else:
				self.useItems()
		if self.touching:
			self.collision()
		if game.MOUSECLICKED or game.KEYTAPPED:
			self.portals()
			self.selectSlot()
		
	
	def draw(self):
		if self.onscreen:
			if self.elliptical:
				shape = pygame.draw.ellipse
			else:
				shape = pygame.draw.rect
			
			x = self.screenX
			y = self.screenY
			shape(game.screen, self.color, self.rect)
			
			if self.image:
				game.screen.blit(pygame.transform.scale(self.image, (int(self.width), int(self.height))), self.rect)
		self.drawItems()
		self.drawEffects()
		
	
	def control(self):
		self.up, self.down, self.right, self.left = False, False, False, False
		if game.keys[pygame.K_w]:
			self.y += self.speed
			self.ymomentum = -self.speed
			self.up = True
		if game.keys[pygame.K_s]:
			self.ymomentum = self.speed
			self.y -= self.speed
			self.down = True
		if game.keys[pygame.K_d]:
			self.xmomentum = self.speed
			self.x -= self.speed
			self.right = True
		if game.keys[pygame.K_a]:
			self.xmomentum = -self.speed
			self.x+= self.speed
			self.left = True
			
		slip = 0
		if self.touching:
			for thing in self.touching:
				#if component.slip > slip: # tries to find max slipperyness regardless of which thing is on top
				slip = thing.slip # actually tries to find slipperyness of the one the character is directly on top of (on the highest layer)
		else:
			slip = self.world.slip
			
		if not (self.left or self.right):	
			self.x -= self.xmomentum
			self.xmomentum *= slip
		if not (self.up or self.down):
			self.ymomentum *= slip
			self.y -= self.ymomentum
		
	
	def face(self):			
		if game.MOUSEMOVED:
			# https://gamedev.stackexchange.com/questions/132163/how-can-i-make-the-player-look-to-the-mouse-direction-pygame-2d
			relativeX, relativeY = game.mouseX - self.screenX-(self.width/2), game.mouseY - self.screenY-(self.height/2)
			self.angle = math.degrees(math.atan2(relativeY, relativeX))+90
		if game.keys[pygame.K_UP]:
			self.angle = 0
		elif game.keys[pygame.K_DOWN]:
			self.angle = 180
		elif game.keys[pygame.K_RIGHT]:
			self.angle = 90
		elif game.keys[pygame.K_LEFT]:
			self.angle = 270
		
	
	def manageSpeed(self):
		speedmultiplier = 1
		if self.overborder and self.onground:
			speedmultiplier *= self.world.borderspeed
		for thing in self.touching:
			speedmultiplier *= thing.playerspeed
		speedmultiplier *= 1 #(((self.world.width+self.world.height)/2)/10000)+1
		self.walkingspeed = ((self.energy*0.010)+self.basespeed)*speedmultiplier
		if self.sprinting:
			self.speed = self.walkingspeed*2 # normal sprinting
			self.energy -= 0.10
		else:
			self.speed = self.walkingspeed # walking normally
			self.energy -= 0.05
		
	
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
			self.age += 0.01
			#self.height *= 1.0002
			#self.height *= 1.0002
			self.cangointodebt = False
		self.onground = not self.touching
		self.health = max(0, self.health)
		self.energy = max(0, self.energy)
		self.weight = max(0, self.weight)
		
	
	def collision(self):
		canpay = self.money > 0 or self.cangointodebt
		if restaurant in self.touching and canpay:
			self.weight += 0.5
			self.happiness += 1
			self.money -= 0.5
			self.energy += 0.5
			self.width += 0.1
			self.height += 0.1
		if gym in self.touching and canpay:
			self.weight -= 0.5
			self.money -= 0.5
			self.happiness -= 0.25
			self.energy -= 0.5
			self.strength += 0.5
			self.width -= 0.075
			self.height -= 0.075
		if school in self.touching:
			self.intelligence += 0.75
			self.happiness -= 0.25
		if university in self.touching and (self.age > 18):
			self.money -= 0.75
			self.intelligence += 1.25
			self.happiness -= 0.5
		if office in self.touching:
			self.money += (0.5 * (self.intelligence/12)) + 0.5
			self.happiness -= 0.5
			self.energy -= 0.5
		if bank in self.touching:
			self.money += (0.25 * (self.money/24)) + 0.5
			self.happiness -= 20/self.money
			self.energy -= 0.5
		if bed in self.touching:
			self.happiness += 1
			self.energy += 1
		if hospital in self.touching and canpay:
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
		self.money += self.coin(cash, self.money, 100, val2=20)
		self.money += self.coin(cash2, self.money, 100, val2=20)
		self.money += self.coin(quarter, self.money, 5, val2=1)
		self.money += self.coin(gold, self.money, 1000, val2=200)
		self.money += self.coin(silver, self.money, 500, val2=100)
		self.money += self.coin(copper, self.money, 250, val2=50)
		
		cardval = random.randint(1, 500)
		self.money += self.coin(credit_card, self.money, cardval, val2=cardval/5)
		
	
	def coin(self, component, variable, value, timer=100, tp=True, var2='self.happiness', val2=0):
		if component.touchtimer > timer: #and (not component.shown):
			component.shown = True
		if component in self.touching:
			if tp:
				component.randPos()
			if var2:
				exec(var2 + ' += val2')
			component.shown = False
			component.touchtimer = 0
			return value
		return 0
		
	
	def cycleWorlds(self, direction=1):
		worlds = game.worlds
		try:
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
		except:
			pass
	
	
	def tp(self, position, world=None, var=0, statement=True):
		if world == None:
			try:
				world = position.world
			except:
				world = self.world
		if self.cangointodebt or statement == True:
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
		for item in self.touching:
			if item in game.components:
				if item.tp and game.BUTTON1 and self.canteleport:
					self.tp(item.tp)
		
	
	def checkBorder(self):
		if not self.rect.colliderect(self.world.rect):
			self.overborder = True
			if self.onground:
				self.health -= self.world.borderdamage
		else:
			self.overborder = False
		if self.world.walled:
			self.x = restrict(self.x, -(self.world.width/2) + (self.width/2), (player.world.width/2) - (player.width/2))
			self.y = restrict(self.y, -(player.world.height/2) +(player.height/2), (player.world.height/2) - (player.height/2))
		
	
	def checkSolid(self):
		width = self.width
		height = self.height
		placedblocks = list(map(lambda x: x in self.touching, game.blocks))
		if True not in placedblocks:
			player.uponblock = False
		items = game.components.copy()
		if game.blocks:
			items.extend(game.blocks)
		for item in items:
			if self.rect.colliderect(item.rect) and (not self.uponblock and not item.deleted) and item.onscreen and item.solid:
				if self.screenY > item.screenY - (item.height/2) and self.screenY < item.screenY + (item.height/2):
					if self.screenX < item.screenX: # Left
						self.x = max(item.x + width, self.x)
					if self.screenX > item.screenX: # Right
						self.x = min(item.x - width, self.x)
				if self.screenX > item.screenX - (item.width/2) and self.screenX < item.screenX + (item.width/2):
					if self.screenY > item.screenY: # Bottom
						self.y = min(item.y - height, self.y)
					if self.screenY < item.screenY: # Top
						self.y = max(item.y+ height, self.y)
		
	
	def useItems(self):
		if self.get_selected_val('Amount') > 0 or self.invincible:
			if self.selected == 'Hand':
				self.canteleport = True
			else:
				self.canteleport = False
			if game.MOUSECLICKED or game.KEYTAPPED:
				if game.BUTTON1:
					if self.get_selected_val('Type') == 'Consumable':
						exec(self.get_selected_val("Stat") + ' += self.get_selected_val("Value")')
				if game.BUTTON2:
					if self.get_selected_val('Type') == 'Weapon':
						self.damage = self.getDamage()
					if 'Range' in self.inventory[self.selected].keys():
							if self.get_selected_val('Range') > 0:
								if self.selected == 'Bow':
									self.damage = self.getDamage()
									newprojectile = Projectile(self.x, self.y, self.angle, 85, 30, 15, 15, (125, 100, 50), pygame.draw.ellipse, damage=self.getDamage())
					self.checkDeplete()
		else:
			self.canteleport = True
		
	
	def drawItems(self):
		if self.get_selected_val('Type') == 'Block' or 'Image' in self.inventory[self.selected].keys():
			width = self.world.tilesize
			height = self.world.tilesize
			x = player.x + (-self.tileX - width/2) + (game.get_screenwidth()/2)
			y = player.y - (self.tileY + height/2) + (game.get_screenheight()/2)
			theblock = self.selected
			color1 = Block.types[theblock]['Color1']
			color2 = Block.types[theblock]['Color2']
			width = 20
			height = 20
			xOffset = -(self.width - 10)
			yOffset = 60
			if self.get_selected_val('Type') == 'Block':
				pygame.draw.rect(game.screen, color2, (self.screenX-(width/2)-xOffset-1, self.screenY-(height/2)+yOffset-1, width+2, height+2))
				pygame.draw.rect(game.screen, color1, (self.screenX-(width/2)-xOffset, self.screenY-(height/2)+yOffset, width, height))
			else:
				image = self.get_selected_val('Image')
				imagerect = (self.screenX - width/2 - xOffset, self.screenY - height/2 + yOffset, width, height)
				game.screen.blit(image, imagerect)
		
	
	def drawEffects(self):
		if self.get_selected_val('Type') == 'Weapon':
			if self.checkRanged(self.selected):
				size = 45
				image = pygame.transform.scale(game.target, (size, size))
				game.screen.blit(image, (game.mouseX-(size/2), game.mouseY-(size/2), size, size))
				pygame.mouse.set_visible(0)
			else:
				pygame.mouse.set_visible(1)
				if player.attackcooldown < 4:
					player.showAttack()
					
		self.showDamage()

		if self.get_selected_val('Type') == 'Block':
			width = self.world.tilesize
			height = self.world.tilesize
			x = self.x + roundto((-self.tileX - (width/2)), self.world.tilesize/2) + (game.get_screenwidth()/2)
			y = self.y - roundto((self.tileY + (height/2)), self.world.tilesize/2) + (game.get_screenheight()/2)
			pygame.draw.rect(game.screen, (0, 0, 0), (x, y, width, height), 1)
			self.blockX = self.tileX# + roundto(game.get_screenwidth()/2, self.world.tilesize)
			self.blockY = self.tileY# + roundto(game.get_screenheight()/2, self.world.tilesize)
		
	
	def checkDeplete(self):
		if self.get_selected_val('Depletable') == True:
			self.depleteItem(self.selected)
		
	
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
		
	
	def getDamage(self):
		basedamage = self.get_selected_val('Damage')
		damage = basedamage + int(self.strength-0.5)
		self.damage = damage
		return damage
		
	
	def showDamage(self):
		if self.damagecooldown < 3 and self.lastdamagetaken > 0 and not self.invincible:
			self.displayText(self.lastdamagetaken, int((self.lastdamagetaken/2)+40), (255, 0, 0))
		self.damagecooldown += 1
		
	
	def showAttack(self):
		self.displayText(player.lastdamage, int((player.lastdamage/2)+40))
		
	
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
		
	
	def checkRanged(self, item):
		if 'Range' in self.inventory[item].keys():
			if self.inventory[item]['Range'] > 0:
				return True
		return False
		
	
	def displayText(self, text, size=40, color=(255, 255, 255)):
		write(game.screen, 'font.ttf', size, game.get_screenwidth()/2, game.get_screenheight()/2-self.height-size/2, str(text), color, True)
		
	
	def manageImage(self):
		if self.happiness >= 300:
			image = 'coolio'
		elif self.happiness >= 200:
			image = 'happy'
		elif self.happiness > 100:
			image = 'meep'
		elif self.happiness <= -300:
			image = 'cry'
		elif self.happiness <= -200:
			image = 'scared' 
		elif self.happiness <= -100:
			image = 'pissed'
		else:
			image = 'meh'
		if self.coolness == 69420:
			image = 'supercoolio'
		if not self.living:
			image = 'dead'
		self.image = self.images[image]
		
	
	def checkPlaceable(self):
		placeable = True
		for item in game.blocks:
			if item.x == self.blockX and item.y == self.blockY and item.world == self.world and not item.deleted:
				placeable = False # Prevents the block from overwriting another block.
		return placeable
		
	
	def placeBlock(self):
		pygame.mouse.set_visible(1)
		self.canteleport = False
		if game.BUTTON1:
			if self.get_selected_val('Type') == 'Block' and (self.get_selected_val('Amount') > 0 or self.invincible) and self.world.tilesize > 0:
				if self.checkPlaceable():
					theblock = self.selected
					width = self.world.tilesize
					height = self.world.tilesize
					newblock = Block(theblock, self.blockX, self.blockY, width, height, self.world, True)
					if Block.viewangle > 0:
						Block.sortBlocks()
					self.depleteItem(theblock)
					self.uponblock = True
		
	
	def deleteBlock(self):
		if game.BUTTON2:
			for block in game.blocks:
				if block.rect.collidepoint(game.mouseX, game.mouseY):
					if not block.deleted:
						game.blocks.remove(block)
						if not self.invincible:
							self.gainItem(block.name)
							block.deleted = True
							del block
		
	
	def clearBlocks(self):
		for block in game.blocks:
			if not block.deleted:
				game.blocks.clear()
				if not self.invincible:
					self.gainblock(block.name)
				block.deleted = True
				del block
	

player = Character('Player')



class Projectile(object):
	
	def __init__(self, x, y, angle, speed, ranges, width=10, height=10, color=(0, 0, 0), shape=pygame.draw.ellipse, passthrough=False, damage=player.getDamage(), image=''):
		game.projectiles.append(self)
		self.world = player.world
		self.x = -x
		self.y = y
		self.startx = self.x
		self.starty = self.y

		self.angle = angle
		self.speed = speed
		self.ranges = ranges
		self.distance = 0
		if type(ranges) != int and type(ranges) != float:
			self.truerange = random.randint(int(ranges))
		else:
			self.truerange = ranges*100
		self.width = width
		self.height = height
		self.screenX = player.x + (self.x - (self.width/2)) + (game.get_screenwidth()/2)
		self.screenY = player.y - (self.y + (self.height/2)) + (game.get_screenheight()/2)
		self.color = color
		self.shape = shape
		self.passthrough = passthrough
		self.damage = damage
		self.image = image
		if self.image:
			self.image = pygame.image.load(image + '.png').convert_alpha()
		self.rect = pygame.Rect(int(self.screenX), int(self.screenY), self.width, self.height)
		self.launched = True
		self.shown = True
		self.onscreen = True
		
	
	def draw(self):
		if self.shown and self.onscreen:
			if self.image:
				self.transform.rotate(self.angle)
				game.screen.blit(self.image, self.rect)
			else:
				self.shape(game.screen,color, self.rect)
		
	
	def loop(self):
		if self.launched:
			self.x = (math.sin(math.radians(self.angle))*self.distance) + self.startx
			self.y = (math.cos(math.radians(self.angle))*self.distance) + self.starty
			self.distance += self.speed
			
			self.screenX = player.x+(self.x-(self.width/2))+(game.get_screenwidth()/2)
			self.screenY = player.y-(self.y+(self.height/2))+(game.get_screenheight()/2)
			
			self.rect = pygame.Rect(int(self.screenX), int(self.screenY), self.width, self.height)	
			self.onscreen = self.rect.colliderect(game.screen.get_rect())
			
			if self.distance > self.truerange:
				self.launched = False
				self.shown = False
				game.projectiles.remove(self)
				del self
				pass
	


class Component:
	
	showname = True
	
	def __init__(self, name, x, y, width, height, color, world, showname=False, elliptical=False, health=10000, solid=False, textsize=50, damage=0, playerspeed=1, slip=0.5, imagename='', textcolor=(255, 255, 255), overrideshow=False, tp=None, noreturn=False):
		game.components.append(self)
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
		self.textcolor = textcolor
		self.screenX = 0
		self.screenY = 0
		self.rect = pygame.Rect(int(self.screenX), int(self.screenY), self.width, self.height)
		
		self.damage = damage
		self.damagetaken = 0
		self.damagecooldown = 15
		self.health = health
		self.solid = solid
		self.playerspeed = playerspeed
		self.slip = slip
		self.tp = tp
		if tp and not noreturn:
			self.tp.tp = self
			
		self.deleted = False
		self.shown = True
		self.overrideshow = overrideshow
		self.showname = showname
		self.onscreen = False
		
		self.imagename = imagename
		if self.imagename:
			self.image = pygame.image.load(self.imagename).convert_alpha()
			self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
		self.touchtimer = 0
		
	
	def draw(self):
		if self.shown:
			if self.imagename:
				game.screen.blit(self.image, (self.screenX, self.screenY, self.width, self.height))
			else:
				if self.elliptical:
					shape = pygame.draw.ellipse
				else:
					shape = pygame.draw.rect
					
				shape(game.screen, self.color, (self.screenX, self.screenY, self.width, self.height))
				
		if ((self.showname and Component.showname) or self.overrideshow) and self.shown:
			write(game.screen, 'font.ttf', self.textsize, self.screenX+self.width/2, self.screenY+self.height/2, self.name, self.textcolor, True)
		if self.damagecooldown < 5:
			player.displayText(self.damagetaken, int((self.damagetaken/2)+40))
	
	def loop(self):
		self.screenX = player.x+(self.x-(self.width/2))+(game.get_screenwidth()/2)
		self.screenY = player.y-(self.y+(self.height/2))+(game.get_screenheight()/2)
		self.rect = pygame.Rect(int(self.screenX), int(self.screenY), self.width, self.height)
		self.onscreen = self.rect.colliderect(game.screen.get_rect())
		
		self.collision()
		self.checkHealth()
		self.damagecooldown += 1
		
	
	def checkHealth(self):
		if self.health <= 0:
			self.shown = False
			self.deleted = True
		
	
	def randPos(self):
		self.x, self.y = self.world.randCoords()
		
	
	def collision(self):
		self.rect = pygame.Rect(self.screenX, self.screenY, self.width, self.height)
		if self.rect.colliderect(player.rect) and player.world == self.world and self.shown:
			player.touching.add(self)
			player.health -= self.damage
			
			if 'Range' in player.inventory[player.selected].keys():
				if player.get_selected_val('Range') == 0:
					self.health -= player.damage
		else:
			player.touching.discard(self)
			self.touchtimer += 1
			
		for projectile in game.projectiles:
			if self.rect.colliderect(projectile.rect):
				self.health -= projectile.damage
				self.damagecooldown = 0
				self.damagetaken = projectile.damage
		
	


# Town components
h_sidewalk = Component('Horizontal Sidewalk', 0, 0, town.width, 300, (185, 185, 185), town, False, False)
v_sidewalk = Component('Horizontal Sidewalk', 0, 0, 300, town.height, (185, 185, 185), town, False, False)
h_road = Component('Horizontal Road', 0, 0, town.width*1.25, 250, (50, 50, 50), town)
v_road = Component('Vertical Road', 0, 0, 250, town.height*1.25, (50, 50, 50), town)

# features
#pond_beach = Component('Pond Beach', 1950, 1625, 1000, 950, (204, 188, 148), town, False, True)
#pond = Component('Pond', 1975, 1650, 600, 565, (20, 150, 185), town, False, True)
volcano = Component('Volcano', 2250, -2250, 1250, 1250, (165, 128, 138), town, False, True)
lava = Component('Lava', 2250, -2250, 250, 250, (240, 185, 30), town, elliptical=True, damage=5, tp=heck)
cave = Component('Cave', -2500,  2600, 650, 300, (190, 190, 190), town)
#tree = Component('Tree', -1000, -1000, 180, 180, (50, 150, 60), town, False, True)
house = Component('House', 900, 350, 300, 200, house_interior.exteriorcolor, town, True)
restaurant = Component('Restaurant', -450, 350, 400, 200, (160, 160, 160), town, True)
gym = Component('Gym', -1100, 450, 300, 400, (135, 130, 140), town, True)
school = Component('School', 450, -400, 400, 300, school_interior.exteriorcolor, town, True)
office = Component('Office',  -490, -400, 300, 300, (160, 180, 180), town, True)
hospital = Component('Hospital', -400, 900, 300, 300, (210, 210, 210), town, True)
shop = Component('Shop', -950, -400, 400, 300, shop_interior.exteriorcolor,  town, True)
town_metro = Component('Metro - $100', 400, 2000, 300, 400, (100,100, 100), town, True)
cash = Component('$', town.randX(), town.randY(), 58, 30, (100, 150, 100), town, True, textsize=40, textcolor=(175, 250, 175), overrideshow=True)
cash2 = Component('$', town.randX(), town.randY(), 58, 30, (100, 150, 100), town, True, textsize=40, textcolor=(175, 250, 175), overrideshow=True)

# House components
quarter = Component('Quarter', house_interior.randX(), house_interior.randY(), 20, 20, (185, 185, 185), house_interior, elliptical=True)
bed = Component('Bed', 200, 200, 80, 120, (255, 0, 0), house_interior)
house_door = Component('House Door', -house_interior.width/2, 0, 20, 120, (190, 170, 80), house_interior, tp=house)
#house_door = Component('House Door', -house_interior.width/2, 0, 20, 120, (180, 150, 100), house_interior, tp=house)

shop_door = Component('Shop Door', 0, shop_interior.height/2, 240, 20, (255, 255, 255), shop_interior, tp=shop)
school_door = Component('School Door', 0, -school_interior.height/2, 200, 20, (110, 78, 48), school_interior, tp=school)

# City components
# streets
h_street = Component('Horizontal Street', 0, 0, city.width, 300, (50, 50, 50), city)
v_street = Component('Vertical Street', 0, 0, 300, city.height, (50, 50, 50), city)
#ocean_beach = Component('Ocean Beach', -4200, 0, 2910, 3500, (204, 188, 148), city, elliptical= rue)
#ocean = Component('Ocean', -4200, 0, 2000, 2500, (10, 140, 165), city, elliptical=True)
bank = Component('Bank', 400, 425, 300, 350, (25, 150, 75), city, True)
apartment = Component('Apartment', -400, -400,  300, 300, apartment_interior.exteriorcolor, city, True)
university = Component('University', -450, 450, 400, 400, (220, 190, 120), city, True)
city_metro = Component('Metro - $100', 400, 2000, 300, 400, (100,100, 100), city, True, tp=town_metro)
#town_metro.tp = city_metro
club = Component('Club - $500', 2000, -425, 300, 350, (255, 50, 170), city, True)
laboratory = Component('Laboratory', 1000, -425, 300, 350, (250, 250, 250), city, True, textcolor=(0, 0, 0))
credit_card = Component('Credit Card', city.randX(), city.randY(), 64, 36, (220, 200, 150), city, True, textsize=17)

apartment_door = Component('Apartment Door', apartment_interior.width/2, (-apartment_interior.height/2)+100, 20, 120, (110, 78, 48), apartment_interior, tp=apartment)

barn = Component('Barn', 0, 500, 350, 350, (220, 75, 25),  farm, True)
field1 = Component('Field 1', 750, 500, 700, 700, (70, 60, 0),  farm, True)
field2 = Component('Field 2', -750, 500, 700, 700, (70, 60, 0),  farm, True)
cheese_hut = Component('Cheese Hut', -1500, -1500,  300, 300, (250, 230, 50), farm, elliptical=True)


ice1 = Component('Ice 1', -1500, -1500, 1500, 1500, (100, 200, 230), snowland, slip=0.97)

cave_exit = Component('Cave Exit', cave_world.width/2, 0, 30, cave_world.height, (0, 0, 0), cave_world, tp=cave)
stone1 = Component('Stone 1', cave_world.randX(), cave_world.randY(), 70, 70, (140, 141, 143), cave_world)
stone2 = Component('Stone 2', cave_world.randX(), cave_world.randY(), 70, 70, (150, 151, 153), cave_world)
stone3 = Component('Stone 3', cave_world.randX(), cave_world.randY(), 70, 70, (145, 146, 148), cave_world)
gold = Component('Gold', cave_world.randX(), cave_world.randY(), 34, 32, (190, 170, 50), cave_world, elliptical=True)
silver = Component('Silver', cave_world.randX(), cave_world.randY(), 35, 37, (170, 170, 170), cave_world, elliptical=True)
copper = Component('Copper', cave_world.randX(), cave_world.randY(), 38, 40, (160, 120, 50), cave_world, elliptical=True)

dl_sign = Component('Daddyland Sign', 0, daddyland.height/2-500, 300, 200, (255, 255, 255), daddyland, tp=club)



if game.doproceduralgen:
	for i in range(game.worldgennum):
		newworld = World(*generator.genWorld())
	for i in range(game.componentgennum):
		newcomponent = Component(*generator.genComponent())
		print(newcomponent.rect)
		print(newcomponent.world)



class Block:
	
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
		if Block.viewangle > 0:
			game.blocks.sort(key = lambda theblock: -theblock.y) #Orders 3d block by Y-position so they dont overlap.
		
	
	def __init__(self, name, x, y, width, height, world, solid):
		game.blocks.append(self)
		self.name = name
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.world = player.world
		self.deleted = False
		self.color1 = Block.types[name]['Color1']
		self.color2 = Block.types[name]['Color2']
		self.solid = solid
		self.screenX = -200
		self.screenY = -200
		self.rect = pygame.Rect(self.screenX, self.screenY, self.width, self.height)
		
		self.playertouch = False
		Block.count += 1
		game.blocks.append(self)
		self.bordered = True
		self.depth = 0
		self.slip = 0
		self.playerspeed = 1
		self.onscreen = True
		self.shown = True
		self.tallness = 0
		
	
	def draw(self):
		if self.world == player.world and not self.deleted:
			pygame.draw.rect(game.screen, self.color2, (self.screenX, self.screenY-self.tallness, self.width, self.height+self.tallness))
			pygame.draw.rect(game.screen, self.color1, (self.screenX + (Block.padding/2), self.screenY + (Block.padding/2)-self.tallness, self.width-Block.padding, self.height-Block.padding))
		
	
	def loop(self):
		self.tallness = max(0, Block.viewangle)
		
		#self.x = roundto(self.x, self.world.tilesize)
		#self.y = roundto(self.y, self.world.tilesize)
		self.screenX = player.x+(-self.x-(self.width/2))+(game.get_screenwidth()/2)
		self.screenY = player.y-(self.y+(self.height/2))+(game.get_screenheight()/2)
		self.rect = pygame.Rect(int(self.screenX), int(self.screenY), self.width, self.height)
		self.truerect = pygame.Rect(int(self.screenX), int(self.screenY-self.tallness), self.width, self.height+int(self.tallness))
		self.onscreen = self.rect.colliderect(game.screen.get_rect())
		
		self.collision()
		
	
	def collision(self):
		if self.rect.colliderect(player.rect):
			player.touching.add(self)
		else:
			player.touching.discard(self)
	


class Stat:
	
	startposition = 3
	textsize = 28
	shown = True
	detailed = False
	stats = []
	
	@classmethod
	def retrieveStats(cls):
		Stat.stats.clear()
		worldstat = Stat('World', player.world.name, True)
		xstat = Stat('X', -player.x, True)
		ystat = Stat('Y', player.y, True)
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
		timestat = Stat('Time elapsed', game.seconds, True)
		framestat = Stat('Frames', game.frames, True)
		fpsstat = Stat('FPS', game.clock.get_fps(), True)
		
	
	@staticmethod
	def get_names(var):
		strings = list(map(lambda x: x.name, var))
		string = ', '.join(strings)
		if not var:
			return 'None'
		return string
		
	
	def __init__(self, name, stat, detailed=False):
		self.detailed = detailed
		self.do = (self.detailed and Stat.detailed) or not self.detailed
		if self.do:
			Stat.stats.append(self)
		self.name = name
		self.stat = stat
		self.spacing = 18
		self.x = 5
		self.y = 0
		
	
	def draw(self, position):
		stat = self.stat
		self.y = game.get_screenheight()-(position*self.spacing) - self.startposition
		if type(stat) == float or type(stat) == int:
			stat = int(round(stat))
		name = self.name + ':  ' + str(stat)
		if self.name == 'Time elapsed':
			minutesFormatting = str(game.minutes)
			secondsFormatting = str(game.seconds)
			if game.minutes <= 9:
				minutesFormatting = '0' + str(game.minutes)
			if game.seconds <= 9:
				secondsFormatting = '0' + str(game.seconds)
			name = (self.name + ': ' + minutesFormatting + ':' + secondsFormatting)
		if Stat.shown:
			write(game.screen, 'font.ttf', Stat.textsize, self.x, self.y, name, (255, 255, 255))
		
	

game.loopitems = [game.components, game.blocks, game.projectiles, game.characters]


while game.running:
	game.play()
	debug()
pygame.quit()
sys.exit()
