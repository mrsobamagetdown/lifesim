#import lifesim
import random

# TODO: Reconfigure init params to v7



def randColor():
	levels = range(32,256,32)
	color =  tuple(random.choice(levels) for _ in range(3))
	return color

def randBool():
	val = bool(random.getrandbits(1))
	return val

class generation:
	worlds = []
	components = []
	
	def genWorld(self):
		# (name, width, height, color, exteriorcolor=None, walled=False, borderdamage=0, borderspeed=1, slip = 0.5)
		
		#name = randWord.get_random_word()
		name = 'Procedurally generated world' + ' ' + str(len(generation.worlds))
		width = random.randint(200, 30000)
		height = random.randint(200, 30000)
		color = randColor()
		exteriorcolor = randColor()
		walled = randBool()
		borderdamage = random.choice((0, 0, random.uniform(0, 5)))
		borderspeed = random.choice((1, 1, random.uniform(0.65, 1)))
		slip = random.choice((0.5, 0.5, random.uniform(0.15, 0.75)))
		
		newworld = [name, width, height, color, exteriorcolor, walled, borderdamage, borderspeed, slip]
		generation.worlds.append(newworld)
		return newworld


	def genComponent(self):
		# (self, name, x, y, width, height, color, world, showname=False, elliptical=False, health=10000, solid=False,
		# textsize=50, damage=0, playerspeed=1, slip=0.5, imagename='', textcolor=(255, 255, 255), overrideshow=False,
		# tp=None, noreturn=False)
		
		#name = randWord.get_random_word()
		name = 'Procedurally generated component' + ' ' + str(len(generation.components))
		world = random.choice(generation.worlds)
		
		distmult = 1
		if not world[5]:
			# If world is not walled, this allows component to be spawned outside the world
			distmult = 2
		x = random.randint(-world[1]*distmult, world[1]*distmult)
		y = random.randint(-world[2]*distmult, world[2]*distmult)
		width = random.randint(25, 500)
		height = random.randint(25, 500)
		color = randColor()
		showname = randBool()
		elliptical = randBool()
		health = random.randint(1, 50000)
		solid = randBool()
		textsize = random.randint(25, 75)
		damage = random.choice((0, 0, random.uniform(0, 5)))
		playerspeed = random.choice((1, 1, random.uniform(0.75, 1.25)))
		slip = random.uniform(0.25, 0.75)
		imagename = ''
		textcolor = (255, 255, 255)
		overrideshow = False
		tp = None
		tpcomponent = None
		if generation.components:
			tpcomponent = random.choice(generation.components)
			if not tpcomponent[19]:
				# Sets tp destination to random procedurally generated component unless the random one already has a tp destination
				tp = random.choice((None, None, tpcomponent[19]))
		noreturn =random.choice((False, False, False, True))
		newcomponent = [name, x, y, width, height, color, world, showname, elliptical, health, solid, textsize, damage, playerspeed, slip, '', textcolor, overrideshow, tp, noreturn]
		generation.components.append(newcomponent)
		return newcomponent
		
