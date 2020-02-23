import pygame as p
import sys, json
from random import randint as r
from classes import *
from screeninfo import get_monitors

p.mixer.init()
clock = p.time.Clock()
p.init()

RED = (226, 0, 0)
ORANGE = (255, 80, 80)
explosionSound = p.mixer.Sound("bam.ogg")
fileName = "data.json"
font = "pixelFont.otf"

bullets = []
enemies = []
sequins = []
bonuses = []
hsTable = False
turn = 0
gradation = "+" #изменение цвета фона
shade = 0
themes = ["синий", "чб"]
t = 0 #номер темы
fsc = False #полный экран
heal = 0
monitors = get_monitors()
while monitors == []:
	monitors = get_monitors()

keys = {p.K_a:"a", p.K_b:"b", p.K_c:"c", p.K_d: "d", p.K_e:"e", p.K_f:"f",
p.K_g:"g", p.K_h:"h", p.K_i:"i", p.K_j:"j", p.K_k:"k", p.K_l:"l", p.K_m:"m",
p.K_n:"n", p.K_o:"o", p.K_p:"p", p.K_q:"q", p.K_r:"r", p.K_s:"s", p.K_t:"t", 
p.K_u:"u", p.K_v:"v", p.K_w:"w", p.K_x:"x", p.K_y:"y", p.K_z:"z", p.K_0:"0",
p.K_1:"1", p.K_2:"2", p.K_3:"3", p.K_4: "4", p.K_5:"5", p.K_6:"6", p.K_7:"7",
p.K_8:"8", p.K_9:"9"}

def start(theme, fsc):
	if fsc:
		Width = monitors[0].width
		Height = monitors[0].height
		print(Height)
		sc = p.display.set_mode((Width, Height), p.FULLSCREEN)
	else:
		Width = 1200
		Height = 600
		sc = p.display.set_mode((Width, Height))
	pl = Player(sc, Width, Height, theme, fsc)
	if theme == "синий":
		buttonColor1 = (184, 105, 208)
		buttonColor2 = ORANGE
		tableColor = (7,88,139)
	elif theme == "чб":
		buttonColor1 = (165, 165, 165)
		buttonColor2 = (140, 140, 140)
		tableColor = (78, 78, 78)
	stButton = Button(Width//2, Height*4//10, Width//11, Height//15, sc, Width//25, buttonColor1) #play
	pButton = Button(Width//19, Height//20, Width//48, Height//40, sc, Width//50, buttonColor1) #points
	healButton = Button(Width//18, Height//9, Width//20, Height//40, sc, Width//50, buttonColor1)
	eButton = Button(Width//2, Height//2, Width//11, Height//12, sc, Width//15, buttonColor2) #конец
	tButton = Button(Width//2, Height*13//20, Width//15, Height//20, sc, Width//24, buttonColor1) #themes
	hsButton = Button(Width//12, Height//18, Width//15, Height//30, sc, Width//50, buttonColor1) #highscore (рекорд)
	fscButton = Button(Width//2, Height*17//20, Width//11, Height//20, sc, Width//50, buttonColor1)
	addPlButton = Button(Width//12, Height//7, Width//15, Height//30, sc, Width//50, buttonColor1)
	hsButtons = []
	for i in range(len(data["players"])):
		hsButtons.append(Button(Width//10, Height//7 + (i * Height//16), Width//12, Height//32, sc, Width//50, tableColor)) #таблица рекордов

	return sc, pl, Width, Height, stButton, pButton, eButton, tButton, hsButton, fscButton, hsButtons, addPlButton, healButton

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
			bullets.append(Bullet(pl.x, pl.y, sc, 0, 10, theme))
		elif pl.mode == 5:
			bullets.append(Bullet(pl.x, pl.y, sc, -1, 10, theme))
			bullets.append(Bullet(pl.x, pl.y, sc, 1, 10, theme))
		else:
			if pl.recharge == 3:
				if pl.mode == 0:
					bullets.append(Bullet(pl.x, pl.y, sc, 0, 10, theme))
				elif pl.mode == 1:
					bullets.append(Bullet(pl.x, pl.y, sc, -1, 10, theme))
					bullets.append(Bullet(pl.x, pl.y, sc, 0, 10, theme))
					bullets.append(Bullet(pl.x, pl.y, sc, 1, 10, theme))
				elif pl.mode == 3:
					bullets.append(Bullet(pl.x, pl.y, sc, 0, 4, theme))
				elif pl.mode == 4:
					bullets.append(Bullet(pl.x, pl.y, sc, -2, 10, theme))
					bullets.append(Bullet(pl.x, pl.y, sc, -1, 10, theme))
					bullets.append(Bullet(pl.x, pl.y, sc, 0, 10, theme))
					bullets.append(Bullet(pl.x, pl.y, sc, 1, 10, theme))
					bullets.append(Bullet(pl.x, pl.y, sc, 2, 10, theme))
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

	if len(bonuses) > 0:
		for i, b in enumerate(bonuses):
			if collision(b, pl):
				pl.heal += 1
				bonuses.pop(i)
				if pl.heal > 8:
					pl.heal = 8
			else:
				b.draw()

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
			if collision(e, pl):								#player.hp
				pl.hp -= e.depth
				enemies.pop(i)
				explosionSound.play()
			elif e.hp <= 0:										#points
				enemies.pop(i)
				explosionSound.play()
				pl.points += e.depth // 8
				if e.bonus == True:
					bonuses.append(Bonus(sc, e.x, e.y, theme))
				if pl.level == 1 and pl.points >= 50:
					pl.level = 2
					pl.mode = 1
					print("level 2")
				elif pl.level == 2 and pl.points >= 100:
					pl.level = 3
					pl.mode = 4
			elif e.y - e.depth > Height:
				enemies.pop(i)
				pl.hp -= e.depth
			else:
				e.draw()
	pButton.draw(str(pl.points))
	healButton.draw("аптечка "+str(pl.heal))
	pl.draw()

	return turn

def menu(hsTable):
	stButton.draw("играть")
	tButton.draw("тема")
	hsButton.draw("рекорд "+str(data["highscore"]))
	fscButton.draw("полный экран")
	if hsButton.pressure:
		if hsTable == False:
			hsTable = True
		else:
			hsTable = False
		hsButton.pressure = False
	if hsTable == True:
		for i, b in enumerate(hsButtons):
			b.draw(data["players"][i]["name"]+" "+str(data["players"][i]["points"]))
			if b.pressure:
				pl.name = data["players"][i]["name"]
				pl.highscore = data["players"][i]["points"]
	else:
		addPlButton.draw(pl.name+" "+str(pl.highscore))

	return hsTable

def events(hsTable):
	for event in p.event.get():
		if event.type == p.MOUSEBUTTONDOWN:
			buttons = []
			if stButton.pressure and eButton.pressure == False:
				if pl.hp <= 0:
					buttons = [eButton]
				else:
					buttons = [pButton]
			elif stButton.pressure == False:
				if hsTable:
					buttons = [stButton, tButton, fscButton, hsButton]
					buttons.extend(hsButtons)
				else:
					buttons = [stButton, tButton, fscButton, hsButton, addPlButton]
			for i in buttons:
				if i.pressure == False:
					pos = event.pos
					if event.button == 1:
						if (pos[0] >= i.x - i.w and pos[0] <= i.x + i.w and 
							pos[1] >= i.y - i.h and pos[1] <= i.y + i.h):
							i.pressure = True
		elif event.type == p.QUIT:
			quit(fileName)
		elif event.type == p.KEYDOWN:
			if stButton.pressure == False and addPlButton.pressure:
				if event.key == p.K_RETURN:
					addPlButton.pressure = False
				elif event.key == p.K_BACKSPACE:
					pl.name = pl.name[:len(pl.name)-1]
				elif event.key in keys and len(pl.name) < 12:
					if pl.name == "введите имя":
						pl.name = keys[event.key]
					else:
						pl.name += keys[event.key]
			elif event.key == p.K_h and pl.heal > 0:
				pl.hp += 20
				pl.heal -= 1
				if pl.hp > pl.maxHp:
					pl.hp = pl.maxHp
			elif event.key == p.K_ESCAPE:
				quit(fileName)
			elif event.key == p.K_LEFT:
				pl.motion = "left"
			elif event.key == p.K_RIGHT:
				pl.motion = "right"
			elif event.key == p.K_SPACE:
				pl.shot = True
			elif event.key == p.K_o:
				pl.level = 2
			elif event.key == p.K_m:
				pl.mode += 1
				if pl.level == 2:
					if pl.mode > 3:
						pl.mode = 1
				elif pl.level == 3:
					if pl.mode > 5:
						pl.mode = 4
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

def quit(fileName):
	pm = False
	for i in data["players"]:
		if pl.name == i["name"]:
			if pl.highscore > i["points"]:
				i["points"] = pl.highscore
			pm = True
	if pm == False and pl.name != "введите имя":
		data["players"].append({"name": pl.name, "points": pl.highscore})
	if pl.highscore > data["highscore"]:
		data["highscore"] = pl.highscore
	write(fileName, data)
	p.quit()
	sys.exit()

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
hsButtons = s[10]
addPlButton = s[11]
healButton = s[12]
while True:
	b = background(gradation, shade, themes[t])
	gradation = b[0]
	shade = b[1]

	events(hsTable)

	if stButton.pressure:
		if pl.hp <= 0:
			eButton.draw("конец")
			if eButton.pressure:
				stButton.pressure = False
				eButton.pressure = False
				ph = pl.highscore
				pn = pl.name
				print(pn, ph)
				pl.__init__(sc, Width, Height, themes[t], fsc)
				pl.highscore = ph
				pl.name = pn
				print(pl.name, pl.highscore)
				bullets = []
				enemies = []
		else:
			turn = play(turn, themes[t])
			if pl.points > pl.highscore:
				pl.highscore = pl.points
	else:
		hsTable = menu(hsTable)
		if tButton.pressure:
			t = themeSel(themes, t)
			ph = pl.highscore
			pn = pl.name
			s = start(themes[t], fsc)
			sc = s[0]
			pl = s[1]
			pl.highscore = ph
			pl.name = pn
			Width = s[2]
			Height = s[3]
			stButton = s[4]
			pButton = s[5]
			eButton = s[6]
			tButton = s[7]
			hsButton = s[8]
			fscButton = s[9]
			hsButtons = s[10]
			addPlButton = s[11]
			healButton = s[12]
		elif fscButton.pressure:
			if fsc == True:
				fsc = False
			else:
				fsc = True
			fscButton.pressure = False
			ph = pl.highscore
			pn = pl.name
			s = start(themes[t], fsc)
			sc = s[0]
			pl = s[1]
			pl.highscore = ph
			pl.name = pn
			Width = s[2]
			Height = s[3]
			stButton = s[4]
			pButton = s[5]
			eButton = s[6]
			tButton = s[7]
			hsButton = s[8]
			fscButton = s[9]
			hsButtons = s[10]
			addPlButton = s[11]
			healButton = s[12]

	#print(len(enemies) + len(sequins) + len(bullets) + 2)
	
			

	clock.tick(60)

	p.display.set_caption(str(clock))
	p.display.update()
	p.display.flip()