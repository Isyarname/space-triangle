import pygame as p
from random import randint as r

RED = (226,0,0)
ORANGE = (255, 80, 80)
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
		form = [(self.x,self.y),(self.x-1,self.y+1),(self.x+2,self.y-1),
		(self.x-1,self.y-1),(self.x+1,self.y+1),(self.x,self.y-2)]
		p.draw.polygon(self.surface, self.color, form)


class Enemy:
	def __init__(self, surf, diff, theme, Width):
		self.hp = self.depth = r(16, 25)
		if theme == "синий":
			self.color = (0, self.depth * 5, 400 - self.depth * 10)
			self.hpColor = RED
		elif theme == "чб":
			c = self.depth * 10
			self.color = (c, c, c)
			self.hpColor = (130, 130, 130)
		self.v = r(4 - self.depth//8 + diff//3, 4 - self.depth//8 + diff//2)
		self.surface = surf
		if self.depth == 25 and r(0,1) == 1:
			self.bonus = True
		else:
			self.bonus = False
		self.depth = self.depth * Width // 1200
		self.y = -self.depth
		self.x = r(self.depth * 2, Width - self.depth * 2)

	def draw(self):
		self.y += self.v
		form = [(self.x-self.depth, self.y+self.depth),
		(self.x+self.depth, self.y+self.depth),
		(self.x+self.depth, self.y-self.depth), (self.x-self.depth, self.y-self.depth)]
		hpForm = [(self.x-self.hp, self.y+self.depth+4),
		(self.x+self.hp, self.y+self.depth+4), (self.x+self.hp, self.y+self.depth+3),
		(self.x-self.hp, self.y+self.depth+3)]
		p.draw.polygon(self.surface, self.color, form)
		p.draw.polygon(self.surface, self.hpColor, hpForm)
		if self.bonus == True:
			bForm = [(self.x-3, self.y+3), (self.x+3, self.y+3),
			(self.x+3, self.y-3), (self.x-3, self.y-3)]
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
		
	def draw(self):
		self.y -= self.v
		self.x += self.direction
		form = [(self.x-2,self.y+self.lenght),(self.x+2,self.y+self.lenght),
		(self.x+2,self.y-self.lenght),(self.x-2,self.y-self.lenght)]
		p.draw.polygon(self.surface, self.color, form)


class Player:
	def __init__(self, surf, Width, Height, theme, fsc):
		self.name = "введите имя"
		self.scWidth = Width
		self.scHeight = Height
		self.depth = Width // 120
		self.x = self.scWidth // 2
		self.y = self.scHeight - self.depth * 2
		if fsc:
			self.y -= 34
		if theme == "синий":
			self.color = (100,255,255)
			self.hpColor = RED
		elif theme == "чб":
			self.color = (203, 203, 203)
			self.hpColor = (130, 130, 130)
		self.v = 6 * Width // 1200
		self.motion = "stop"
		self.shot = False
		self.surface = surf
		self.points = self.highscore = 0
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
		form = [(self.x, self.y-self.depth),
		(self.x-self.depth, self.y+self.depth+1), (self.x+self.depth, self.y+self.depth+1)]
		hpForm = [(0, 0), (0, 5), (self.scWidth*self.hp//self.maxHp, 5),
		(self.scWidth*self.hp//self.maxHp, 0)]
		p.draw.polygon(self.surface, self.color, form)
		p.draw.polygon(self.surface, self.hpColor, hpForm)


class Button:
	def __init__(self, x, y, surf, size, color):
		self.pressure = False
		self.surface = surf
		self.color = color
		self.textColor = textColor
		self.size = size
		self.f = p.font.Font(font, self.size)
		self.x = x
		self.y = y
		self.h = size * 10 // 19 + 7
		self.w = 10

	def draw(self, txt, Width):
		text = self.f.render(txt, 1, self.textColor)
		self.w = len(txt) * self.size // 3 + 10
		if self.x - self.w < 5:
			self.x -= (self.x - self.w) - 5
		elif self.x + self.w > Width - 5:
			self.x -= (self.x + self.w) - (Width - 5)
		place = text.get_rect(center=(self.x,self.y))
		form = [(self.x - self.w, self.y - self.h), (self.x + self.w, self.y - self.h),
		(self.x + self.w, self.y + self.h), (self.x - self.w, self.y + self.h)]
		p.draw.polygon(self.surface, self.color, form)
		self.surface.blit(text, place)


class Bonus:
	def __init__(self, surf, x, y, theme):
		self.surface = surf
		self.x = x
		self.y = y
		self.v = 2
		self.depth = 10
		if theme == "чб":
			self.color1 = (138, 138, 138)
			self.color2 = (76, 76, 76)
		elif theme == "синий":
			self.color1 = ORANGE
			self.color2 = RED

	def draw(self):
		self.y += self.v
		d = self.depth // 2
		form1 = [(self.x-self.depth, self.y+self.depth),
		(self.x+self.depth, self.y+self.depth), (self.x+self.depth, self.y-self.depth),
		(self.x-self.depth, self.y-self.depth)]
		form2 = [(self.x-d, self.y+self.depth), (self.x+d, self.y+self.depth),
		(self.x+d, self.y+d), (self.x+self.depth, self.y+d),
		(self.x+self.depth, self.y-d),(self.x+d, self.y-d),
		(self.x+d, self.y-self.depth), (self.x-d, self.y-self.depth),
		(self.x-d, self.y-d), (self.x-self.depth, self.y-d),
		(self.x-self.depth, self.y+d), (self.x-d, self.y+d)]
		p.draw.polygon(self.surface, self.color1, form1)
		p.draw.polygon(self.surface, self.color2, form2)