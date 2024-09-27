import pygame as pg
from time import sleep as s
from random import randint

horizontalLength = max(2, min(int(input("Enter horizontal size (2 to 17):\n")), 17))
verticalLength = max(2, min(int(input("Enter vertical size (2 to 8):\n")), 8))
totalBoxes = horizontalLength*verticalLength
totalLines = (2*horizontalLength*verticalLength)+horizontalLength+verticalLength
boxSize = 80
player1LineColor,computerLineColor = [11,253,204], [254,58,107]# line colors blue and red
screen = pg.display.set_mode((horizontalLength*boxSize+40,verticalLength*boxSize+40))
screen.fill(((30,30,30)))# background color
boxPosition = []

for i in range(horizontalLength * verticalLength):
    boxNumber = i + 1
    if boxNumber == 1:
        boxPosition.append('topLeftCorner')
    elif boxNumber == horizontalLength:
        boxPosition.append('topRightCorner')
    elif boxNumber == horizontalLength * verticalLength - horizontalLength + 1:
        boxPosition.append('bottomLeftCorner')
    elif boxNumber == horizontalLength * verticalLength:
        boxPosition.append('bottomRightCorner')
    elif boxNumber in [j + 2 for j in range(horizontalLength - 2)]:
        boxPosition.append('topEdge')
    elif boxNumber in [horizontalLength * verticalLength + j + 2 - horizontalLength for j in range(horizontalLength - 2)]:
        boxPosition.append('bottomEdge')
    elif boxNumber in [horizontalLength * (j + 2) for j in range(verticalLength - 2)]:
        boxPosition.append('rightEdge')
    elif boxNumber in [horizontalLength * (j + 1) + 1 for j in range(verticalLength - 2)]:
        boxPosition.append('leftEdge')
    else:
        boxPosition.append('Center')


def drawDots():
    for i in range(horizontalLength+1):
        for j in range(verticalLength+1):
            pg.draw.circle(screen ,'white',(20+boxSize*i,20+boxSize*j),3)

def drawLines(playerMove):
    for localMove in playerMove:
        moveType = localMove[:2]
        x, y = map(int, localMove[2:].split('/'))
        color = player1LineColor if 'b' in moveType else computerLineColor
        rect = (24 + boxSize * x, 19 + boxSize * y, boxSize - 8, 2) if 'h' in moveType else (19 + boxSize * x, 24 + boxSize * y, 2, boxSize - 8)
        # 24 = 20 margin + 4 is to center line on horizontally, since we are reducing 8 px from line for dots to be visible
        # 19 = 20 margin - 1 is to center line  vertically 
        # for vertical line we can reverse the margins
        pg.draw.rect(screen, color, rect)

def getClickedLine():
    mouse = pg.mouse.get_pos()
    x, y = (mouse[0] - 15) // boxSize, (mouse[1] - 15) // boxSize
    if x > horizontalLength or y > verticalLength or mouse[1] < 20 or mouse[0] < 20:
        return None
    for i in range(horizontalLength + verticalLength):
        if 15 + boxSize * i < mouse[0] < 30 + boxSize * i:
            return f'bv{x}/{y}' if x <= horizontalLength and y <= verticalLength - 1 else None
        elif 15 + boxSize * i < mouse[1] < 30 + boxSize * i:
            return f'bh{x}/{y}' if x <= horizontalLength - 1 and y <= verticalLength else None
    return None


     
def isMoveNotTaken(move):
    if any(move1 in [f'r{move[1:]}', f'b{move[1:]}'] for move1 in totalMoves):
        return (False)
    else:
        return (True)
    
filledBoxes = []
def chk_sqr(who):
    # I want to change this function 
    # instead of going through all the boxes
    # check the boxes that are touching the move 
    # if x and y are 0 or verticalLength or horizontalLength then we need only to 
    # check for the one box inside the grid or else we need to check two boxes touching the move.
    flag = 0
    for i in range(totalBoxes):
        boxNumber = i + 1
        if boxNumber not in filledBoxes:
            hx = (boxNumber - 1) % horizontalLength
            hy = (boxNumber - 1) // horizontalLength
            sidesOfBoxNumber = [f'rh{hx}/{hy}', f'rv{hx}/{hy}', f'rh{hx}/{hy + 1}', f'rv{hx + 1}/{hy}']
            # Check if all sides have been played
            if all(not isMoveNotTaken(move) for move in sidesOfBoxNumber):
                filledBoxes.extend([who, boxNumber])
                score(who, boxNumber)
                flag = 1
                # this flag there to make sure that every scored box is counted before returning
    return flag == 1


def makeBoxMove():
    for i in range(totalBoxes):
        boxNumber = i + 1
        if boxNumber not in filledBoxes:
            hx = (boxNumber - 1) % horizontalLength
            hy = (boxNumber - 1) // horizontalLength
            sidesOfBoxNumber = [f'rh{hx}/{hy}', f'rv{hx}/{hy}', f'rh{hx}/{hy + 1}', f'rv{hx + 1}/{hy}']
            moveStatus = [isMoveNotTaken(move) for move in sidesOfBoxNumber]
            # chk_sqr(who) have same logic want to make faction for that but 
            # I might change chk_sqr(who) in future if not then I make a new function for that
            # Check if exactly one side is available (True) out of four (3 False) # 
            if moveStatus.count(False) == 3:
                return sidesOfBoxNumber[moveStatus.index(True)]
def rend_move():
    randomType = randint(0,10)
    if randomType%2 == 0:
        typ = 'rh' 
        randomX = randint(0,horizontalLength-1)
        randomY = randint(0,verticalLength)
    else:
        typ = 'rv'
        randomX = randint(0,horizontalLength)
        randomY = randint(0,verticalLength-1)
    return(typ,randomX,randomY)

def smartMove(typ,x,y,cnt):
    snakes = []
    if cnt == totalLines:
        snakes = mk_snk()
        return(snakes)
    else:
        m1 = []
        tf = []
        if typ == 'rh':
            if y != 0:
                m1.append('rv'+str(x+1)+'/'+str(y-1))
                m1.append('rh'+str(x)+'/'+str(y-1))
                m1.append('rv'+str(x)+'/'+str(y-1))
            if y != verticalLength:
                m1.append('rv'+str(x)+'/'+str(y))
                m1.append('rh'+str(x)+'/'+str(y+1))
                m1.append('rv'+str(x+1)+'/'+str(y))
        elif typ == 'rv':
            if x != 0:
                m1.append('rh'+str(x-1)+'/'+str(y))
                m1.append('rv'+str(x-1)+'/'+str(y))
                m1.append('rh'+str(x-1)+'/'+str(y+1))
            if x != horizontalLength:
                m1.append('rh'+str(x)+'/'+str(y+1))
                m1.append('rv'+str(x+1)+'/'+str(y))
                m1.append('rh'+str(x)+'/'+str(y))
        for word in m1:
            tf.append(isMoveNotTaken(word))
        vd = tf.count(False)    
        if len(tf) == 6:
            if vd > 2:
                return(False)
            else:
                vd1 = tf[:3].count(False)
                vd2 = tf[3:].count(False)
                if vd1 > 1 or vd2 > 1:
                    return(False)
                else:
                    return(True)
        if len(tf) == 3:
            if vd > 1:
                return(False)
            else:
                return(True)

def chk_dir(p,a_div):
    r_dir = a_div
    if a_div =='rl':
        if p == 'Center' or p == 'topEdge' or p == 'bottomEdge':
            r_dir = 'rl'
        elif p == 'rightEdge'or p == 'topRightCorner'or p == 'bottomRightCorner':
            r_dir = 'l'
        elif p == 'leftEdge'or p == 'topLeftCorner'or p == 'bottomLeftCorner':
            r_dir = 'r'
        else:
            pass
    elif a_div =='ud':
        if p == 'Center' or p == 'rightEdge' or p == 'leftEdge':
            r_dir = 'ud'
        elif p == 'bottomEdge'or p == 'bottomRightCorner'or p == 'bottomLeftCorner':
            r_dir = 'u'
        elif p == 'topEdge'or p == 'topLeftCorner'or p == 'topRightCorner':
            r_dir = 'd'
        else:
            pass
    elif a_div =='rd':
        if p == 'Center' or p == 'topEdge' or p == 'leftEdge'or p == 'topLeftCorner':
            r_dir = 'rd'
        elif p == 'bottomEdge'or p == 'bottomLeftCorner':
            r_dir = 'r'
        elif p == 'rightEdge'or p == 'topRightCorner':
            r_dir = 'd'
        elif p == 'bottomRightCorner':
            r_dir = ''
        else:
            pass
    elif a_div =='lu':
        if p == 'Center' or p == 'bottomEdge' or p == 'rightEdge'or p == 'bottomRightCorner':
            r_dir = 'lu'
        elif p == 'topEdge'or p == 'topRightCorner':
            r_dir = 'l'
        elif p == 'leftEdge'or p == 'bottomLeftCorner':
            r_dir = 'u'
        elif p == 'topLeftCorner':
            r_dir = ''
        else:
            pass
    elif a_div =='ru':
        if p == 'Center' or p == 'bottomEdge' or p == 'leftEdge'or p == 'bottomLeftCorner':
            r_dir = 'ru'
        elif p == 'topEdge'or p == 'topLeftCorner':
            r_dir = 'r'
        elif p == 'rightEdge'or p == 'bottomRightCorner':
            r_dir = 'u'
        elif p == 'topRightCorner':
            r_dir = ''
        else:
            pass
    elif a_div =='ld':
        if p == 'Center' or p == 'topEdge' or p == 'rightEdge'or p == 'topRightCorner':
            r_dir = 'ld'
        elif p == 'bottomEdge'or p == 'bottomRightCorner':
            r_dir = 'l'
        elif p == 'leftEdge'or p == 'topLeftCorner':
            r_dir = 'd'
        elif p == 'bottomLeftCorner':
            r_dir = ''
        else:
            pass
    else:
        pass
    return(r_dir)

def shift_dir():
    bns = []
    sd = []
    for i in range(totalBoxes):
        tf = []
        bn = i+1
        if True: #bn not in box fill
            if bn%horizontalLength == 0:
                hx = horizontalLength - 1
            else:
                hx = (bn%horizontalLength) - 1
            hy = int((bn-hx-1)/horizontalLength)
            sidesOfBox = ['lh'+str(hx)+'/'+str(hy),'lv'+str(hx)+'/'+str(hy),'lh'+str(hx)+'/'+str(hy+1),'lv'+str(hx+1)+'/'+str(hy)]
            for word in sidesOfBox:
                tf.append(isMoveNotTaken(word))
            if tf.count(False) == 2:
                hv='a'
                if tf[0] == tf[2]:
                    if tf[0] == False:
                        hv='rl'
                    elif tf[1] == False:
                        hv='ud'
                elif tf[0] == tf[1]:
                    if tf[0] == False:
                        hv='rd'
                    elif tf[2] == False:
                        hv='lu'
                elif tf[1] == tf[2]:
                    if tf[1] == False:
                        hv='ru'
                    elif tf[3] == False:
                        hv='ld'
            elif tf.count(False) == 1:
                hv='a'
                if tf[0] == False:
                    hv = 'rdl'
                elif tf[1] == False:
                    hv = 'urd'
                elif tf[2] == False:
                    hv = 'rul'
                elif tf[3] == False:
                    hv = 'uld'
            else:
                hv = ''
            r_dir = chk_dir(boxPosition[bn-1],hv)
            bns.append(bn)
            sd.append(r_dir)
    return bns,sd
# ([1,  2,     3,    4,    5,    6,   7,      8,    9,   10,    11,   12,  13,  14,   15,  16], 
# ['r', 'rl', 'rl', 'ld', 'rd', 'rl', 'rl', 'uld', 'ru', 'rl', 'rl', 'lu', 'r', 'rl', 'l', ''])
# [[16], [13, 14, 15], [1, 2, 3, 4, 8, 12, 5, 6, 7, 9, 10, 11]]

def mk_snk():

    # making snakes have bug where it sometimes combines two snakes into one
    # it connects two snakes where if we have intersection a box have 3 open sides instead of 2
    # find and fix this bug
    asa = shift_dir()
    print(asa)
    boxNumber=asa[0]
    availableDirection=asa[1]
    snakes=[]
    def find_snakes(x):
        for snake in range(len(snakes)):
            for j in range(len(snakes[snake])):
                if snakes[snake][j] == x:
                    return snake
    for i in range(len(boxNumber)):
        if i == 0:
            snakes.append([boxNumber[i]])
        if len(availableDirection[i]) ==3 :
            continue
        if 'l' in availableDirection[i]:
            f=find_snakes(boxNumber[i-1])
            if f == None:
                snakes.append([boxNumber[i]])
            else:
                snakes[f].append(boxNumber[i])
        if 'u' in availableDirection[i]:
            f=find_snakes(boxNumber[i-horizontalLength])
            if f == None:
                snakes.append([boxNumber[i]])
            else:
                snakes[f].append(boxNumber[i])
        if 'r' in availableDirection[i]:
            f=find_snakes(boxNumber[i+1])
            if f == None:
                snakes.append([boxNumber[i]])
            else:
                snakes[f].append(boxNumber[i])
        if 'd' in availableDirection[i]:
            f=find_snakes(boxNumber[i+horizontalLength])
            if f == None:
                snakes.append([boxNumber[i]])
            else:
                snakes[f].append(boxNumber[i])
        if availableDirection[i] == '':
            snakes.append([boxNumber[i]])
    for i in range(len(snakes)):
        for j in range(len(snakes[i])):
            f=find_snakes(snakes[i][j])
            if i != f:
                snakes[f] = snakes[f]+snakes[i]
                snakes[i] = []
                break
    for i in range(len(snakes)):
        snakes[i] = list(dict.fromkeys(snakes[i]))
    snakes = list(filter(None,snakes))
    for i in range(len(snakes)):
        if snakes[i][0] in filledBoxes: 
            snakes[i] = []
    snakes.sort(key=len)
    snakes = list(filter(None,snakes))
    snakes1 = snakes
    return snakes1

def computer():
    cnt = 0
    snakes = []
    completeBoxMove = makeBoxMove()
    if completeBoxMove:
        return completeBoxMove
    while True:
        randomMove = rend_move()
        computerMove = randomMove[0]+str(randomMove[1])+'/'+str(randomMove[2])
        if isMoveNotTaken(computerMove):
            sm = smartMove(randomMove[0],randomMove[1],randomMove[2],cnt)
            print(sm)
            if sm == True:
                break
            else:
                cnt = cnt + 1
            if type(sm) is list:
                snakes = sm
                break
        else:
            pass
    if snakes:
        bn = snakes[0][0]
        snakes.remove(snakes[0])
        if bn%horizontalLength == 0:
            hx = horizontalLength - 1
        else:
            hx = (bn%horizontalLength) - 1
        hy = int((bn-hx-1)/horizontalLength)
        sidesOfBox = ['rh'+str(hx)+'/'+str(hy),'rv'+str(hx)+'/'+str(hy),'rh'+str(hx)+'/'+str(hy+1),'rv'+str(hx+1)+'/'+str(hy)]
        for i in range(4):
            if isMoveNotTaken(sidesOfBox[i]):
                return sidesOfBox[i]
    return computerMove

p1s,ais = [],[]
def score(who,bn):
    if who == 'p1':
        p1s.append(bn)
    elif who == 'ai':
        ais.append(bn)
    else:
        pass

## main game loop
totalMoves = []
 
isPlayer1Move =  randint(0,1)
print(isPlayer1Move)
drawDots()
while True:
    event = pg.event.poll()
    if event.type == pg.QUIT:
        break
    if isPlayer1Move: 
        if pg.mouse.get_pressed()[0] == 1:
            player1Move = getClickedLine()
            if player1Move and isMoveNotTaken(player1Move):
                totalMoves.append(player1Move)
                s(0.2)
                if not chk_sqr('p1'):
                    isPlayer1Move = False
    else:
        a1 = computer()
        totalMoves.append(a1)
        s(0.2)
        if not chk_sqr('ai'):
            isPlayer1Move = True
    drawLines(totalMoves)
    pg.display.flip()
    s(0.1)
    if len(totalMoves) == totalLines:
        print('GAME IS OVER\nYour box : ',len(p1s),p1s,'\n','AI box :',len(ais),ais)
        if len(p1s) > len(ais):
            print('You Win GG :)')
        elif len(p1s) < len(ais):
            print('Computer Wins:)')
        else:
            print('Draw')
        s(1000)


# add more global variables that will be used in the game