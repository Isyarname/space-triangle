import pygame as p
import sys, json
from random import randint as r
from classes import *
from screeninfo import get_monitors

RED = (226, 0, 0)
ORANGE = (255, 80, 80)
buttonColor = (184, 105, 208)
fileName = "data.json"

bullets = []
enemies = []
sequins = []
turn = 0
gradation = "+" #изменение цвета фона
shade = 0
themes = ["синий", "чб"]
t = 0 #номер темы
fsc = False #полный экран

clock = p.time.Clock()
p.init()

def start(theme, fsc):
	if fsc:
		m = get_monitors()
		while m == []:
			m = get_monitors()
		Width = m[0].width
		Height = m[0].height
		sc = p.display.set_mode((Width, Height), p.FULLSCREEN)
	else:
		Width = 1200
		Height = 600
		sc = p.display.set_mode((Width, Height))
	pl = Player(sc, Width, Height, theme)
	if theme == "синий":
		stButton = Button(Width//2, Height*45//100, Width//11, Height//15, sc, 60, buttonColor) #play
		pButton = Button(Width//25, Height//20, Width//48, Height//40, sc, 30, buttonColor) #points
		eButton = Button(Width//2, Height//2, Width//11, Height//12, sc, 80, ORANGE) #конец
		tButton = Button(Width//2, Height*65//100, Width//15, Height//20, sc, 50, buttonColor) #themes
		hsButton = Button(Width//10, Height//18, Width//12, Height//30, sc, 30, buttonColor) #highscore (рекорд)
		fscButton = Button(Width//2, Height*85//100, Width//11, Height//20, sc, 30, buttonColor)
	elif theme == "чб":
		stButton = Button(Width//2, Height*45//100, Width//11, Height//15, sc, 60, (165, 165, 165)) #play
		pButton = Button(Width//25, Height//20, Width//48, Height//40, sc, 30, (165, 165, 165)) #points
		eButton = Button(Width//2, Height//2, Width//11, Height//12, sc, 80, (140, 140, 140),) #конец
		tButton = Button(Width//2, Height*65//100, Width//15, Height//20, sc, 50, (165, 165, 165)) #themes
		hsButton = Button(Width//10, Height//18, Width//12, Height//30, sc, 30, (165, 165, 165)) #highscore (рекорд)
		fscButton = Button(Width//2, Height*85//100, Width//11, Height//20, sc, 30, (165, 165, 165))

	return sc, pl, Width, Height, stButton, pButton, eButton, tButton, hsButton, fscButton

def themeSel(themes, t):
	t += 1
	tButton.pressure = False
	if t >= len(themes):
		t = 0

	return t

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

def shooting(theme):
	if pl.shot == True:
		if pl.mode == 2:
			bullets.append(Bullet(pl.x, pl.y, sc, "forward", 10, theme))
		else:
			if pl.recharge == 3:
				if pl.mode == 0:
					bullets.append(Bullet(pl.x, pl.y, sc, "forward", 10, theme))
				elif pl.mode == 1:
					bullets.append(Bullet(pl.x, pl.y, sc, "left", 10, theme))
					bullets.append(Bullet(pl.x, pl.y, sc, "forward", 10, theme))
					bullets.append(Bullet(pl.x, pl.y, sc, "right", 10, theme))
				elif pl.mode == 3:
					bullets.append(Bullet(pl.x, pl.y, sc, "forward", 4, theme))
				pl.recharge = 0
			else:
				pl.recharge += 1

	if len(bullets) > 0:
		for index, bullet in enumerate(bullets):
			if bullet.y + bullet.lenght <= 0:
				bullets.pop(index)
			else:
				  bullet.draw()

def play(turn, theme):
	shooting(theme)

	turn += 1
	if turn > r(100,600):
		enemies.append(Enemy(sc, pl.points//25, theme, Width))
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
	pButton.draw(str(pl.points))
	pl.draw()

	return turn

def menu():
	stButton.draw("играть")
	tButton.draw("тема")
	hsButton.draw("рекорд "+str(data["highscore"]))
	fscButton.draw("полный экран")

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
				buttons = [stButton, tButton, fscButton]
			for i in buttons:
				if i.pressure == False:
					pos = event.pos
					if event.button == 1:
						if (pos[0] >= i.x - i.w and pos[0] <= i.x + i.w and 
							pos[1] >= i.y - i.h and pos[1] <= i.y + i.h):
							i.pressure = True
		elif event.type == p.QUIT:
			write(fileName, data)
			p.quit()
			sys.exit()
		elif event.type == p.KEYDOWN:
			if event.key == p.K_ESCAPE:
				write(fileName, data)
				p.quit()
				sys.exit()
			elif event.key == p.K_LEFT:
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

def background(gradation, shade, theme):
	if r(0,15) == 1:
		if gradation == "+":
			shade += 1
			if shade >= 30:
				gradation = "-"
		elif gradation == "-":
			shade -= 1
			if shade <= 0:
				gradation = "+"
	if theme == "синий":
		sc.fill((30 - shade, shade, 40))
	elif theme == "чб":
		sc.fill((shade, shade, shade))

	sequins.append(Sequin(sc, pl.points//25, themes[t], Width))
	for i, s in enumerate(sequins):
		if s.y > Height:
			sequins.pop(i)
		else:
			s.draw()

	return gradation, shade

data = read(fileName)
s = start(themes[t], fsc)
sc = s[0]
pl = s[1]
Width = s[2]
Height = s[3]
stButton = s[4]
pButton = s[5]
eButton = s[6]
tButton = s[7]
hsButton = s[8]
fscButton = s[9]
while True:
	b = background(gradation, shade, themes[t])
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
				bullets = []
				enemies = []
		else:
			turn = play(turn, themes[t])
			if pl.points > data["highscore"]:
				data["highscore"] = pl.points
	else:
		menu()
		if tButton.pressure:
			t = themeSel(themes, t)
			s = start(themes[t], fsc)
			sc = s[0]
			pl = s[1]
			Width = s[2]
			Height = s[3]
			stButton = s[4]
			pButton = s[5]
			eButton = s[6]
			tButton = s[7]
			hsButton = s[8]
			fscButton = s[9]
		elif fscButton.pressure:
			if fsc == True:
				fsc = False
			else:
				fsc = True
			fscButton.pressure = False
			s = start(themes[t], fsc)
			sc = s[0]
			pl = s[1]
			Width = s[2]
			Height = s[3]
			stButton = s[4]
			pButton = s[5]
			eButton = s[6]
			tButton = s[7]
			hsButton = s[8]
			fscButton = s[9]

	#print(len(enemies) + len(sequins) + len(bullets) + 2)
	
			

	clock.tick(60)

	p.display.set_caption(str(clock))
	p.display.update()
	p.display.flip()