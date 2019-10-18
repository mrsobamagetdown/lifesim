import pygame
import random
import math

from globfuns import *


class Stat:
	
	startposition = 3
	textsize = 28
	visible = True
	detailed = False
	formatminutes = True
	stats = []
	
	game = None
	player = None
	
	# Create string of all names of items in a list or set
	@staticmethod
	def getNames(var):
		strings = list(map(lambda x: x.name, var))
		strings = ', '.join(strings)
		if not var:
			return 'None'
		return strings
		
	@classmethod
	def retrieveStats(cls):
		player = cls.player
		game = cls.game
		
		cls.stats.clear()
		cls.startposition = game.height-3
		
		worldstat = Stat('World', player.world.name, True)
		xstat = Stat('X', -player.x, True)
		ystat = Stat('Y', player.y, True)
		itemstat = Stat('Item selected', str(player.getSelectedVal('Amount'))+' * '+player.selected) #+' Type: '+str(player.getSelectedVal('Type')))
		healthstat = Stat('Health', player.health)
		agestat = Stat('Age', player.age)
		energystat = Stat('Energy', player.energy)
		weightstat = Stat('Weight', player.weight)
		strengthstat = Stat('Strength', player.strength)
		happinessstat = Stat('Happiness', player.happiness)
		intelstat = Stat('Intelligence', player.intelligence)
		moneystat = Stat('Cash', player.money)
		speedstat = Stat('Speed', player.speed, True)
		touchingstat=Stat('Touching', Stat.getNames(player.touching), True)
		timestat = Stat('Time elapsed', (game.minutes, game.seconds), True)
		framestat = Stat('Frames', game.frames, True)
		fpsstat = Stat('FPS', game.clock.get_fps(), True)
		
		
	@classmethod
	def drawStats(cls):
		if cls.visible:
			for stat in cls.stats:
				if stat.visible:
					stat.format()
					write(cls.game.screen, 'font.ttf', Stat.textsize, stat.x, stat.y, stat.stat, (255, 255, 255))
		
	
	def __init__(self, name, val, detailed=False):
		self.detailed = detailed
		self.do = (self.detailed and Stat.detailed) or not self.detailed
		if self.do:
			Stat.stats.append(self)
		self.name = name
		self.val = val
		self.stat = ''
		self.spacing = 18
		self.x = 5
		self.y = 0
		
	
	def format(self):
		position = len(Stat.stats)-Stat.stats.index(self)
		val = self.val
		self.y = self.startposition-(position*self.spacing)
		if type(val) == float:
			val = int(round(val))
		if self.name == 'Time elapsed' and Stat.formatminutes:
			minutes = val[0]
			seconds = val[1]
			if minutes <= 9:
				minutes = '0' + str(minutes)
			if seconds <= 9:
				seconds = '0' + str(seconds)
			val = (str(minutes) + ':' + str(seconds))
		stat = self.name + ':  ' + str(val)
		self.stat = stat
	


#from lifesim import *

