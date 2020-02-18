import pygame as p
import sys
from random import randint as r
from classes import *

RED = (226,0,0)
ORANGE = (255,80,80)
buttonColor = (184,105,208)
Width = 1200
Height = 600
pF = "pixelFont.otf"

clock = p.time.Clock()
p.init()
sc = p.display.set_mode((Width, Height))
pl = Player(sc)

stButton = Button(Width//2, Height//2, 110, 40, sc, pF, 60, buttonColor, (40,41,35))
pButton = Button(Width//25, Height//20, 25, 15, sc, pF, 30, buttonColor, (40,60,40))
eButton = Button(Width//2, Height//2, 110, 50, sc, pF, 80, ORANGE, (0,0,0))
bullets = []
enemies = []
sequins = []
recharge = 0
turn = 0
gradation = True #изменение цвета фона
green = 0 #зелёный фона

def collision(object1, object2): #enemy, bullet/player
	if (object2.y - object2.depth < object1.y + object1.depth and
		object2.y + object2.depth > object1.y - object2.depth and 
		object1.x - object1.depth < object2.x + object2.depth and
		object1.x + object1.depth > object2.x - object2.depth):
		return True
	else:
		return False

def shooting(recharge):
	if pl.shot == True:
		if pl.mode == 2:
			bullets.append(Bullet(pl.x, pl.y, sc, "forward", 10))
		else:
			if recharge == 3:
				if pl.mode == 0:
					bullets.append(Bullet(pl.x, pl.y, sc, "forward", 10))
				elif pl.mode == 1:
					bullets.append(Bullet(pl.x, pl.y, sc, "left", 10))
					bullets.append(Bullet(pl.x, pl.y, sc, "forward", 10))
					bullets.append(Bullet(pl.x, pl.y, sc, "right", 10))
				elif pl.mode == 3:
					bullets.append(Bullet(pl.x, pl.y, sc, "forward", 4))
				recharge = 0
			else:
				recharge += 1

	if len(bullets) > 0:
		for index, bullet in enumerate(bullets):
			if bullet.y + bullet.lenght <= 0:
				bullets.pop(index)
			else:
				  bullet.draw()

	return recharge

def play(recharge, turn):
	recharge = shooting(recharge)

	turn += 1
	if turn > r(100,600):
		enemies.append(Enemy(sc, pl.points//20))
		turn = 0

	if len(enemies) > 0:
		for i, e in enumerate(enemies):
			for j, b in enumerate(bullets):
				if collision(e, b):
					e.hp -= b.depth * 2
					bullets.pop(j)
			if collision(e, pl):										#player.hp
				pl.hp -= e.depth
				enemies.pop(i)
			if e.hp <= 0:												#points
				enemies.pop(i)
				pl.points += e.depth // 8
				if e.bonus == True:
					pl.hp += e.depth
					if pl.hp > pl.maxHp:
						pl.hp = pl.maxHp
				if pl.points >= 50:
					if pl.level == 1:
						pl.level = 2
						pl.mode = 1
						print("level 2")
			elif e.y - e.depth > Height:
				enemies.pop(i)
				pl.hp -= e.depth
			else:
				e.draw()
	pl.draw()

	return recharge, turn

def menu():
	stButton.draw("играть")

def events():
	for event in p.event.get():
		if event.type == p.MOUSEBUTTONDOWN:
			if stButton.pressure and pl.hp <= 0 and eButton.pressure == False:
				i = eButton
			else:
				i = stButton
			if i.pressure == False:
				pos = event.pos
				if event.button == 1:
					if (pos[0] >= i.x - i.w and pos[0] <= i.x + i.w and 
						pos[1] >= i.y - i.h and pos[1] <= i.y + i.h):
						i.pressure = True
		elif event.type == p.QUIT:
			p.quit()
			sys.exit()
		elif event.type == p.KEYDOWN:
			if event.key == p.K_LEFT:
				pl.motion = "left"
			elif event.key == p.K_RIGHT:
				pl.motion = "right"
			elif event.key == p.K_SPACE:
				pl.shot = True
			elif event.key == p.K_o:
				pl.level = 2
			elif event.key == p.K_m:
				if pl.level == 2:
					if pl.mode == 1:
						pl.mode = 2
					elif pl.mode == 2:
						pl.mode = 3
					else:
						pl.mode = 1
		elif event.type == p.KEYUP:
			if event.key in [p.K_LEFT, p.K_RIGHT]:
				pl.motion = "stop"
			if event.key == p.K_SPACE:
				pl.shot = False

def background(gradation, green):
	if gradation == True:
		if r(1,5) == 1:
			green += r(0,1)
		if green >= 40:
			gradation = False
	else:
		if r(0,5) == 1:
			green -= r(0,1)
		if green <= 0:
			gradation = True
	blue = 40 - green
	sc.fill((blue//4, green, blue))

	sequins.append(Sequin(sc, pl.points//10))
	for i, s in enumerate(sequins):
		if s.y > Height:
			sequins.pop(i)
		else:
			s.draw()

	return gradation, green


while True:
	b = background(gradation, green)
	gradation = b[0]
	green = b[1]

	events()

	if stButton.pressure:
		if pl.hp <= 0:
			eButton.draw("конец")
			if eButton.pressure:
				stButton.pressure = False
				eButton.pressure = False
				pl.hp = pl.maxHp
				pl.points = 0
		else:
			t = play(recharge, turn)
			recharge = t[0]
			turn = t[1]
		pButton.draw(str(pl.points))

	else:
		menu()

	#print(len(enemies) + len(sequins) + len(bullets) + 2)
	
			

	clock.tick(60)

	p.display.set_caption(str(clock))
	p.display.update()
	p.display.flip()