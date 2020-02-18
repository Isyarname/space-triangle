import pygame as p
from random import randint as r

Width = 1200
Height = 600
RED = (226,0,0)
sc = p.display.set_mode((Width, Height))


class Sequin:
	def __init__(self, surf, diff):
		self.surface = surf
		self.x = r(0,Width)
		self.y = 0
		self.v = r(diff//3 + 1, diff//3 + 4)
		self.color = (r(0,200), r(0,200), r(0,200))

	def draw(self):
		self.y += self.v
		form = [(self.x,self.y),(self.x-1,self.y+1),(self.x+2,self.y-1),(self.x-1,self.y-1),(self.x+1,self.y+1),(self.x,self.y-2)]
		p.draw.polygon(self.surface, self.color, form)


class Enemy:
	def __init__(self, surf, diff):
		self.color = (0,r(180,240),r(140,180))
		self.hp = self.depth = r(16, 24)
		self.v = r(3 - self.depth//8 + diff//2, 4 - self.depth//8 + diff//2)
		self.y = -self.depth
		self.x = r(10, Width - 10)
		self.surface = surf
		if self.depth == 24:
			self.bonus = True
		else:
			self.bonus = False

	def draw(self):
		self.y += self.v
		form = [(self.x-self.depth, self.y+self.depth), (self.x+self.depth, self.y+self.depth), (self.x+self.depth, self.y-self.depth), (self.x-self.depth, self.y-self.depth)]
		hpForm = [(self.x-self.hp, self.y+self.depth+3), (self.x+self.hp, self.y+self.depth+3), (self.x+self.hp, self.y+self.depth+2), (self.x-self.hp, self.y+self.depth+2)]
		p.draw.polygon(self.surface, self.color, form)
		p.draw.polygon(self.surface, RED, hpForm)
		if self.bonus == True:
			bForm = [(self.x-2, self.y+2), (self.x+2, self.y+2), (self.x+2, self.y-2), (self.x-2, self.y-2)]
			p.draw.polygon(self.surface, RED, bForm)


class Bullet:
	def __init__(self, x, y, surf, direct, v):
		self.x = x
		self.y = y
		self.color = (80,120,200)
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
	def __init__(self,surf):
		self.depth = 10
		self.x = Width//2
		self.y = Height-self.depth*2
		self.color = (100,255,255)
		self.v = 6
		self.motion = "stop"
		self.shot = False
		self.surface = surf
		self.points = 0
		self.hp = self.maxHp = 200
		self.level = 1
		self.mode = 0

	def left(self):
		self.x -= self.v + self.points // 30

	def right(self):
		self.x += self.v + self.points // 30

	def movement(self):
		if self.motion == "left":
			self.left()
		if self.motion == "right":
			self.right()
		if self.x > Width:
			self.x = 0
		if self.x < 0:
			self.x = Width

	def draw(self):
		self.movement()
		form = [(self.x,self.y-self.depth),(self.x-self.depth,self.y+self.depth+1),(self.x+self.depth,self.y+self.depth+1)]
		hpForm = [(0,0),(0,5),(Width*self.hp//self.maxHp,5),(Width*self.hp//self.maxHp,0)]
		p.draw.polygon(self.surface, self.color, form)
		p.draw.polygon(self.surface, RED, hpForm)


class Button:
	def __init__(self, x, y, w, h, surf, font, size, color, textColor):
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
		sc.blit(text, place)