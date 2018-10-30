import pygame, sys
from pygame.locals import *
import pickle
import select
import socket
import random
import time

WIDTH = 800
HEIGHT = 500
BUFFERSIZE = 40480000
flag=0
pygame.init()
black=Color(0,0,0)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((0,255,0))
haxa=0
gameDisplay = pygame.display.set_mode((WIDTH,HEIGHT))

























#pygame.draw.rect(screen, black, [75, 100, 350, 200], 2)
pygame.display.set_caption('Game')

clock = pygame.time.Clock()
background=pygame.image.load("bg4.png")
background=pygame.transform.scale(background,(WIDTH,HEIGHT))
background.set_alpha(150)

sprite1 = pygame.image.load('1.png')
sprite2 = pygame.image.load('1.png')
sprite3 = pygame.image.load('3.png')
sprite4 = pygame.image.load('3.png')
wakka=sprite1.get_width()
serverAddr = '192.168.43.250'
if len(sys.argv) == 2:
  serverAddr = sys.argv[1]
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((serverAddr, 4321))

playerid = 0

sprites = { 0: sprite1, 1: sprite2, 2: sprite3, 3: sprite4 }


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()




def message_display(text):
    text=str(text)
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((WIDTH/2),(HEIGHT/2))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()

i=5
while i>0:

    print(i)
    message_display(i)
    time.sleep(1)
    screen.fill((255,255,255))
    screen.blit(background,(0,0))
    i=i-1








##############################################




##############################################


def crash():
    message_display('youcrashed')
    haxa=1






class Minion:
  def __init__(self, x, y, id):
    self.x = x
    self.y = y
    self.vx = 0
    self.vy = 0
    self.id = id

  def update(self):
    self.x += self.vx
    self.y += self.vy

    if self.x > WIDTH - 50:
      self.x = WIDTH - 50
    if self.x < 0:
      self.x = 0
    if self.y > HEIGHT - 50:
      self.y = HEIGHT - 50
    if self.y < 0:
      self.y = 0

    if self.id == 0:
      self.id = playerid

  def render(self):
    screen.blit(sprites[self.id % 4], (self.x, self.y))





class GameEvent:





  def __init__(self, vx, vy):
    self.vx = vx
    self.vy = vy


cc = Minion(50,450, 0)

minions = []

thing_startx=500
thing_starty=500
thing_speed=2
thing_width=100
thing_height=100
x=random.randrange(0,800)
j=10;
t=75
t1=75
BLACK=Color((random.randrange(1,254)),(random.randrange(1,254)),(random.randrange(1,254)))
xx=random.randrange(0,800)
J=10
T=75
T1=75
while True:
  #pygame.draw.rect(screen,black,[thing_startx,thing_starty,thing_width,thing_height])
  ins, outs, ex = select.select([s], [], [], 0)
  for inm in ins:
    thing_starty+=thing_speed
    j=j+12
    J=J+6








    pygame.draw.rect(screen,black, [x, j, t, t1])

    pygame.draw.rect(screen,BLACK, [xx, J, T, T1])

    if j>500:
        j=0-200
        x=random.randrange(0,700)
        t=random.randrange(40,150)
        t1=random.randrange(40,150)
    if J>500:

        J=0-200

        xx=random.randrange(0,700)
        T=random.randrange(40,150)
        T1=random.randrange(40,150)
	BLACK=Color((random.randrange(1,254)),(random.randrange(1,254)),(random.randrange(1,254)))

        black=Color((random.randrange(1,254)),(random.randrange(1,254)),(random.randrange(1,254)))
    #print("hola")

    if cc.y<j+t1:
        #print("y crossover")

        if cc.x>x and cc.x<x+t or cc.x+wakka >x  and cc.x+wakka<x+t:
            print('crossover')
            flag=1
            crash()
            j=0-200
            s.send(pickle.dumps('died'))
            #time.sleep(2)
            s.close()

    if cc.y<J+T1:
        #print("y crossover")

        if cc.x>xx and cc.x<xx+T or cc.x+wakka >xx  and cc.x+wakka<xx+T:
            print('crossover')
            flag=1
            crash()
            j=0-200
            s.send(pickle.dumps('died'))
            #time.sleep(2)
            s.close()





    gameEvent = pickle.loads(s.recv(BUFFERSIZE))
    print(gameEvent)
    if(gameEvent[0]=='victory'):
            print("jai babe ri")
            if(flag==0):
                message_display('you Won')
                time.sleep(5)
            s.close()


    else:
            if gameEvent[0] == 'id update':
              playerid = gameEvent[1]
              print(playerid)
            if gameEvent[0] == 'player locations':
              gameEvent.pop(0)
              minions = []
              for minion in gameEvent:
                if minion[0] != playerid:
                  minions.append(Minion(minion[1], minion[2], minion[0]))












  for event in pygame.event.get():

    #cc.things(thing_startx,thing_starty,thing_width,thing_height,black)
    if event.type == QUIT:
    	pygame.quit()
    	sys.exit()
    if event.type == KEYDOWN:
      if event.key == K_LEFT: cc.vx = -10
      if event.key == K_RIGHT: cc.vx = 10
      #if event.key == K_UP: cc.vy = -10
      #if event.key == K_DOWN: cc.vy = 10
    if event.type == KEYUP:
      if event.key == K_LEFT and cc.vx == -10: cc.vx = 0
      if event.key == K_RIGHT and cc.vx == 10: cc.vx = 0
      #if event.key == K_UP and cc.vy == -10: cc.vy = 0
      #if event.key == K_DOWN and cc.vy == 10: cc.vy = 0

  clock.tick(60)
  #pygame.draw.rect(screen,black,[thing_startx,thing_starty,thing_width,thing_height])


  cc.update()

  for m in minions:
    m.render()

  cc.render()

  pygame.display.flip()

  ge = ['position update', playerid, cc.x, cc.y]

  s.send(pickle.dumps(ge))
  screen.fill((255,255,255))
  screen.blit(background,(0,0))
s.close()
