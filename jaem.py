import pygame
pygame.init()
from pygame import image as img
pygame.font.init()
textfont=pygame.font.SysFont("monospace",50)

level=0
lc=0
displayw=1540
displayb=865
endr=[displayw-100,displayb]
endl=[0,displayb]
end=endr
display=pygame.display.set_mode((displayw,displayb))
pygame.display.set_caption("Test")
idle=img.load("Idle.png")
bg=pygame.image.load("bg.jpg")
runR=(pygame.image.load("Run_R1.png"),pygame.image.load("Run_R2.png"))
runL=(pygame.image.load("Run_L1.png").convert_alpha(),pygame.image.load("Run_L2.png"))
m=0
text="didnt work"
js= pygame.mixer.Sound("Jump.wav")
music=pygame.mixer.music.load('Music.mp3')
pygame.mixer.music.play(-1)
ls=pygame.mixer.Sound("level.wav")
gcount=10
x=0
y=0
width=35
height=40
wc=0
left=False
right=False
isjump=False
defo=10
jumpcount=defo
vel = 12
c=2.5
neg=1


ground=[]
log=[]
def block(x,y,w,h):
    global ground
    global log
    ground.append(((x,x+w),(y,y+h)))
    log.append((x,y,w,h))

def collidex():
    global ground
    global x
    global y
    global width
    global height
    global vel
    for i in ground:
        if y > i[1][0] and y< i[1][1]:
            if x+width+vel>=i[0][0] and x+width<=i[0][0]:
                return "r"
                break
            if x-vel<=i[0][1] and x>=i[0][1]:
                return"l"
        if y+height>i[1][0] and y+height< i[1][1]:
            if x+width+vel>=i[0][0] and x+width<=i[0][0]:
                return "r"
                break
            if x-vel<=i[0][1] and x>=i[0][1]:
                return"l"
                break
    else:
        return "n"

def collidey():
    global ground
    global x
    global y
    global width
    global height
    global gcount
    global jumpcount
    global isjump
    global c
    for i in ground:
        if x > i[0][0] and x< i[0][1]:
            if y+height+gcount**2>=i[1][0] and y+ height<=i[1][0]:
                return True
                if gcount !=1:
                    y=i[1][0]-height
                break
            if y-(jumpcount**2)*0.45*neg+height>=i[1][0] and isjump==True:
                return True
                y=i[1][0]-height
                break
            
        if x+width>i[0][0] and x+width< i[0][1]:
            if y+height+gcount**2>=i[1][0] and y+ height<=i[1][0]:
                return True
                if gcount !=1:
                    y=i[1][0]-height
                break
            if y-(jumpcount**2)*0.45*neg+height>=i[1][0] and isjump==True:
                return True
                y=i[1][0]-height
                break
    else:
        return False
def window():
    global ground
    global dtext
    global end
    display.blit(bg, (0,0))
    for i in log:
        pygame.draw.rect(display,(255,0,0),(i))
    pygame.draw.rect(display,(0,100,0),(end[0],end[1]-50,100,50))
    display.blit(dtext,(0,0))
    
    global wc
    if wc>1:
        wc=0
    if left==True and isjump==True:
        display.blit(img.load("Jump_L.png"),(x,y))
    elif right==True and isjump==True:
        display.blit(img.load("Jump_R.png"),(x,y))
    elif left==True and isjump==False:
        display.blit(runL[wc],(x,y))
    elif right==True and isjump==False:
        display.blit(runR[wc],(x,y))
    elif right== False and left ==False and isjump==True:
        display.blit(img.load("Jump_N.png"),(x,y))
    else:
        display.blit(idle,(x,y))
    pygame.display.update()


run=True
while run:
    dtext=textfont.render(text,1,(255,255,255))
    if not collidey() and isjump==False:
        y+=gcount**2
        gcount+=1
    if collidey():
        gcount=1
        jumpcount=defo
        isjump=False
    window()
    pygame.time.delay(30)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    keys=pygame.key.get_pressed()


    if keys[pygame.K_LEFT] and collidex()!="l":
                    x-=vel
                    left=True
                    right=False
                    wc+=1
    elif keys[pygame.K_RIGHT] and collidex()!="r":
                    x+=vel
                    right=True
                    left=False
                    wc+=1

    else:
        left=False
        right=False
        wc=0
    if not isjump:
        if collidey()==True:
            if keys[pygame.K_SPACE]:
                isjump=True
                gcount=1
                js.play()
                wc=0
    if isjump:
        neg=1
        if jumpcount <0:
            neg=-1
        if jumpcount>=-10:
            y-=(jumpcount**2)*neg*0.45
            jumpcount-=1
        else:
            jumpcount=10
            isjump=False
    if x>end[0] and x<end[0]+100:
        if y>=end[1]-height-5 and y<=end[1]-height+5 and m==0:
            level+=1
            lc=0
            ls.play()
            m+=1
    if x+width>end[0] and x+width<end[0]+100:
        if y>=end[1]-height-5 and y<=end[1]-height+5 and m==0:
            level+=1
            lc=0
            ls.play()
            m+=1
    if y>displayb:
        x=0
        y=height
    if level==0:
        if lc==0:
            m=0
            ground=[]
            log=[]
        block(0,0,1,displayb)
        block(0,displayb,displayw,1)
        block(displayw,0,1,displayb)
        text="Use arrow keys to move your character"
        end=endr
        lc+=1
    if level==1:
        if lc==0:
            ground=[]
            m=0
            log=[]
        block(0,0,1,displayb)
        block(0,displayb,displayw,1)
        block(displayw,0,1,displayb)
        block(700,displayb-100,300,100)
        text="Press spacebar to jump"
        end=endl
        lc+=1
    if level==2:
        if lc==0:
            ground=[]
            m=0
            log=[]
            end=endr
            end[1]=endr[1]-200
            x=0
            y=0
        text="arrow + jump"
        block(0,0,1,displayb)
        block(displayw,0,1,displayb)
        block(0,displayb-200,500,200)
        block(700,displayb-200,displayw,200)
        lc+=1
    if level==3:
        text="Reach the green section"
        if lc==0:
            ground=[]
            m=0
            log=[]
            x=0
            y=displayb-height-20
            end=(1150,displayb-520)
        block(0,0,1,displayb)
        block(displayw,0,1,displayb)
        block(0,displayb-20,100,20)
        block(150,displayb-120,40,20)
        block(300,displayb-220,40,20)
        block(450,displayb-320,40,20)
        block(600,displayb-420,40,20)
        block(750,displayb-520,500,20)
        block(endr[0],endr[1],100,20)
        lc+=1
    if level==4:
        text="Beware"
        if lc==0:
            ground=[]
            m=0
            log=[]
            x=0
            y=displayb-height-20
            end=(1300,displayb-170)
        block(0,0,1,displayb)
        block(displayw,0,1,displayb)
        block(0,displayb-20,100,20)
        block(100,displayb-170,50,20)
        block(180,displayb-170,40,20)
        block(250,displayb-170,40,20)
        block(320,displayb-170,40,20)
        block(390,displayb-170,40,20)
        block(460,displayb-170,40,20)
        block(540,displayb-170,40,20)
        block(610,displayb-170,40,20)
        block(680,displayb-170,40,20)
        block(750,displayb-170,40,20)
        block(830,displayb-170,40,20)
        block(900,displayb-170,40,20)
        block(970,displayb-170,40,20)
        block(1050,displayb-170,40,20)
        block(1120,displayb-170,40,20)
        block(1190,displayb-170,40,20)
        block(1260,displayb-170,100,20)
        block(end[0],end[1],100,20)
        lc+=1
    if level==5:
        text="You can give up here"
        if lc==0:
            ground=[]
            m=0
            log=[]
            x=0
            y=displayb-height-20
            end=endr
        block(0,0,1,displayb)
        block(displayw,0,1,displayb)
        block(0,displayb-20,100,20)
        block(150,displayb-100,50,20)
        block(250,displayb-270,50,20)
        block(350,displayb-440,50,20)
        block(350,displayb-420,10,100)
        block(400,displayb-300,110,20)
        block(650,displayb-470,50,20)
        block(850,displayb-610,50,20)
        block(920,displayb-550,50,20)
        block(1000,displayb-300,400,20)
        block(1110,displayb-720,200,20)
        block(endr[0],endr[1],100,20)
        lc+=1
    if level>=6:
        text="Thank you!"
        if lc==0:
            end=(-500,-500)
            ground=[]
            m=0
            log=[]
            x=0
            y=displayb-height-100
        block(0,0,1,displayb)
        block(0,displayb,displayw,1)
        block(displayw,0,1,displayb)
        lc+=1
pygame.quit()
