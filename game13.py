import pygame as pg
from time import sleep as s
from random import randint

a = int(input("Enter size\n"))
b = int(input())
if a < 2 or b < 2:
    a,b = 2,2
elif a > 20 or b > 10:
    a,b = 20,10
tsqr = a*b
c_tl = [1]
c_tr = [a]
c_bl = [(a*b)+1-a] 
c_br = [a*b]
e_t = []
for i in range(a-2):
    e_t.append(i+2)
e_b = []
for i in range(a-2):
    e_b.append((a*b)+2+i-a)
e_r = []
for i in range(b-2):
    e_r.append(a*(i+2))
e_l = []
for i in range(b-2):
    e_l.append((a*(i+1))+1)
ce_all = c_tl+c_tr+c_bl+c_br+e_t+e_b+e_r+e_l
pos = []
for i in range(a*b):
    bn = i+1
    if bn not in ce_all:
        pos.append('c')
    elif bn  in e_t:
        pos.append('et')
    elif bn  in e_b:
        pos.append('eb')
    elif bn  in e_r:
        pos.append('er')
    elif bn  in e_l:
        pos.append('el')
    elif bn  in c_tl:
        pos.append('ctl')
    elif bn  in c_tr:
        pos.append('ctr')
    elif bn  in c_bl:
        pos.append('cbl')
    elif bn  in c_br:
        pos.append('cbr')
    else:
        pass
tline = ((a - 1)*(b - 1)*2)+(((a - 1)+(b - 1))*3)+4
p1_move = []
ai_move = []
shmovelist = []
scl = 80
screen = pg.display.set_mode((a*scl+40,b*scl+40))
running = True
player_move = True
sqfill = []
yourclr = [11,253,204]
aiclr = [254,58,107]
def dots():
    for i in range(a+1):
        for j in range(b+1):
            pg.draw.circle(screen ,(100,100,100),(20+scl*i,20+scl*j),3)
def drli(pmove):
    for word in pmove:
        typ = word[:2]
        x = int(word[2:word.find('/')])
        y = int(word[word.find('/')+1:])
        if typ == 'bh':
            pg.draw.aaline(screen ,(yourclr),(26+scl*x,20+scl*y),(10+scl+scl*x,19+scl*y))#hl
            pg.draw.aaline(screen ,(yourclr),(26+scl*x,20+scl*y),(11+scl+scl*x,20+scl*y))
            pg.draw.aaline(screen ,(yourclr),(26+scl*x,20+scl*y),(12+scl+scl*x,21+scl*y))
        elif typ == 'bv':
            pg.draw.aaline(screen ,(yourclr),(19+scl*x,25+scl*y),(20+scl*x,+11+scl+scl*y))#vl
            pg.draw.aaline(screen ,(yourclr),(20+scl*x,26+scl*y),(20+scl*x,+11+scl+scl*y))#vl
            pg.draw.aaline(screen ,(yourclr),(21+scl*x,27+scl*y),(20+scl*x,+11+scl+scl*y))#vl
        elif typ == 'rh':
            pg.draw.aaline(screen ,(aiclr),(26+scl*x,20+scl*y),(10+scl+scl*x,19+scl*y))#hl
            pg.draw.aaline(screen ,(aiclr),(26+scl*x,20+scl*y),(11+scl+scl*x,20+scl*y))#hl
            pg.draw.aaline(screen ,(aiclr),(26+scl*x,20+scl*y),(12+scl+scl*x,21+scl*y))#hl
        elif typ == 'rv':
            pg.draw.aaline(screen ,(aiclr),(19+scl*x,25+scl*y),(20+scl*x,+11+scl+scl*y))#vl
            pg.draw.aaline(screen ,(aiclr),(20+scl*x,26+scl*y),(20+scl*x,+11+scl+scl*y))#vl
            pg.draw.aaline(screen ,(aiclr),(21+scl*x,27+scl*y),(20+scl*x,+11+scl+scl*y))#vl
        else:
            pass
def click():
    mouse = pg.mouse.get_pos()
    x1 = mouse[0]-15
    y1 = mouse[1]-15
    x = int(x1/scl)#int(str(
    y = int(y1/scl)
    for i in range(a+b):
        if 15+scl*i < mouse[0]< 30+scl*i:
            if x > a or y > b-1 :
                pass#stop click outside
            elif mouse[1] < 20:
                pass#stop click outside
            else:
                return('bv'+str(x)+'/'+str(y))
        elif 15+scl*i < mouse[1] < 30+scl*i:
            if x > a-1 or y > b :
                pass#stop click outside
            elif mouse[0] < 20:
                pass#stop click outside
            else:
                return('bh'+str(x)+'/'+str(y))
def move(who,move):
    if who == 'p1':
        p1_move.append(move)
        shmovelist.append(move[1:])
        p2 = list(dict.fromkeys(p1_move))
        s(0.2)
    else:
        ai_move.append(move)
        shmovelist.append(move[1:])
        a2 = list(dict.fromkeys(ai_move))
        s(0.2)
        pass
    scored = chk_sqr(who)
    if scored == True:
        return(True)
    else:
        pass
def move_test(move):
    movelist = p1_move+ai_move
    if move[1:] not in shmovelist:
        return (True)
    else:
        return (False)
def chk_sqr(who):
    flg = 0
    for i in range(tsqr):
        bn = i+1
        if bn not in sqfill:
            if bn%a == 0:
                hx = a - 1
            else:
                hx = (bn%a) - 1
            hy = int((bn-hx-1)/a)
            sqmove = ['lh'+str(hx)+'/'+str(hy),'lv'+str(hx)+'/'+str(hy),'lh'+str(hx)+'/'+str(hy+1),'lv'+str(hx+1)+'/'+str(hy)]
            if move_test(sqmove[0])!= True and move_test(sqmove[1])!= True and move_test(sqmove[2])!= True and move_test(sqmove[3])!= True:
                sqfill.append(who)
                sqfill.append(bn)
                score(who,bn)
                flg = 1 
            else:
                pass
    if flg == 1:
        return(True)
def ai():
    cnt = 0
    cnt2 = 0
    snks = []
    smove = com_sqr_move()
    if smove != None:
        return smove
    while True:
        rendmove = rend_move()
        aimove = rendmove[0]+str(rendmove[1])+'/'+str(rendmove[2])
        mt = move_test(aimove)
        if mt == True:
            if cnt2 < 1:
                sm = smart_move(rendmove[0],rendmove[1],rendmove[2],cnt,cnt2)            
                if sm == True:
                    break
                elif sm == False:
                    cnt = cnt + 1
                else:
                    pass
                if type(sm) is list:
                    snks = sm
                    break
            else:
                pass
        else:
            pass
    if snks != []:
        bn = snks[0][0]
        snks.remove(snks[0])
        if bn%a == 0:
            hx = a - 1
        else:
            hx = (bn%a) - 1
        hy = int((bn-hx-1)/a)
        sqmove = ['rh'+str(hx)+'/'+str(hy),'rv'+str(hx)+'/'+str(hy),'rh'+str(hx)+'/'+str(hy+1),'rv'+str(hx+1)+'/'+str(hy)]
        for i in range(4):
            mt = move_test(sqmove[i])
            if mt == True:
                return sqmove[i]
    return aimove
def com_sqr_move():
    for i in range(tsqr):
        bn = i+1
        if bn not in sqfill:
            m1 = []
            tf = []
            if bn%a == 0:
                hx = a - 1
            else:
                hx = (bn%a) - 1
            hy = int((bn-hx-1)/a)
            m1.append('rh'+str(hx)+'/'+str(hy))
            m1.append('rv'+str(hx)+'/'+str(hy))
            m1.append('rh'+str(hx)+'/'+str(hy+1))
            m1.append('rv'+str(hx+1)+'/'+str(hy))
            for word in m1:
                tf.append(move_test(word))
            vd = tf.count(False)
            if vd == 3:
                index = tf.index(True)
                return(m1[index])
            else:
                pass
def rend_move():
    rentyp = randint(0,10)
    if rentyp%2 == 0:
        typ = 'rh'
        rendx = randint(0,a-1)
        rendy = randint(0,b)
    else:
        typ = 'rv'
        rendx = randint(0,a)
        rendy = randint(0,b-1)
    return(typ,rendx,rendy)
def smart_move(typ,x,y,cnt,cnt2):
    snks = []
    if cnt > 1000 and cnt < 1002:
        snks = mk_snk()
        return(snks)
    else:
        m1 = []
        tf = []
        if typ == 'rh':
            if y != 0:
                m1.append('rv'+str(x+1)+'/'+str(y-1))
                m1.append('rh'+str(x)+'/'+str(y-1))
                m1.append('rv'+str(x)+'/'+str(y-1))
            if y != b:
                m1.append('rv'+str(x)+'/'+str(y))
                m1.append('rh'+str(x)+'/'+str(y+1))
                m1.append('rv'+str(x+1)+'/'+str(y))
        elif typ == 'rv':
            if x != 0:
                m1.append('rh'+str(x-1)+'/'+str(y))
                m1.append('rv'+str(x-1)+'/'+str(y))
                m1.append('rh'+str(x-1)+'/'+str(y+1))
            if x != a:
                m1.append('rh'+str(x)+'/'+str(y+1))
                m1.append('rv'+str(x+1)+'/'+str(y))
                m1.append('rh'+str(x)+'/'+str(y))
        for word in m1:
            tf.append(move_test(word))
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
        if p == 'c' or p == 'et' or p == 'eb':
            r_dir = 'rl'
        elif p == 'er'or p == 'ctr'or p == 'cbr':
            r_dir = 'l'
        elif p == 'el'or p == 'ctl'or p == 'cbl':
            r_dir = 'r'
        else:
            pass
    elif a_div =='ud':
        if p == 'c' or p == 'er' or p == 'el':
            r_dir = 'ud'
        elif p == 'eb'or p == 'cbr'or p == 'cbl':
            r_dir = 'u'
        elif p == 'et'or p == 'ctl'or p == 'ctr':
            r_dir = 'd'
        else:
            pass
    elif a_div =='rd':
        if p == 'c' or p == 'et' or p == 'el'or p == 'ctl':
            r_dir = 'rd'
        elif p == 'eb'or p == 'cbl':
            r_dir = 'r'
        elif p == 'er'or p == 'ctr':
            r_dir = 'd'
        elif p == 'cbr':
            r_dir = ''
        else:
            pass
    elif a_div =='lu':
        if p == 'c' or p == 'eb' or p == 'er'or p == 'cbr':
            r_dir = 'lu'
        elif p == 'et'or p == 'ctr':
            r_dir = 'l'
        elif p == 'el'or p == 'cbl':
            r_dir = 'u'
        elif p == 'ctl':
            r_dir = ''
        else:
            pass
    elif a_div =='ru':
        if p == 'c' or p == 'eb' or p == 'el'or p == 'cbl':
            r_dir = 'ru'
        elif p == 'et'or p == 'ctl':
            r_dir = 'r'
        elif p == 'er'or p == 'cbr':
            r_dir = 'u'
        elif p == 'ctr':
            r_dir = ''
        else:
            pass
    elif a_div =='ld':
        if p == 'c' or p == 'et' or p == 'er'or p == 'ctr':
            r_dir = 'ld'
        elif p == 'eb'or p == 'cbr':
            r_dir = 'l'
        elif p == 'el'or p == 'ctl':
            r_dir = 'd'
        elif p == 'cbl':
            r_dir = ''
        else:
            pass
    else:
        pass
    return(r_dir)
def shift_dir():
    bns = []
    sd = []
    for i in range(tsqr):
        tf = []
        bn_dir =''
        bn = i+1
        if True: #bn not in sqfill
            if bn%a == 0:
                hx = a - 1
            else:
                hx = (bn%a) - 1
            hy = int((bn-hx-1)/a)
            sqmove = ['lh'+str(hx)+'/'+str(hy),'lv'+str(hx)+'/'+str(hy),'lh'+str(hx)+'/'+str(hy+1),'lv'+str(hx+1)+'/'+str(hy)]
            for word in sqmove:
                tf.append(move_test(word))
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
            r_dir = chk_dir(pos[bn-1],hv)
            bns.append(bn)
            sd.append(r_dir)
    return bns,sd
def mk_snk():
    asa = shift_dir()
    bx=asa[0]
    bd=asa[1]
    tsnk=[]
    def f_tsnk(x):
        for i in range(len(tsnk)):
            for j in range(len(tsnk[i])):
                if tsnk[i][j] == x:
                    return i
    for i in range(len(bx)):
        if i == 0:
            tsnk.append([bx[i]])
        if 'l' in bd[i]:
            f=f_tsnk(bx[i-1])
            if f == None:
                tsnk.append([bx[i]])
            else:
                tsnk[f].append(bx[i])
        if 'u' in bd[i]:
            f=f_tsnk(bx[i-a])
            if f == None:
                tsnk.append([bx[i]])
            else:
                tsnk[f].append(bx[i])
        if 'r' in bd[i]:
            f=f_tsnk(bx[i+1])
            if f == None:
                tsnk.append([bx[i]])
            else:
                tsnk[f].append(bx[i])
        if 'd' in bd[i]:
            f=f_tsnk(bx[i+a])
            if f == None:
                tsnk.append([bx[i]])
            else:
                tsnk[f].append(bx[i])
        if bd[i] == '':
            tsnk.append([bx[i]])
    for i in range(len(tsnk)):
        for j in range(len(tsnk[i])):
            f=f_tsnk(tsnk[i][j])
            if i != f:
                tsnk[f] = tsnk[f]+tsnk[i]
                tsnk[i] = []
                break
    for i in range(len(tsnk)):
        tsnk[i] = list(dict.fromkeys(tsnk[i]))
    tsnk = list(filter(None,tsnk))
    for i in range(len(tsnk)):
        if tsnk[i][0] in sqfill: 
            tsnk[i] = []
    tsnk.sort(key=len)
    tsnk = list(filter(None,tsnk))
    snks = tsnk
    return snks
p1s = []
ais = []
def score(who,bn):
    if who == 'p1':
        p1s.append(bn)
        
    elif who == 'ai':
        ais.append(bn)
    else:
        pass
screen.fill(((30,30,30)))
dots()
while running:
    event = pg.event.poll()
    if event.type == pg.QUIT:
        running = 0
    if player_move == True:
        mouse1 = pg.mouse.get_pressed()
        if mouse1[0] == 1:
            v = click()
            if v != None:
                mt = move_test(v)
                if mt == True:
                    mv = move('p1',v)
                    if mv !=  True:
                        player_move = False
                    else:
                        pass
                else:
                    pass
    else:
        a1 = ai()
        mv = move('ai',a1)
        if mv != True:
            player_move = True
        else:
            pass
    movelist = p1_move+ai_move
    drli(movelist)
    pg.display.flip()
    s(0.1)
    if len(movelist) == tline:
        print('GAME IS OVER')
        print('Your box : ',len(p1s),p1s,'\n','AI box :',len(ais),ais)
        if len(p1s) > len(ais):
            print('You Win \n Look at you go :)')
        elif len(p1s) < len(ais):
            print('AI Wins \nWell it only proves that i created one hack of AI :)')
        else:
            print('Draw')
            s(1000)
