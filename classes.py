import pygame as p
from random import randint as r

RED = (226,0,0)
font = "pixelFont.otf"
textColor = (0,0,0)


class Sequin:
	def __init__(self, surf, diff, theme, Width):
		self.surface = surf
		self.x = r(0, Width)
		self.y = 0
		self.v = r(diff//3 + 1, diff//2 + 2)
		if theme == "чб":
			c = r(40, 100)
			self.color = (c, c, c)
		elif theme == "синий":
			self.color = (r(0,150), r(0,150), r(0,150))

	def draw(self):
		self.y += self.v
		form = [(self.x,self.y),(self.x-1,self.y+1),(self.x+2,self.y-1),(self.x-1,self.y-1),(self.x+1,self.y+1),(self.x,self.y-2)]
		p.draw.polygon(self.surface, self.color, form)


class Enemy:
	def __init__(self, surf, diff, theme, Width):
		self.hp = self.depth = r(16, 24)
		if theme == "синий":
			self.color = (0, self.depth * 5, 400 - self.depth * 10)
			self.hpColor = RED
		elif theme == "чб":
			c = self.depth * 10
			self.color = (c, c, c)
			self.hpColor = (200, 200, 200)
		self.v = r(3 - self.depth // 8 + diff // 2, 4 - self.depth // 8 + diff // 2)
		self.surface = surf
		if self.depth == 24:
			self.bonus = True
		else:
			self.bonus = False
		self.depth = self.depth * Width // 1200
		self.y = -self.depth
		self.x = r(self.depth * 2, Width - self.depth * 2)

	def draw(self):
		self.y += self.v
		form = [(self.x-self.depth, self.y+self.depth), (self.x+self.depth, self.y+self.depth), (self.x+self.depth, self.y-self.depth), (self.x-self.depth, self.y-self.depth)]
		hpForm = [(self.x-self.hp, self.y+self.depth+3), (self.x+self.hp, self.y+self.depth+3), (self.x+self.hp, self.y+self.depth+2), (self.x-self.hp, self.y+self.depth+2)]
		p.draw.polygon(self.surface, self.color, form)
		p.draw.polygon(self.surface, self.hpColor, hpForm)
		if self.bonus == True:
			bForm = [(self.x-2, self.y+2), (self.x+2, self.y+2), (self.x+2, self.y-2), (self.x-2, self.y-2)]
			p.draw.polygon(self.surface, self.hpColor, bForm)


class Bullet:
	def __init__(self, x, y, surf, direct, v, theme):
		self.x = x
		self.y = y
		if theme == "синий":
			self.color = (80,120,200)
		elif theme == "чб":
			self.color = (133, 133, 133)
		self.v = v
		self.surface = surf
		self.depth = (12 - self.v)//2
		self.lenght = 3
		self.direction = direct

	def movement(self):
		if self.direction == "right":
			self.x += self.v*1//10
			self.y -= self.v*9//10
		elif self.direction == "left":
			self.x -= self.v*1//10
			self.y -= self.v*9//10
		else:
			self.y -= self.v

	def draw(self):
		self.movement()
		form = [(self.x-2,self.y+self.lenght),(self.x+2,self.y+self.lenght),(self.x+2,self.y-self.lenght),(self.x-2,self.y-self.lenght)]
		p.draw.polygon(self.surface, self.color, form)


class Player:
	def __init__(self, surf, Width, Height, theme, fsc):
		self.scWidth = Width
		self.scHeight = Height
		self.depth = Width // 120
		self.x = self.scWidth // 2
		self.y = self.scHeight - self.depth * 2
		if fsc:
			self.y -= 34
		if theme == "синий":
			self.color = (100,255,255)
		elif theme == "чб":
			self.color = (203, 203, 203)
		self.v = 6 * Width // 1200
		self.motion = "stop"
		self.shot = False
		self.surface = surf
		self.points = 0
		self.hp = self.maxHp = 200
		self.level = 1
		self.mode = 0
		self.recharge = 0

	def left(self):
		self.x -= self.v + self.points // 30

	def right(self):
		self.x += self.v + self.points // 30

	def movement(self):
		if self.motion == "left":
			self.left()
		if self.motion == "right":
			self.right()
		if self.x > self.scWidth:
			self.x = 0
		if self.x < 0:
			self.x = self.scWidth

	def draw(self):
		self.movement()
		form = [(self.x, self.y-self.depth), (self.x-self.depth, self.y+self.depth+1), (self.x+self.depth, self.y+self.depth+1)]
		hpForm = [(0, 0), (0, 5), (self.scWidth*self.hp//self.maxHp, 5), (self.scWidth*self.hp//self.maxHp, 0)]
		p.draw.polygon(self.surface, self.color, form)
		p.draw.polygon(self.surface, RED, hpForm)


class Button:
	def __init__(self, x, y, w, h, surf, size, color):
		self.pressure = False
		self.surface = surf
		self.color = color
		self.textColor = textColor
		self.f = p.font.Font(font, size)
		self.x = x
		self.y = y
		self.h = h
		self.w = w

	def draw(self, txt):
		text = self.f.render(txt, 1, self.textColor)
		place = text.get_rect(center=(self.x,self.y))
		form = [(self.x - self.w, self.y - self.h), (self.x + self.w, self.y - self.h), (self.x + self.w, self.y + self.h), (self.x - self.w, self.y + self.h)]
		p.draw.polygon(self.surface, self.color, form)
		self.surface.blit(text, place)