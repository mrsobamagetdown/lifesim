import pygame
import random
import math

from globfuns import *
from world import *
from block import *
import proceduralgen


game = None
player = None


class Component:
	
	components = []
	showname = True
	
	def __init__(self, name, x, y, width, height, color, world, showname=False, elliptical=False, health=10000, solid=False, textsize=65, damage=0, bumphit=False, playerspeed=1, slip=0.5, imagename='', textcolor=(255, 255, 255), overrideshow=False, condition='True', command='pass', interactive=False, replenish=False, tp=None, noreturn=False):
		Component.components.append(self)
		
		self.name = name
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.color = color
		self.world = world
		self.showname = showname
		self.elliptical = elliptical
		if self.elliptical:
			self.shape = pygame.draw.ellipse
		else:
			self.shape = pygame.draw.rect
		self.textsize = textsize
		self.textcolor = textcolor
		self.screenX = -self.width
		self.screenY = -self.height
		self.rect = screenRect(self)
		
		self.damage = damage
		self.damagetaken = 0
		self.damagecooldown = 15
		self.bumphit = bumphit
		self.health = health
		self.solid = solid
		self.playerspeed = playerspeed
		self.slip = slip
		
		self.condition = condition
		self.command = command
		self.interactive = interactive
		self.replenish = replenish
		self.tp = tp
		if tp and not noreturn:
			self.tp.tp = self
		
		self.touching = set([])
		self.deleted = False
		self.visible = True
		self.overrideshow = overrideshow
		self.showname = showname
		self.onscreen = False
		self.imagename = imagename
		self.image = createImage(self, imagename)
		
	
	def update(self):
		self.screenX = player.x+(self.x-(self.width/2))+(game.width/2)
		self.screenY = player.y-(self.y+(self.height/2))+(game.height/2)
		self.rect = screenRect(self)
		self.onscreen = self.rect.colliderect(game.screen.get_rect())
		self.damagecooldown += 1
		
	
	def draw(self):
		if self.visible and player.world is self.world:
			if self.imagename:
				game.screen.blit(self.image, self.rect)
			if self.color:
				self.shape(game.screen, self.color, self.rect)
			if ((self.showname and Component.showname) or self.overrideshow) and self.visible:
				write(game.screen, game.font, self.textsize, self.screenX+self.width/2, self.screenY+self.height/2, self.name, self.textcolor, True)
			if self.damagecooldown < 5:
				player.damage += self.damagetaken
			
	
	def act(self):
		self.collision()
		self.checkHealth()
		
	
	def checkHealth(self):
		if self.health <= 0:
			self.visible = False
			self.deleted = True
			self.health = max(self.health, 0)
		
	
	def collision(self, damageplayer=True):
		if self.rect.colliderect(player.rect) and player.world == self.world and self.visible:
			if not self.bumphit or (self.bumphit and not self in player.touching):
				player.touching.add(self)
				self.touching.add(player)
				if damageplayer:
					player.health -= self.damage
				if eval(self.condition):
					if not player.checkRanged:
						self.health -= player.damage
					if self.interactive:
						game.drawfinger = True
					if (self.interactive and game.BUTTON1 and game.KEYTAPPED or game.MOUSECLICKED) or not self.interactive:
						exec(self.command)
						if self.replenish:
							self.x, self.y = self.world.randX(), self.world.randY()
			if self.tp and player.canteleport:
				game.drawfinger = True
				if game.BUTTON1 and (game.MOUSECLICKED or game.KEYTAPPED):
					player.tp(self.tp)
		else:
			self.touching.discard(player)
			player.touching.discard(self)
		
		for item in game.entities:
			if self.rect.colliderect(item.rect) and item is not self:
				if (item.bumphit and not item in self.touching) or not item.bumphit:
					self.touching.add(item)
					self.health -= item.damage
					self.damagecooldown = 0
					self.damagetaken = item.damage
					self.touching.add(item)
			else:
				self.touching.discard(item)
		
	
	def randPos(self):
		self.x = self.world.randX()
		self.y = self.world.randY()
	



# Town components
hsidewalk = Component('Horizontal Sidewalk', 0, 0, town.width, 400, (185, 185, 185), town, False)
vsidewalk = Component('Horizontal Sidewalk', 0, 0, 400, town.height, (185, 185, 185), town, False)
hroad = Component('Horizontal Road', 0, 0, town.width*1.25, 300, (50, 50, 50), town)
vroad = Component('Vertical Road', 0, 0, 300, town.height*1.25, (50, 50, 50), town)

# features
#pond_beach = Component('Pond Beach', 1950, 1625, 1000, 950, (204, 188, 148), town, False, True)
#pond = Component('Pond', 1975, 1650, 600, 565, (20, 150, 185), town, False, True)
volcano = Component('Volcano', 3500, -3500, 1250, 1250, (165, 128, 138), town, False, elliptical=True)
lava = Component('Lava', volcano.x, volcano.y, 250, 250, (240, 185, 30), town, False, elliptical=True, damage=5, tp=heck)
cave = Component('Cave', -4000,  4500, 650, 300, (190, 190, 190), town)
#tree = Component('Tree', -1000, -1000, 180, 180, (50, 150, 60), town, False, True)
house = Component('House', 600, 550, 500, 400, houseinterior.outercolor, town, True)
restaurant = Component('Restaurant', -600, 550, 500, 400, (255, 213, 125), town, True, condition='player.canPay()', command='player.energy+=0.5; player.money-=0.5; player.weight+=0.5; player.strength-=0.25; player.happiness+=1;')

gym = Component('Gym', -1300, 650, 500, 600, (135, 130, 140), town, True, condition='player.canPay()', command='player.strength+=0.5; player.weight-=0.125; player.money-=0.5; player.energy-=0.5; player.happiness-=0.5')
school = Component('School', 650, -550, 600, 400, schoolinterior.outercolor, town, True, command='player.intelligence+=0.5; player.energy-=0.25; player.happiness-=0.5')
office = Component('Office',  -600, -600, 500, 500, (160, 180, 180), town, True, command='player.money+=(player.intelligence/100); player.energy-=0.5; player.happiness-=0.75')
hospital = Component('Hospital', -600, 1200, 500, 500, (210, 210, 210), town, True, condition='player.canPay()', command='player.health+=1; player.energy+=1; player.money-=1')
shop = Component('Shop', -1350, -550, 600, 400, shopinterior.outercolor,  town, True)
townmetro = Component('Metro - $100', 600, 2050, 500, 600, (100,100, 100), town, True, interactive=True, condition='player.canPay(100)', command='player.tp(city)')


for i in range(2):
	cash = Component('$', town.randX(), town.randY(), 60, 32, (100, 155, 100), town, True, textsize=38, textcolor=(175, 250, 175), overrideshow=True, command='player.money += 10; print("yeeeeeeeet")', replenish=True)


housedoor = Component('House Door', -houseinterior.width/2, 0, 20, 120, (190, 170, 80), houseinterior, tp=house)
quarter = Component('Quarter', houseinterior.randX(), houseinterior.randY(), 20, 20, (185, 185, 185), houseinterior, elliptical=True, command='player.money+=1; self.randPos()')
bed = Component('Bed', 200, 200, 80, 120, (255, 0, 0), houseinterior)

shopdoor = Component('Shop Door', 0, shopinterior.height/2, 240, 20, (255, 255, 255), shopinterior, tp=shop)

schooldoor = Component('School Door', 0, -schoolinterior.height/2, 200, 20, (110, 78, 48), schoolinterior, tp=school)


hstreet = Component('Horizontal Street', 0, 0, city.width, 300, (50, 50, 50), city)
vstreet = Component('Vertical Street', 0, 0, 300, city.height, (50, 50, 50), city)
bank = Component('Bank', 700, 600, 700, 500, (25, 150, 75), city, True, command='player.money*=1.12; player.happiness-=player.money/20; player.energy-=0.5')
apartment = Component('Apartment', -600, -700,  500, 700, apartmentinterior.outercolor, city, True)
university = Component('University', -650, 650, 600, 600, (220, 190, 120), city, True,  condition='player.age >= 18 && player.canPay(1)', command='player.money-=1; player.intelligence*=1.2; player.happiness-=0.5; player.energy-=0.5')
citymetro = Component('Metro - $100', 600, 2200, 500, 600, (100,100, 100), city, True, tp=townmetro, condition='player.canPay(100)', interactive=True, command='player.money-=0.5')
museum = Component('Museum', 1550, 650, 600, 600, (10, 10, 10), city, True, condition='player.canPay()', command='player.happiness += 0.5; player.money-=0.75')
laboratory = Component('Laboratory', 1200, -625, 500, 550, (250, 250, 250), city, True, textcolor=(0, 0, 0))
creditcard = Component('Credit Card', city.randX(), city.randY(), 64, 36, (220, 200, 150), city, True, textsize=17)

apartmentdoor = Component('Apartment Door', apartmentinterior.width/2, (-apartmentinterior.height/2)+100, 20, 120, (110, 78, 48), apartmentinterior, tp=apartment)

barn = Component('Barn', 0, 500, 550, 550, (220, 75, 25),  farm, True)
field1 = Component('Field 1', -2250, 2000, 1400, 1900, (70, 60, 0),  farm, True)
field2 = Component('Field 2', 2000, -2250, 1900, 1400, (70, 60, 0),  farm, True)
cheese_hut = Component('Cheese Hut', -1500, -1500,  300, 300, (250, 230, 50), farm, elliptical=True)

caveexit = Component('Cave Exit', caveland.width/2, 0, 30, caveland.height, (0, 0, 0), caveland, tp=cave)

