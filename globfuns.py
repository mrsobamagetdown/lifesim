import pygame
import random
import math

pygame.display.init()

def roundTo(x, base):
	return base*round(float(x)/base)
	

def restrict(value, minvalue, maxvalue):
    return max(minvalue, min(value, maxvalue))


def screenRect(item, screen=True, xinflate=0, yinflate=0):
	if screen:
		x, y, = item.screenX, item.screenY
	else:
		x, y = item.x, item.y
	rect = pygame.Rect(x, y, item.width+xinflate, item.height+yinflate)
	return rect


def loadImage(imagename, fileending='png'):
	image = pygame.image.load('Images/' + imagename + '.' + fileending).convert_alpha()
	return image


def createImage(item, imagename, fileending='png'):
	if imagename:
		image = loadImage(imagename, fileending)
		image = pygame.transform.smoothscale(image, (item.width, item.height))
		return image
	return None



fonts = {}
def write(surface, fontFace, size, x, y, text, color, center=False):
	if size in fonts:
		Font = fonts[size]
	else:
		Font = pygame.font.SysFont(fontFace, size)
		fonts[size] = Font
	text = Font.render(text, 1, color)
	
	if center:
		text_rect = text.get_rect(center=(x, y))
	else:
		text_rect = (x, y)
	surface.blit(text, text_rect)
	


