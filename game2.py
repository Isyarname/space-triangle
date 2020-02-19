import pygame as p
import sys, json
from random import randint as r
from classes import *

RED = (226, 0, 0)
ORANGE = (255, 80, 80)
buttonColor = (184, 105, 208)
Width = 1200
Height = 600
pF = "pixelFont.otf"

clock = p.time.Clock()
p.init()
sc = p.display.set_mode((Width, Height))
pl = Player(sc)

stButton = Button(Width//2, Height//2, 110, 40, sc, pF, 60, buttonColor, (40,41,35)) #start
pButton = Button(Width//25, Height//20, 25, 15, sc, pF, 30, buttonColor, (40,60,40)) #points
eButton = Button(Width//2, Height//2, 110, 50, sc, pF, 80, ORANGE, (0,0,0)) #конец
tButton = Button(Width//2, Height*65//100, 80, 30, sc, pF, 50, buttonColor, (40,41,35)) #themes
hsButton = Button(Width//10, Height//18, 100, 20, sc, pF, 30, buttonColor, (40,60,40)) #highscore
bullets = []
enemies = []
sequins = []
turn = 0
gradation = "+" #изменение цвета фона
shade = 0
themes = ["синий", "чб"]
t = 0
fileName = "data.json"

def read(fileName):
	with open(fileName, "r", encoding = "UTF-8") as file:
		return json.load(file)

def write(fileName, data):
	with open(fileName, "w", encoding = "UTF-8") as file:
		json.dump(data, file)

def collision(object1, object2): #enemy, bullet/player
	if (object2.y - object2.depth < object1.y + object1.depth and
		object2.y + object2.depth > object1.y - object2.depth and 
		object1.x - object1.depth < object2.x + object2.depth and
		object1.x + object1.depth > object2.x - object2.depth):
		return True
	else:
		return False

def shooting(themes, t):
	if pl.shot == True:
		if pl.mode == 2:
			bullets.append(Bullet(pl.x, pl.y, sc, "forward", 10, themes[t]))
		else:
			if pl.recharge == 3:
				if pl.mode == 0:
					bullets.append(Bullet(pl.x, pl.y, sc, "forward", 10, themes[t]))
				elif pl.mode == 1:
					bullets.append(Bullet(pl.x, pl.y, sc, "left", 10, themes[t]))
					bullets.append(Bullet(pl.x, pl.y, sc, "forward", 10, themes[t]))
					bullets.append(Bullet(pl.x, pl.y, sc, "right", 10, themes[t]))
				elif pl.mode == 3:
					bullets.append(Bullet(pl.x, pl.y, sc, "forward", 4, themes[t]))
				pl.recharge = 0
			else:
				pl.recharge += 1

	if len(bullets) > 0:
		for index, bullet in enumerate(bullets):
			if bullet.y + bullet.lenght <= 0:
				bullets.pop(index)
			else:
				  bullet.draw()

def play(turn, themes, t, data, fileName):
	shooting(themes, t)

	turn += 1
	if turn > r(100,600):
		enemies.append(Enemy(sc, pl.points//25, themes[t]))
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
			elif e.hp <= 0:												#points
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

	if pl.points > data["highscore"]:
		data["highscore"] = pl.points
		write(fileName, data)

	pButton.draw(str(pl.points))
	pl.draw()

	return turn, data

def menu(themes, t):
	stButton.draw("играть")
	tButton.draw("тема")
	hsButton.draw("highscore "+str(data["highscore"]))
	t = themeSel(themes, t)

	return t

def events():
	for event in p.event.get():
		if event.type == p.MOUSEBUTTONDOWN:
			buttons = []
			if stButton.pressure and eButton.pressure == False:
				if pl.hp <= 0:
					buttons = [eButton]
				else:
					buttons = [pButton]
			elif stButton.pressure == False:
				buttons = [stButton, tButton]
			for i in buttons:
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

def background(gradation, shade, themes, t):
	if r(0,15) == 1:
		if gradation == "+":
			shade += 1
			if shade >= 30:
				gradation = "-"
		elif gradation == "-":
			shade -= 1
			if shade <= 0:
				gradation = "+"
	if themes[t] == "синий":
		sc.fill((30 - shade, shade, 40))
	elif themes[t] == "чб":
		sc.fill((shade, shade, shade))

	sequins.append(Sequin(sc, pl.points//25, themes[t]))
	for i, s in enumerate(sequins):
		if s.y > Height:
			sequins.pop(i)
		else:
			s.draw()

	return gradation, shade

def themeSel(themes, t):
	if tButton.pressure:
		t += 1
		tButton.pressure = False
		if t >= len(themes):
			t = 0
			print(themes[t], tButton.pressure)
			
	if themes[t] == "синий":
		hsButton.color = tButton.color = pButton.color = stButton.color = buttonColor
		tButton.textColor = stButton.textColor = (40, 41, 35)
		hsButton.textColor = pButton.textColor = (40, 60, 40)
		eButton.color = ORANGE
		pl.color = (100, 255, 255)
	elif themes[t] == "чб":
		hsButton.color = tButton.color = pButton.color = stButton.color = (165, 165, 165)
		tButton.textColor = stButton.textColor = (39, 39, 39)
		hsButton.textColor = pButton.textColor = (47, 47, 47)
		eButton.color = (140, 140, 140)
		pl.color = (203, 203, 203)

	return t

data = read(fileName)
while True:
	b = background(gradation, shade, themes, t)
	gradation = b[0]
	shade = b[1]

	events()

	if stButton.pressure:
		if pl.hp <= 0:
			eButton.draw("конец")
			if eButton.pressure:
				stButton.pressure = False
				eButton.pressure = False
				pl.__init__(sc)
		else:
			pla = play(turn, themes, t, data, fileName)
			turn = pla[0]
			data =pla[1]
	else:
		t = menu(themes, t)

	#print(len(enemies) + len(sequins) + len(bullets) + 2)
	
			

	clock.tick(60)

	p.display.set_caption(str(clock))
	p.display.update()
	p.display.flip()