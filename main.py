import pygame
import os
import os.path
from pygame.locals import *
from login import InputBox

intro = True
display_width = 400
display_height = 400
white = (255,255,255)
green = (0,198,0)
bright_green = (0,250,0)
clock = pygame.time.Clock()

background=pygame.image.load("bg1.jpg")
background=pygame.transform.scale(background,(display_width,display_height))
background.set_alpha(150)

pygame.init()
screen1 = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Game')


screen2 = pygame.display.set_mode((400, 400))
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)

def userDetailsCheck():
    f = open("user.txt","r")
    c=0
    while True:
        con = f.read()
        c+=1
        if("" == con):
            c-=1
            break;
    if c == 0:
        return 0
    else:
        return 1

def text_objects(text, font):
    textSurface = font.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect()

def start_game(x,y,w,h,c,lstat):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen1, c,(x,y,w,h))
        if click[0] == 1:
            if lstat == 1:
                os.system('python game.py')
            else:
                print("Please Login")
    else:
        pygame.draw.rect(screen1, c,(x,y,w,h))

    smallText = pygame.font.Font("freesansbold.ttf",20)
    textSurf, textRect = text_objects("START!", smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen1.blit(textSurf, textRect)

def LogIn():
    clock = pygame.time.Clock()

    input_box1 = InputBox(150, 170, 140, 32)
    # input_boxes = [input_box1]
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == KEYDOWN:
                if event.key == K_KP_ENTER:
                    done = True
            # for box in input_boxes:
            input_box1.handle_event(event)

        # for box in input_boxes:
        input_box1.update()
        screen2.fill((255, 255, 255))
        # for box in input_boxes:
        input_box1.draw(screen2)

        username = pygame.font.Font("freesansbold.ttf",20)
        textSurf, textRect = text_objects("Username:", username)
        textRect.center = ( 90,185 )
        screen2.blit(textSurf, textRect)
        lText = pygame.font.Font("freesansbold.ttf",35)
        textSurf, textRect = text_objects("Log In", lText)
        textRect.center = ( 200,100 )
        screen2.blit(textSurf, textRect)
        displayText = pygame.font.Font("freesansbold.ttf",20)
        textSurf, textRect = text_objects("Please Press Enter to continue", displayText)
        textRect.center = ( 200,270 )
        screen2.blit(textSurf, textRect)

        pygame.display.flip()
        clock.tick(30)

    return input_box1.text


def call_mainscreen1(logstat):
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen1.fill(white)
        set = pygame.image.load('login.png')
        screen1.blit(set,(300,10))

        if userDetailsCheck() == 0:
            logFont = pygame.font.Font('freesansbold.ttf',20)
            TextSurf,TextRect = text_objects("LogIn", logFont)
            TextRect.center = (350,20)
            screen1.blit(TextSurf, TextRect)
        elif userDetailsCheck():
            logFont = pygame.font.Font('freesansbold.ttf',20)
            TextSurf,TextRect = text_objects("LogOut", logFont)
            TextRect.center = (358,20)
            screen1.blit(TextSurf, TextRect)

        # prin(TextSurf.get_width(), TextSurf.get_height())
        log_width = TextSurf.get_width()
        log_height = TextSurf.get_height()

        largeText = pygame.font.Font('freesansbold.ttf',95)
        TextSurf,TextRect = text_objects("GoMan", largeText)
        TextRect.center = ((display_width/2),120)
        screen1.blit(TextSurf, TextRect)

        mouse = pygame.mouse.get_pos()

        f=0
        if 100+200 > mouse[0] > 100 and 250+50 > mouse[1] > 250:
            start_game(100,250,200,50,bright_green,logstat);
        else:
            start_game(100,250,200,50,green,logstat);

        click = pygame.mouse.get_pressed()
        if 300+80>mouse[0]>300 and 10+30>mouse[1]>10:
                if click[0] == 1 and userDetailsCheck() == 0:
                    s = LogIn()
                    f = open("user.txt", "w+")
                    f.write("%s\n" % s)
                    f.write("%d" % 0)
                    f.close()
                    print("Logged in")
                elif click[0] == 1 and userDetailsCheck():
                    f = open("user.txt","w+")
                    f.write("")
                    f.close()
                    print("Logged Out")

        pygame.display.update()
        clock.tick(20)

	screen1.blit(background,(0,0))


if os.path.isfile("user.txt"):
        pass
else:
    f = open("user.txt","w+")
    f.write("")
    f.close()

logstat = userDetailsCheck()
call_mainscreen1(logstat)
