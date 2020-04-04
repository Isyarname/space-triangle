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

	def draw(self, move):
		if move:
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
		self.bonus = False
		if self.depth == 25 and r(0,1) == 1:
			self.bonus = True
		self.depth = self.depth * Width // 1200
		self.y = -self.depth
		self.x = r(self.depth * 2, Width - self.depth * 2)

	def draw(self, move):
		if move:
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
	def __init__(self, x, y, surf, vx, vy, theme, type):
		self.type = type
		self.x = x
		self.y = y
		if theme == "синий":
			self.color = (80,120,200)
		elif theme == "чб":
			self.color = (133, 133, 133)
		self.vy = vy
		self.surface = surf
		self.depth = (12 - self.vy)
		self.lenght = 3
		self.vx = vx
		
	def draw(self, move):
		if move:
			if self.type == 1:
				self.y -= self.vy
			else:
				self.y += self.vy
			self.x += self.vx
		form = [(self.x-2,self.y+self.lenght),(self.x+2,self.y+self.lenght),
		(self.x+2,self.y-self.lenght),(self.x-2,self.y-self.lenght)]
		p.draw.polygon(self.surface, self.color, form)


class Player:
	def __init__(self, surf, Width, Height, theme, fsc):
		self.name = "введите имя"
		self.scWidth = Width
		self.time = 0
		self.scHeight = Height
		self.depth = Width // 110
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
		self.motion = []
		self.shot = False
		self.surface = surf
		self.points = self.highscore = 0
		self.hp = self.maxHp = 600
		self.level = 1
		self.mode = 1
		self.recharge = 0

	def left(self, v):
		self.x -= v

	def right(self, v):
		self.x += v

	def up(self, v):
		self.y -= v

	def down(self, v):
		self.y += v

	def movement(self):
		v = self.v + self.points // 30
		if p.K_LEFT in self.motion:
			self.left(v)
		elif p.K_RIGHT in self.motion:
			self.right(v)
		if p.K_UP in self.motion and self.y > 0:
			self.up(v)
		elif p.K_DOWN in self.motion and self.y < self.scHeight:
			self.down(v)
		if self.x > self.scWidth:
			self.x = 0
		elif self.x < 0:
			self.x = self.scWidth

	def draw(self, move):
		if move:
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
	def __init__(self, surf, x, y, theme, level, points, type="random", bossIndex=1):
		self.surface = surf
		self.x = x
		self.y = y
		self.v = 2
		self.depth = 10
		self.type = type
		if self.type == "random":
			if r(0,1) == 1 and level - 1 < bossIndex and level < 3:
				self.type = 2	
			else:
				self.type = 1
		if self.type == 2:
			self.textColor = textColor
			size = 20
			self.w = size // 3 + 3
			self.h = size * 10 // 19 + 5
			self.f = p.font.Font(font, size)
			if theme == "чб":
				self.color = (99, 99, 99)
			elif theme == "синий":
				self.color = (0, 85, 213)
		elif self.type == 1:
			if theme == "чб":
				self.color1 = (138, 138, 138)
				self.color2 = (76, 76, 76)
			elif theme == "синий":
				self.color1 = ORANGE
				self.color2 = RED

	def draw(self, move):
		if move:
			self.y += self.v
		d = self.depth // 2
		if self.type ==  1:
			form1 = [(self.x-self.depth, self.y+self.depth), #квадрат
			(self.x+self.depth, self.y+self.depth), (self.x+self.depth, self.y-self.depth),
			(self.x-self.depth, self.y-self.depth)]
			form2 = [(self.x-d, self.y+self.depth), (self.x+d, self.y+self.depth), #крест
			(self.x+d, self.y+d), (self.x+self.depth, self.y+d),
			(self.x+self.depth, self.y-d),(self.x+d, self.y-d),
			(self.x+d, self.y-self.depth), (self.x-d, self.y-self.depth),
			(self.x-d, self.y-d), (self.x-self.depth, self.y-d),
			(self.x-self.depth, self.y+d), (self.x-d, self.y+d)]
			p.draw.polygon(self.surface, self.color1, form1)
			p.draw.polygon(self.surface, self.color2, form2)
		elif self.type == 2:
			text = self.f.render("m", 1, self.textColor)
			place = text.get_rect(center=(self.x,self.y))
			form = [(self.x - self.w, self.y - self.h), (self.x + self.w, self.y - self.h),
			(self.x + self.w, self.y + self.h), (self.x - self.w, self.y + self.h)]
			p.draw.polygon(self.surface, self.color, form)
			self.surface.blit(text, place)


class Boss1:
	def __init__(self, surf, theme, Width):
		self.deathTime = 0
		self.color2 = (0,0,0)
		self.color1 = (255,255,255)
		self.v = 1
		self.surface = surf
		self.hp = self.maxHp = 450
		self.depth = Width // 6
		self.y = -self.depth
		self.x = Width // 2
		if theme == "синий":
			self.hpColor = RED
		elif theme == "чб":
			self.hpColor = (130, 130, 130)

	def draw(self, move):
		if move:
			self.y += self.v
		h = self.depth * self.hp // self.maxHp
		form = [(self.x-self.depth, self.y+self.depth),
		(self.x+self.depth, self.y+self.depth),
		(self.x+self.depth, self.y-self.depth), (self.x-self.depth, self.y-self.depth)]
		form2 = [(self.x-self.depth+3, self.y+self.depth-3),
		(self.x+self.depth-3, self.y+self.depth-3),
		(self.x+self.depth-3, self.y-self.depth+3), (self.x-self.depth+3, self.y-self.depth+3)]
		hpForm = [(self.x-h, self.y+self.depth+4), (self.x+h, self.y+self.depth+4),
		(self.x+h, self.y+self.depth+3), (self.x-h, self.y+self.depth+3)]
		p.draw.polygon(self.surface, self.hpColor, hpForm)
		p.draw.polygon(self.surface, self.color1, form)
		p.draw.polygon(self.surface, self.color2, form2)


class Boss2:
	def __init__(self, surf, theme, Width):
		self.deathTime = 0
		self.v = 2
		self.surface = surf
		self.hp = self.maxHp = 1000
		self.width = Width // 7
		self.height = self.width // 2
		self.y = -self.height
		self.x = Width // 2
		self.recharge = 0
		if theme == "синий":
			self.hpColor = RED
			self.color = (10,80,230)
			self.color2 = (245,73,102)
		elif theme == "чб":
			self.hpColor = (130, 130, 130)
			self.color = (110,110,110)
			self.color2 = (140,140,140)
		self.d = self.width // 4
		self.x1 = self.x - self.d
		self.x2 = self.x + self.d
		self.y2 = self.y + self.d

	def draw(self, move):
		self.recharge += 1
		if self.recharge > 10:
			self.recharge = 0
		if move and self.y <= self.height:
			self.y += self.v
		self.y2 = self.y + self.d
		form = [(self.x-self.width, self.y-self.height), (self.x+self.width, self.y-self.height), (self.x, self.y+self.height)]
		form1 = [(self.x1-self.d, self.y2-self.d), (self.x1+self.d, self.y2-self.d), (self.x1, self.y2)]
		form2 = [(self.x2-self.d, self.y2-self.d), (self.x2+self.d, self.y2-self.d), (self.x2, self.y2)]
		p.draw.polygon(self.surface, self.color, form)
		p.draw.polygon(self.surface, self.color2, form1)
		p.draw.polygon(self.surface, self.color2, form2)
		h = self.height * self.hp // self.maxHp
		hpForm = [(self.x-h, self.y+self.height+4), (self.x+h, self.y+self.height+4),
		(self.x+h, self.y+self.height+3), (self.x-h, self.y+self.height+3)]
		p.draw.polygon(self.surface, self.hpColor, hpForm)


class Boss3:
	def __init__(self, surf, theme, Width):
		self.deathTime = 0
		self.v = 2
		self.surface = surf
		self.hp = self.maxHp = 1000
		self.width = Width // 7
		self.height = self.width // 2
		self.y = -self.height
		self.x = Width // 2
		self.recharge = 0
		self.d = self.width // 4
		if theme == "синий":
			self.hpColor = RED
			self.color = (10,80,230)
			self.color2 = (245,73,102)
		elif theme == "чб":
			self.hpColor = (130, 130, 130)
			self.color = (110,110,110)
			self.color2 = (140,140,140)

	def draw(self, move):
		self.recharge += 1
		if self.recharge > 10:
			self.recharge = 0
		if move and self.y <= self.height:
			self.y += self.v
		h = self.height * self.hp // self.maxHp
		form = [(self.x-self.width, self.y-self.height), (self.x+self.width, self.y-self.height), (self.x, self.y+self.height)]
		form2 = [(self.x-self.d, self.y), (self.x+self.d, self.y), (self.x, self.y+self.d)]
		hpForm = [(self.x-h, self.y+self.height+4), (self.x+h, self.y+self.height+4),
		(self.x+h, self.y+self.height+3), (self.x-h, self.y+self.height+3)]
		p.draw.polygon(self.surface, self.color, form)
		p.draw.polygon(self.surface, self.color2, form2)
		p.draw.polygon(self.surface, self.hpColor, hpForm)

''' я пытался
class Boss2(Boss3):
	def __init__(self, surf, theme, Width):
		Boss3.__init__(self, surf, theme, Width)
		self.recharge = 0
		self.d = self.width // 4
		self.x1 = self.x - self.d
		self.x2 = self.x + self.d
		self.y2 = self.y + self.d

	def draw(self, move):
		self.y2 = self.y + self.d
		form1 = [(self.x1-self.d, self.y2-self.d), (self.x1+self.d, self.y2-self.d), (self.x1, self.y2)]
		form2 = [(self.x2-self.d, self.y2-self.d), (self.x2+self.d, self.y2-self.d), (self.x2, self.y2)]
		p.draw.polygon(self.surface, self.color2, form1)
		p.draw.polygon(self.surface, self.color2, form2)
'''