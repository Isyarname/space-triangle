import pygame as p
import sys, json
from math import *
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
hsTable = False #открыта ли таблица рекордов
bossIndex = 0
bossA = False
turn = 0
gradation = "+" #изменение цвета фона
shade = 0
themes = ["синий", "чб"]
t = 0 #номер темы
fsc = False #полный экран
monitors = get_monitors()
while monitors == []: #так работает
	monitors = get_monitors()

keys = {p.K_a:"a", p.K_b:"b", p.K_c:"c", p.K_d: "d", p.K_e:"e", p.K_f:"f",
p.K_g:"g", p.K_h:"h", p.K_i:"i", p.K_j:"j", p.K_k:"k", p.K_l:"l", p.K_m:"m",
p.K_n:"n", p.K_o:"o", p.K_p:"p", p.K_q:"q", p.K_r:"r", p.K_s:"s", p.K_t:"t", 
p.K_u:"u", p.K_v:"v", p.K_w:"w", p.K_x:"x", p.K_y:"y", p.K_z:"z", p.K_0:"0",
p.K_1:"1", p.K_2:"2", p.K_3:"3", p.K_4: "4", p.K_5:"5", p.K_6:"6", p.K_7:"7",
p.K_8:"8", p.K_9:"9", p.K_SPACE:" "}

def start(theme, fsc):
	if fsc:
		Width = monitors[0].width
		Height = monitors[0].height
		print(Height)
		sc = p.display.set_mode((Width, Height), p.FULLSCREEN)
	else:
		Width = 900
		Height = 500
		sc = p.display.set_mode((Width, Height))
	if theme == "синий":
		buttonColor1 = (184, 105, 208)
		buttonColor2 = ORANGE
		tableColor = (7,88,139)
	elif theme == "чб":
		buttonColor1 = (165, 165, 165)
		buttonColor2 = (140, 140, 140)
		tableColor = (78, 78, 78)
	stButton = Button(Width//2, Height*4//10, sc, Width//25, buttonColor1) #play
	pButton = Button(Width//29, Height//20, sc, Width//50, buttonColor1) #points
	pauseButton = Button(Width*28//29, Height//20, sc, Width//50, buttonColor1)
	eButton = Button(Width//2, Height//2, sc, Width//15, buttonColor2) #конец
	tButton = Button(Width//2, Height*13//20, sc, Width//24, buttonColor1) #themes
	hsButton = Button(Width//10, Height//18, sc, Width//50, buttonColor1) #highscore (рекорд)
	fscButton = Button(Width//2, Height*17//20, sc, Width//40, buttonColor1)
	plButton = Button(Width//10, Height//7, sc, Width//50, buttonColor1)
	boss = Boss1(sc, theme, Width)
	pl = Player(sc, Width, Height, theme, fsc)
	hsButtons = []
	for i in range(len(data["players"])):
		hsButtons.append(Button(Width//10, Height//7 + (i * Height//16), sc, Width//50, tableColor)) #таблица рекордов

	return (sc, pl, Width, Height, stButton, pButton, eButton, tButton,
	hsButton,fscButton, hsButtons, plButton, pauseButton, boss)

def themeChoice(themes, t, sc):
	t += 1
	tButton.pressure = False
	if t >= len(themes):
		t = 0
	if themes[t] == "синий":
		buttonColor1 = (184, 105, 208)
		buttonColor2 = ORANGE
		tableColor = (7,88,139)
	elif themes[t] == "чб":
		buttonColor1 = (165, 165, 165)
		buttonColor2 = (140, 140, 140)
		tableColor = (78, 78, 78)
	boss = Boss1(sc, themes[t], Width)
	ph, pn = pl.highscore, pl.name
	pl.__init__(sc, Width, Height, themes[t], fsc)
	pl.highscore, pl.name = ph, pn
	stButton.color = pButton.color = pauseButton.color = buttonColor1
	tButton.color = hsButton.color = fscButton.color = plButton.color = buttonColor1
	eButton.color = buttonColor2
	for i in hsButtons:
		i.color = tableColor

	return t, boss

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

def tCollision(obj1, obj2): #столкновение с треугольным боссом
	if (obj1.x - obj1.width <= obj2.x <= obj1.x and 
		(obj1.y + obj1.height - obj2.y) * (obj1.width / 2) / obj1.height > obj1.x - obj2.x or 
		obj1.x <= obj2.x <= obj1.x + obj1.width and 
		(obj1.y + obj1.height - obj2.y) * (obj1.width / 2) / obj1.height > obj2.x - obj1.x):
		return True
	else:
		return False

def ai(x, y, a, b, v):
	dx = x - a
	dy = y - b
	ra = sqrt(dx * dx + dy * dy)
	n = 99
	vxb = 0
	vyb = 0
	vx = dx * v / ra
	vy = dy * v / ra

	return vx, vy

def shooting(theme, move):
	for j, b in enumerate(bullets):
		if b.type == 2:
			if collision(pl, b):
				pl.hp -= b.depth
				bullets.pop(j)
		elif len(enemies) > 0:
			for i, e in enumerate(enemies):
				if collision(e, b):
					e.hp -= b.depth
					bullets.pop(j)
		
	if move and pl.shot == True:
		y = pl.y - pl.depth
		if pl.mode == 3: #часто в одну колонну
			bullets.append(Bullet(pl.x, y, sc, 0, 10, theme, 1))
		elif pl.mode == 6: #часто в 2 колонны
			bullets.append(Bullet(pl.x, y, sc, -1, 10, theme, 1))
			bullets.append(Bullet(pl.x, y, sc, 1, 10, theme, 1))
		elif pl.mode == 7: #часто в 3 колонны
			bullets.append(Bullet(pl.x, y, sc, -1, 10, theme, 1))
			bullets.append(Bullet(pl.x, y, sc, 0, 10, theme, 1))
			bullets.append(Bullet(pl.x, y, sc, 1, 10, theme, 1))
		elif pl.recharge == 3:
			if pl.mode == 1: #редко в оду колонну
				bullets.append(Bullet(pl.x, y, sc, 0, 10, theme, 1))
			elif pl.mode == 2: #редко в 3 колонны
				bullets.append(Bullet(pl.x, y, sc, -1, 10, theme, 1))
				bullets.append(Bullet(pl.x, y, sc, 0, 10, theme, 1))
				bullets.append(Bullet(pl.x, y, sc, 1, 10, theme, 1))
			elif pl.mode == 4: #редко в 1 колонну, но пули большие и медленые
				bullets.append(Bullet(pl.x, y, sc, 0, 4, theme, 1))
			elif pl.mode == 5: #редко в 5 колонн
				bullets.append(Bullet(pl.x, y, sc, -2, 10, theme, 1))
				bullets.append(Bullet(pl.x, y, sc, -1, 10, theme, 1))
				bullets.append(Bullet(pl.x, y, sc, 0, 10, theme, 1))
				bullets.append(Bullet(pl.x, y, sc, 1, 10, theme, 1))
				bullets.append(Bullet(pl.x, y, sc, 2, 10, theme, 1))
			pl.recharge = 0
		else:
			pl.recharge += 1

	if len(bullets) > 0:
		for index, bullet in enumerate(bullets):
			if bullet.y + bullet.lenght <= 0 or bullet.y - bullet.lenght > Height:
				bullets.pop(index)
			else:
				  bullet.draw(move)

def enemyMovement(theme, move, bossIndex):
	if len(enemies) > 0:
		for i, e in enumerate(enemies):
			'''for j, b in enumerate(bullets):
				if b.type == 1 and collision(e, b):
					e.hp -= b.depth
					bullets.pop(j)'''
			if collision(e, pl):								#player.hp
				pl.hp -= e.depth * 2
				enemies.pop(i)
				explosionSound.play()
			elif e.hp <= 0:										#points
				enemies.pop(i)
				explosionSound.play()
				pl.points += e.depth // 8
				'''if pl.points > pl.highscore:
					pl.highscore = pl.points'''
				if e.bonus:
					bonuses.append(Bonus(sc, e.x, e.y, theme, pl.level, pl.points, "random", bossIndex))
				if bossIndex == 3 and e.y < Height // 2:
					boss.hp -= e.depth * 2
			elif e.y - e.depth > Height:
				enemies.pop(i)
				pl.hp -= e.depth * 2
			else:
				e.draw(move)

def bossMovement(move, theme, bossIndex, bossA):
	if bossA == True:
		if boss.hp > 0:
			if move:
				if bossIndex == 2:
					for j, b in enumerate(bullets):
						if b.type == 1 and tCollision(boss, b):
							boss.hp -= b.depth
							bullets.pop(j)
					if tCollision(boss, pl):
						pl.hp -= boss.hp
					if boss.recharge == 10:
						if r(1,2) == 1:
							a = boss.x1
						else:
							a = boss.x2
						vmax = 6
						vai = ai(pl.x, pl.y, a, boss.y2, vmax)
						vx, vy = vai[0], vai[1]
						bullets.append(Bullet(a, boss.y2, sc, vx, vy, theme, 2))
				elif bossIndex == 3: #Boss3.hp в enemyMovement()
					if tCollision(boss, pl):
						pl.hp -= boss.hp
					if boss.recharge == 10:
						vmax = 6
						b = boss.y + boss.d
						vai = ai(pl.x, pl.y, boss.x, b, vmax)
						vx, vy = vai[0], vai[1]
						bullets.append(Bullet(boss.x, b, sc, vx, vy, theme, 2))
				elif bossIndex == 1:
					if collision(boss, pl) or boss.y - boss.depth >= Height:
						pl.hp -= boss.hp
						boss.hp = 0
						explosionSound.play()
					for j, b in enumerate(bullets):
						if b.type == 1 and collision(boss, b):
							print("collision")
							boss.hp -= b.depth
							bullets.pop(j)
			boss.draw(move)
		else:
			bonuses.append(Bonus(sc, boss.x, boss.y, theme, pl.level, pl.points, 1))
			bonuses.append(Bonus(sc, boss.x+20, boss.y, theme, pl.level, pl.points, 2))
			pl.points += 50
			boss.deathTime = pl.time
			bossA = False

	return bossA

def play(turn, theme, move, bossIndex, bossA):
	if len(bonuses) > 0:
		for i, b in enumerate(bonuses):
			if collision(b, pl):
				if b.type == 1:
					pl.hp += 20
					if pl.hp > pl.maxHp:
						pl.hp = pl.maxHp
				else:
					pl.level += 1
				bonuses.pop(i)
			else:
				b.draw(move)

	if move:
		turn += 1
		if turn > r(100,600):
			turn = 0
			enemies.append(Enemy(sc, pl.points//50, theme, Width))

	bossA = bossMovement(move, theme, bossIndex, bossA)
	enemyMovement(theme, move, bossIndex)
	shooting(theme, move)
	pButton.draw(str(pl.points), Width)
	pl.draw(move)
	pauseButton.draw("||", Width)

	return turn, bossA

def menu(hsTable):
	stButton.draw("играть", Width)
	tButton.draw("тема", Width)
	if hsTable:
		hsButton.draw("^ рекорд "+str(data["highscore"]), Width)
	else:
		hsButton.draw("v рекорд "+str(data["highscore"]), Width)
	fscButton.draw("полный экран", Width)
	if hsButton.pressure:
		if not hsTable:
			hsTable = True
		else:
			hsTable = False
		hsButton.pressure = False
	if hsTable:
		for i, b in enumerate(hsButtons):
			b.draw(data["players"][i]["name"]+" "+str(data["players"][i]["points"]), Width)
			if b.pressure:
				pl.name = data["players"][i]["name"]
				pl.highscore = data["players"][i]["points"]
	else:
		plButton.draw(pl.name+" "+str(pl.highscore), Width)

	return hsTable

def events(hsTable):
	for event in p.event.get():
		if event.type == p.MOUSEBUTTONDOWN:
			buttons = []
			if stButton.pressure and not eButton.pressure:
				if pl.hp <= 0:
					buttons = [eButton]
				else:
					buttons = [pButton, pauseButton]
			elif not stButton.pressure:
				if hsTable:
					buttons = [stButton, tButton, fscButton, hsButton]
					buttons.extend(hsButtons)
				else:
					buttons = [stButton, tButton, fscButton, hsButton, plButton]
			for i in buttons:
				pos = event.pos
				if event.button == 1:
					if (pos[0] >= i.x - i.w and pos[0] <= i.x + i.w and 
						pos[1] >= i.y - i.h and pos[1] <= i.y + i.h):
						i.pressure = not i.pressure
		elif event.type == p.QUIT:
			quit(fileName)
		elif event.type == p.KEYDOWN:
			if not stButton.pressure and plButton.pressure:
				if event.key == p.K_BACKSPACE:
					pl.name = pl.name[:-1]
				elif event.key in keys:
					if len(pl.name) < 12:
						if pl.name == "введите имя":
							pl.name = keys[event.key]
						else:
							pl.name += keys[event.key]
				else:
					addPlButton.pressure = False
			elif event.key == p.K_ESCAPE:
				quit(fileName)
			elif event.key in [p.K_DOWN, p.K_UP, p.K_LEFT, p.K_RIGHT]:
				pl.motion.append(event.key)
				if event.key == p.K_DOWN:
					key = p.K_UP
				elif event.key == p.K_UP:
					key = p.K_DOWN
				elif event.key == p.K_LEFT:
					key = p.K_RIGHT
				elif event.key == p.K_RIGHT:
					key = p.K_LEFT
				for i, k in enumerate(pl.motion):
					if key == k:
						pl.motion.pop(i)
			elif event.key == p.K_SPACE:
				pl.shot = True
			elif event.key == p.K_e:
				pl.shot = not pl.shot
			elif event.key == p.K_RETURN:
				stButton.pressure = True
			elif event.key == p.K_p and stButton.pressure:
				pauseButton.pressure = not pauseButton.pressure
			elif event.key == p.K_o:
				pl.level = 2
			elif event.key == p.K_l:
				pl.time = 3500 * 2 - 1
			elif event.key == p.K_m and pl.level > 1:
				pl.mode += 1
				print("mode =", pl.mode)
				print("level =", pl.level)
				if (pl.level == 2 and pl.mode > 4 or
				pl.level == 3 and pl.mode > 6 or
				pl.level == 4 and pl.mode > 7):
					pl.mode = pl.level
					print("pl.mode = pl.level =", pl.level)
		elif event.type == p.KEYUP:
			if event.key == p.K_SPACE:
				pl.shot = False
			else:
				for i, k in enumerate(pl.motion):
					if event.key == k:
						pl.motion.pop(i)

def background(gradation, shade, theme, move):
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
	if move:
		sequins.append(Sequin(sc, pl.points//25, themes[t], Width))
	for i, s in enumerate(sequins):
		if s.y > Height:
			sequins.pop(i)
		else:
			s.draw(move)

	return gradation, shade

def quit(fileName):
	pm = False
	for i in data["players"]:
		if pl.name == i["name"]:
			if pl.highscore > i["points"]:
				i["points"] = pl.highscore
			pm = True
	if pm == False and pl.name != ("введите имя" or ""):
		data["players"].append({"name": pl.name, "points": pl.highscore})
	if pl.highscore > data["highscore"]:
		data["highscore"] = pl.highscore
	write(fileName, data)
	p.quit()
	sys.exit()

data = read(fileName)
s = start(themes[t], fsc)
sc, pl, Width, Height, stButton, pButton = s[0], s[1], s[2], s[3], s[4], s[5]
eButton, tButton, hsButton, fscButton = s[6], s[7], s[8], s[9]
hsButtons, plButton, pauseButton, boss = s[10], s[11], s[12], s[13]
while True:
	b = background(gradation, shade, themes[t], not pauseButton.pressure)
	gradation = b[0]
	shade = b[1]

	events(hsTable)

	if stButton.pressure:
		if pl.hp <= 0:
			eButton.draw("конец", Width)
			if eButton.pressure:
				eButton.pressure = False
				stButton.pressure = False
				pauseButton.pressure = False
				bossA = False
				if pl.points > pl.highscore:
					pl.highscore = pl.points
				ph, pn = pl.highscore, pl.name
				pl.__init__(sc, Width, Height, themes[t], fsc)
				pl.highscore, pl.name = ph, pn
				boss = Boss1(sc, themes[t], Width)
				bossIndex = 0
				bullets = []
				enemies = []
		else:
			if not pauseButton.pressure:
				pl.time += 1
			if (bossA == False and (pl.time - boss.deathTime) % 3500 == 0 and bossIndex < 3):
				bossIndex += (pl.time - boss.deathTime) // 3500
				print("bossIndex=", bossIndex)
				bossA = True
				if bossIndex == 2:
					print("boss2")
					boss = Boss2(sc, themes[t], Width)
				elif bossIndex == 3:
					print("boss 3")
					boss = Boss3(sc, themes[t], Width)
			pla = play(turn, themes[t], not pauseButton.pressure, bossIndex, bossA)
			turn, bossA = pla[0], pla[1]
	else:
		hsTable = menu(hsTable)
		if tButton.pressure:
			tc = themeChoice(themes, t, sc)
			t, boss = tc[0], tc[1]
		elif fscButton.pressure:
			fsc = not fsc
			fscButton.pressure = False
			ph, pn = pl.highscore, pl.name
			s = start(themes[t], fsc)
			sc, pl, Width, Height, stButton, pButton = s[0], s[1], s[2], s[3], s[4], s[5]
			eButton, tButton, hsButton, fscButton = s[6], s[7], s[8], s[9]
			hsButtons, plButton, pauseButton, boss = s[10], s[11], s[12], s[13]
			pl.highscore, pl.name = ph, pn


	#print(len(enemies) + len(sequins) + len(bullets) + 2)
			

	clock.tick(60)

	p.display.set_caption(str(clock))
	p.display.update()
	p.display.flip()