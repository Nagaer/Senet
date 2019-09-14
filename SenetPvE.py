import pygame as pg
import sys, random, os, time

FPS = 10
Window_WIDTH = 1500
Window_HEIGHT = 664
YELLOW = [255, 176, 46]
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
RED = [227, 38, 54]
BLUE = [21, 96, 189]
Line_WIDTH_1 = 10
Line_WIDTH_2 = 5
Indent_X = 0.2 #Отступ по X
Indent_Y = 0.25 #Отступ по Y
Cell_X = Window_WIDTH*(1-Indent_X*2)/10
Cell_Y = Window_HEIGHT*(1-Indent_Y)/3
COLOR = [YELLOW, RED, BLUE]

class Player:
    def __init__(self, chips, color):
        self.chips = chips #Здесь хранятся позиции фишек от 0 до 29. Победа присуждается тому, кто первый получил все фишки -1
        self.color = color
        
    def move(self, Enemy, points): #Enemy - противоположный игрок, points - результат дайса
        if points == 1 or points == 4 or points == 5:
            ExTurn = True
        else:
            ExTurn = False
        if self.color == BLUE:
            Chip_List = [len(self.chips) + 1 - i for i in range(1, len(self.chips) + 1)]
        elif self.color == RED:
            Chip_List = [i for i in range(1, len(self.chips) + 1)] #Создаём список неиспользованных фишек 
        index_chip = Chip_List.pop(random.randint(0, len(Chip_List)-1)) - 1 #Выбираем любую фишку
        Turn = True
        while Turn:
            if (self.chips[index_chip]+points) in self.chips: #Случай, когда там своя фишка
                if len(Chip_List) == 0: #Если множество пустое
                    Turn = False #Ход окончен - выходим
                else:
                    index_chip = Chip_List.pop(random.randint(0, len(Chip_List)-1)) - 1 #Выбираем новую фишку
            elif (self.chips[index_chip]+points) in Enemy.chips: #Случай, когда там вражья фишка
                enemy_index_chip = Enemy.chips.index(self.chips[index_chip]+points) #Берём индекс вражеской фишки
                neigh = Neighbors(Enemy.chips, enemy_index_chip)
                
                if len(neigh) == 1: #Если фишка без соседей, мы с ней меняемся
                    self.chips[index_chip], Enemy.chips[enemy_index_chip] = Enemy.chips[enemy_index_chip], self.chips[index_chip]
                    Turn = False #Ход окончен

                elif len(neigh) == 2: #Если у фишки два соседа - их не разбить, выходим
                    if len(Chip_List) == 0: #Если множество пустое
                        Turn = False #Ход окончен - выходим
                    else:
                        index_chip = Chip_List.pop(random.randint(0, len(Chip_List)-1)) - 1 #Выбираем новую фишку

                elif len(neigh) > 2: #Если у фишки более двух соседей
                    if (self.chips[index_chip] + points) == neigh[-2]: #Мы можем меняться <=> Фишка идёт на предпоследнее место
                        self.chips[index_chip], Enemy.chips[enemy_index_chip] = Enemy.chips[enemy_index_chip], self.chips[index_chip]
                        Turn = False #Ход окончен
                    else: #Иначе ход окончен без перемещения
                        if len(Chip_List) == 0: #Если множество пустое
                            Turn = False #Ход окончен - выходим
                        else:
                            index_chip = Chip_List.pop(random.randint(0, len(Chip_List)-1)) - 1 #Выбираем новую фишку
                         
            else: #Случай, когда там никого нет
                if points == 1 and points == 2: #Передвинутся на следующую или перешагнуть через одну на пустую можно всегда
                    self.chips[index_chip] = self.chips[index_chip]+points #Перемещаемся на пустое место
                    Turn = False
                    
                else: #Иначе проверяем, есть ли тут чужие или свои фишки
                    f = True
                    for i in range(1, points + 1): #Проверяем наличие фишек, своих или чужих, на пути
                        if (self.chips[index_chip]+i in self.chips or
                            self.chips[index_chip]+i in Enemy.chips):
                                f = False
                    if f: #Если можно  двигаться
                        self.chips[index_chip] = self.chips[index_chip]+points #Перемещаемся на пустое место
                        Turn = False
                    else: # Иначе
                        if len(Chip_List) == 0: #Если множество пустое
                            Turn = False #Ход окончен - выходим
                        else:
                            index_chip = Chip_List.pop(random.randint(0, len(Chip_List)-1)) - 1 #Выбираем новую фишку
        for x in self.chips:
            if x > 29:
                self.chips.remove(x)
        return ExTurn
        
def Neighbors(chips, i): #Определяет список из фишки и её соседей
    neigh = [chips[i]]
    for j in range(len(chips)):
        if i==j:
            continue
        else:
            if chips[j] == max(neigh) + 1 or chips[j] == min(neigh) - 1:
                neigh.append(chips[j])
    return neigh

def DrawChup(Num, Color): #Num - согласно правилам программирования
    pg.draw.circle(sc, Color, Cell_List[Num], int(Cell_X*2/5))

def EraseChip(Num):
    pg.draw.circle(sc, YELLOW, Cell_List[Num], int(Cell_X*2/5))

def SwapChips(Num1, Num2, Color1, Color2):
    pg.draw.circle(sc, Color2, Cell_List[Num1], int(Cell_X*2/5))
    pg.draw.circle(sc, Color1, Cell_List[Num2], int(Cell_X*2/5))

def Ankh(X, Y):
    pg.draw.circle(sc, BLACK, (X, Y), 20, 4)
    pg.draw.line(sc, BLACK, [X-20, Y+20], [X+20, Y+20], 5)
    pg.draw.line(sc, BLACK, [X, Y+20], [X, Y+50], 5)

def Nefer(Nefer_Center_X, Nefet_Center_Y):
    pg.draw.line(sc, BLACK, [Nefer_Center_X-10, Nefet_Center_Y], [Nefer_Center_X+10, Nefet_Center_Y], 5)
    pg.draw.line(sc, BLACK, [Nefer_Center_X, Nefet_Center_Y-10], [Nefer_Center_X, Nefet_Center_Y+30], 5)

    pg.draw.line(sc, BLACK, [Nefer_Center_X-10-25, Nefet_Center_Y], [Nefer_Center_X+10-25, Nefet_Center_Y], 5)
    pg.draw.line(sc, BLACK, [Nefer_Center_X-25, Nefet_Center_Y-10], [Nefer_Center_X-25, Nefet_Center_Y+30], 5)

    pg.draw.line(sc, BLACK, [Nefer_Center_X-10+25, Nefet_Center_Y], [Nefer_Center_X+10+25, Nefet_Center_Y], 5)
    pg.draw.line(sc, BLACK, [Nefer_Center_X+25, Nefet_Center_Y-10], [Nefer_Center_X+25, Nefet_Center_Y+30], 5)

def Chaos(C_C_X, C_C_Y, S_X, S_Y):
    pg.draw.lines(sc, BLACK, False, [[C_C_X-S_X*4, C_C_Y-S_Y], [C_C_X-S_X*3, C_C_Y-S_Y/2-S_Y], [C_C_X-S_X*2, C_C_Y-S_Y],
                                     [C_C_X-S_X, C_C_Y-S_Y/2-S_Y], [C_C_X, C_C_Y-S_Y], [C_C_X+S_X, C_C_Y-S_Y/2-S_Y],
                                     [C_C_X+S_X*2, C_C_Y-S_Y], [C_C_X+S_X*3, C_C_Y-S_Y/2-S_Y], [C_C_X+S_X*4, C_C_Y-S_Y]], 5)

    pg.draw.lines(sc, BLACK, False, [[C_C_X-S_X*4, C_C_Y], [C_C_X-S_X*3, C_C_Y-S_Y/2], [C_C_X-S_X*2, C_C_Y],
                                     [C_C_X-S_X, C_C_Y-S_Y/2], [C_C_X, C_C_Y], [C_C_X+S_X, C_C_Y-S_Y/2],
                                     [C_C_X+S_X*2, C_C_Y], [C_C_X+S_X*3, C_C_Y-S_Y/2], [C_C_X+S_X*4, C_C_Y]], 5)

    pg.draw.lines(sc, BLACK, False, [[C_C_X-S_X*4, C_C_Y+S_Y], [C_C_X-S_X*3, C_C_Y-S_Y/2+S_Y], [C_C_X-S_X*2, C_C_Y+S_Y],
                                     [C_C_X-S_X, C_C_Y-S_Y/2+S_Y], [C_C_X, C_C_Y+S_Y], [C_C_X+S_X, C_C_Y-S_Y/2+S_Y],
                                     [C_C_X+S_X*2, C_C_Y+S_Y], [C_C_X+S_X*3, C_C_Y-S_Y/2+S_Y], [C_C_X+S_X*4, C_C_Y+S_Y]], 5)

def Bird(Bird_Center_X, Bird_Center_Y, Stick_X, Stick_Y):
    pg.draw.line(sc, BLACK, [Bird_Center_X, Bird_Center_Y-Stick_Y],
                            [Bird_Center_X, Bird_Center_Y+Stick_Y], 4)

    pg.draw.line(sc, BLACK, [Bird_Center_X-Stick_X, Bird_Center_Y-Stick_Y],
                            [Bird_Center_X+Stick_X, Bird_Center_Y-Stick_Y], 4)
    pg.draw.line(sc, BLACK, [Bird_Center_X-Stick_X, Bird_Center_Y+Stick_Y],
                            [Bird_Center_X+Stick_X, Bird_Center_Y+Stick_Y], 4)
    #===
    pg.draw.line(sc, BLACK, [Bird_Center_X-3*Stick_X, Bird_Center_Y-Stick_Y],
                            [Bird_Center_X-3*Stick_X, Bird_Center_Y+Stick_Y], 4)

    pg.draw.line(sc, BLACK, [Bird_Center_X-Stick_X-3*Stick_X, Bird_Center_Y-Stick_Y],
                            [Bird_Center_X+Stick_X-3*Stick_X, Bird_Center_Y-Stick_Y], 4)
    pg.draw.line(sc, BLACK, [Bird_Center_X-Stick_X-3*Stick_X, Bird_Center_Y+Stick_Y],
                            [Bird_Center_X+Stick_X-3*Stick_X, Bird_Center_Y+Stick_Y], 4)
    #===
    pg.draw.line(sc, BLACK, [Bird_Center_X+3*Stick_X, Bird_Center_Y-Stick_Y],
                            [Bird_Center_X+3*Stick_X, Bird_Center_Y+Stick_Y], 4)

    pg.draw.line(sc, BLACK, [Bird_Center_X-Stick_X+3*Stick_X, Bird_Center_Y-Stick_Y],
                            [Bird_Center_X+Stick_X+3*Stick_X, Bird_Center_Y-Stick_Y], 4)
    pg.draw.line(sc, BLACK, [Bird_Center_X-Stick_X+3*Stick_X, Bird_Center_Y+Stick_Y],
                            [Bird_Center_X+Stick_X+3*Stick_X, Bird_Center_Y+Stick_Y], 4)

def Human(Human_Center_X, Human_Center_Y, Stick_X, Stick_Y):
    pg.draw.line(sc, BLACK, [Human_Center_X-1.5*Stick_X, Human_Center_Y-Stick_Y],
                            [Human_Center_X-1.5*Stick_X, Human_Center_Y+Stick_Y], 4)

    pg.draw.line(sc, BLACK, [Human_Center_X-Stick_X-1.5*Stick_X, Human_Center_Y-Stick_Y],
                            [Human_Center_X+Stick_X-1.5*Stick_X, Human_Center_Y-Stick_Y], 4)
    pg.draw.line(sc, BLACK, [Human_Center_X-Stick_X-1.5*Stick_X, Human_Center_Y+Stick_Y],
                            [Human_Center_X+Stick_X-1.5*Stick_X, Bird_Center_Y+Stick_Y], 4)
    #===
    pg.draw.line(sc, BLACK, [Human_Center_X+1.5*Stick_X, Human_Center_Y-Stick_Y],
                            [Human_Center_X+1.5*Stick_X, Human_Center_Y+Stick_Y], 4)

    pg.draw.line(sc, BLACK, [Human_Center_X-Stick_X+1.5*Stick_X, Human_Center_Y-Stick_Y],
                            [Human_Center_X+Stick_X+1.5*Stick_X, Human_Center_Y-Stick_Y], 4)
    pg.draw.line(sc, BLACK, [Human_Center_X-Stick_X+1.5*Stick_X, Human_Center_Y+Stick_Y],
                            [Human_Center_X+Stick_X+1.5*Stick_X, Human_Center_Y+Stick_Y], 4)

def InList(x, y):
    for i in range(30):
        xC = Play_Field[i][0]
        yC = Play_Field[i][1]
        if ((x>=xC-Cell_X/2 and x<=xC+Cell_X/2) and
            (y>=yC-Cell_Y/2 and y<=yC+Cell_Y/2)):
            return i
    return None

def EgDice():
    random.seed(os.urandom(17))
    q = random.randint(1, 16)
    if q<=4:
        return 1
    elif q<=10:
        return 2
    elif q<=14:
        return 3
    elif q==15:
        return 4
    elif q==16:
        return 5

pg.init()

sc = pg.display.set_mode((Window_WIDTH, Window_HEIGHT))
pg.display.set_caption('Senet')
background = pg.image.load('images\\background.png')
background_rect = background.get_rect(bottomright=(Window_WIDTH, Window_HEIGHT))
sc.blit(background, background_rect)

clock = pg.time.Clock()

pg.draw.rect(sc, YELLOW, (Window_WIDTH*Indent_X, Window_HEIGHT*Indent_Y,
                            Window_WIDTH*(1-Indent_X*2), Window_HEIGHT*(1-Indent_Y*2)))
pg.draw.rect(sc, BLACK, (Window_WIDTH*Indent_X, Window_HEIGHT*Indent_Y,
                            Window_WIDTH*(1-Indent_X*2), Window_HEIGHT*(1-Indent_Y*2)), Line_WIDTH_1)

pg.draw.line(sc, BLACK, [Window_WIDTH*Indent_X, Window_HEIGHT*Indent_Y+Window_HEIGHT*(1-Indent_Y*2)*1/3],
                        [Window_WIDTH*Indent_X+Window_WIDTH*(1-Indent_X*2)*0.9, Window_HEIGHT*Indent_Y+Window_HEIGHT*(1-Indent_Y*2)*1/3], Line_WIDTH_1)
pg.draw.line(sc, BLACK, [Window_WIDTH*Indent_X+Window_WIDTH*(1-Indent_X*2)*0.9, Window_HEIGHT*Indent_Y+Window_HEIGHT*(1-Indent_Y*2)*1/3],
                        [Window_WIDTH*(1-Indent_X), Window_HEIGHT*Indent_Y+Window_HEIGHT*(1-Indent_Y*2)*1/3], Line_WIDTH_2)

pg.draw.line(sc, BLACK, [Window_WIDTH*Indent_X, Window_HEIGHT*Indent_Y+Window_HEIGHT*(1-Indent_Y*2)*2/3],
                        [Window_WIDTH*Indent_X+Window_WIDTH*(1-Indent_X*2)*0.1, Window_HEIGHT*Indent_Y+Window_HEIGHT*(1-Indent_Y*2)*2/3], Line_WIDTH_2)
pg.draw.line(sc, BLACK, [Window_WIDTH*Indent_X+Window_WIDTH*(1-Indent_X*2)*0.1, Window_HEIGHT*Indent_Y+Window_HEIGHT*(1-Indent_Y*2)*2/3],
                        [Window_WIDTH*(1-Indent_X), Window_HEIGHT*Indent_Y+Window_HEIGHT*(1-Indent_Y*2)*2/3], Line_WIDTH_1)

for i in range(1, 10):
    pg.draw.line(sc, BLACK, [Window_WIDTH*Indent_X+Window_WIDTH*(1-2*Indent_X)*i/10, Window_HEIGHT*Indent_Y],
                             [Window_WIDTH*Indent_X+Window_WIDTH*(1-2*Indent_X)*i/10, Window_HEIGHT*(1-Indent_Y)], Line_WIDTH_2)
random.seed(os.urandom(17))
ColorDice = (random.randint(0, 1), random.randint(0, 1), random.randint(0, 1), random.randint(0, 1))
Cell_Y_Old = Cell_Y

#Дом Возрождения, Анкх
Ankh_Center_X = int(Window_WIDTH*Indent_X+Window_WIDTH*(1-Indent_X*2)*0.5+Cell_X/2)
Ankh_Center_Y = int(Window_HEIGHT*Indent_Y+Window_HEIGHT*(1-Indent_Y*2)*1/3+Cell_Y_Old/4)

#Дом Красоты, Нефер
Nefer_Center_X = Ankh_Center_X
Nefer_Center_Y = Ankh_Center_Y + Cell_Y_Old*2/3

#Дом Воды, Хаос
C_C_X = Nefer_Center_X + Cell_X #Chaos_Center_X
C_C_Y = Nefer_Center_Y + Cell_Y/10 #Chaos_Center_Y
S_X = 8 #Shift_X; Смещение по иксу
S_Y = 15 #Shift_Y; Смещение по игреку

#Дом трёх Истин, Птица
Bird_Center_X = C_C_X + Cell_X
Bird_Center_Y = C_C_Y
Stick_X = 8
Stick_Y = 20

#Дом Исиды и Нефтиды, Человек
Human_Center_X = Bird_Center_X + Cell_X
Human_Center_Y = Bird_Center_Y

Cell_Y = Window_HEIGHT*(1-Indent_Y*2)/3
Play_Field = [0]*30
Cell_List_X = int(Window_WIDTH*Indent_X+Cell_X/2)
Cell_List_Y = int(Window_HEIGHT*Indent_Y+Cell_Y/2)
Radius_Chip = int(int(Cell_X*2/5))
for i in range(10):
    Play_Field[i] = [int(Cell_List_X), int(Cell_List_Y), YELLOW]
    Cell_List_X += Cell_X
Cell_List_X -= Cell_X
Cell_List_Y += Cell_Y

for i in range(10, 20):
    Play_Field[i] = [int(Cell_List_X), int(Cell_List_Y), YELLOW]
    Cell_List_X -= Cell_X
Cell_List_X += Cell_X
Cell_List_Y += Cell_Y

for i in range(20, 30):
    Play_Field[i] = [int(Cell_List_X), int(Cell_List_Y), YELLOW]
    Cell_List_X += Cell_X           
pg.display.update()

BluePlayer = Player([0, 2, 4, 6, 8], BLUE)
RedPlayer = Player([1, 3, 5, 7, 9], RED)
List_Player = [BluePlayer, RedPlayer]

kol = 0

#Определяем кто первый играет
k_player = 0
random.seed(os.urandom(17))
qqq = True
choice = EgDice()
while choice != 1:
    choice = EgDice()
    qqq = not qqq
font1 = pg.font.Font(None, 36)
    
if qqq:
    HumanPlayer = BluePlayer
    AIPlayer = RedPlayer
    text = font1.render('Вы играете за синих', 1, BLUE)
else:
    HumanPlayer = RedPlayer
    AIPlayer = BluePlayer
    text = font1.render('Вы играете за красных', 1, RED)
sc.blit(text, (150, Window_HEIGHT*4/20-10))
choice = EgDice()
while choice not in (2, 3):
    choice = EgDice()

ToPlay = True
ToAI = False
HighPos = []

while True:
    clock.tick(FPS)

    #Отрисовка фишек
    for i in range(30): #Заменить на отрисовку фишек игроков
        #pg.draw.circle(sc, Play_Field[i][2], Play_Field[i][0:2], Radius_Chip)
        if i in BluePlayer.chips:
            pg.draw.circle(sc, BLUE, Play_Field[i][0:2], Radius_Chip)
        elif i in RedPlayer.chips:
            pg.draw.circle(sc, RED, Play_Field[i][0:2], Radius_Chip)
        else:
            pg.draw.circle(sc, YELLOW, Play_Field[i][0:2], Radius_Chip)
        
    #Палочки сенета
    for i in range(4): 
        if ColorDice[i]:
            pg.draw.rect(sc, BLACK, (20+2*20*i, Window_HEIGHT*16/20,
                                 20, Window_HEIGHT*4/20-10))
        else:
            pg.draw.rect(sc, WHITE, (20+2*20*i, Window_HEIGHT*16/20,
                                 20, Window_HEIGHT*4/20-10))
        for e in pg.event.get(): #Обработчик событий
            if e.type == pg.QUIT: #Выход
                pg.quit()
                sys.exit()
            elif e.type == pg.KEYDOWN and ToPlay:
                if e.key == pg.K_SPACE: #Бросок палочек
                    random.seed(os.urandom(17))
                    ColorDice = (random.randint(0, 1), random.randint(0, 1), random.randint(0, 1), random.randint(0, 1))
                    s = 0
                    for x in ColorDice:
                        s += x
                    if s == 0:
                        points = 5
                    else:
                        points = s
            elif e.type == pg.MOUSEBUTTONDOWN and ToPlay: #Обработчик отрисовки мышки
                if InList(e.pos[0], e.pos[1]) != None:
                    k = InList(e.pos[0], e.pos[1])
                    if HighPos == []:
                        HighPos.append(k)
                    elif len(HighPos) == 1:
                        HighPos.append(k)
                        if k in AIPlayer.chips: #Обдумать нормальную замену
                            HumanPlayer.chips[HighPos[0]], AIPlayer.chips[AIPlayer.chips.index(HighPos[1])] = AIPlayer.chips[AIPlayer.chips.index(HighPos[1])], HumanPlayer.chips[HighPos[0]]
                        elif k in HumanPlayer.chips:
                            continue
                        else:
                            HumanPlayer.chips[HumanPlayer.chips.index(HighPos[0])] = HighPos[1]
                        ToPlay = False
                        ToAI = True
                        HighPos = []
    #AI
    k = 1
    while ToAI and k:
        k -= 1
        q = AIPlayer.move(HumanPlayer, choice) #Получаем, есть ли право на доп. ход
        if q:
            k += 1
            q = False
        if len(BluePlayer.chips) == 0:
            print('ПОБЕДИЛ СИНИЙ ИГРОК')
            ToAI = False
            break
        elif len(RedPlayer.chips) == 0:
            print('ПОБЕДИЛ КРАСНЫЙ ИГРОК')
            ToAI = False
            break
        else:
            ToAI = False
            ToPlay = True
            choice = EgDice()
    
    #Отрисовка символов
    Ankh(Ankh_Center_X, Ankh_Center_Y)
    Nefer(Nefer_Center_X, Nefer_Center_Y)
    Chaos(C_C_X, C_C_Y, S_X, S_Y)
    Bird(Bird_Center_X, Bird_Center_Y, Stick_X, Stick_Y)
    Human(Human_Center_X, Human_Center_Y, Stick_X, Stick_Y)
    
    pg.display.update()
'''
    keys = pg.key.get_pressed()
    if keys[pg.K_SPACE]:
        random.seed(os.urandom(17))
        ColorDice = (random.randint(1, 2), random.randint(1, 2),
                     random.randint(1, 2), random.randint(1, 2))
'''














