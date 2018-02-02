#------------------------------------------------------------------------------------------------------
# File Name:    piClock.py
# Author:       Kyle Parrish
# Date:         12/29/2017
# Description:  An application to display a clock with different colors for my daughters room.
#
# Change log:
#       12.29.2017	Initial Release
#------------------------------------------------------------------------------------------------------


# imports
import datetime, pygame, sys, datetime
from pygame.locals import *

# global variables
red_hour = 6
red_minute = 0
show_settings = False

# constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# colors
RED = (255, 0, 0)
MATRIX_GREEN = (0, 255, 21)
BLACK = (0, 0, 0)

# define some functions for the GUI frame to use
def increase_hour():
    global red_hour
    global var_hour
    red_hour = int(var_hour.get()) + 1
    if red_hour > 12:
        red_hour = 1
    var_hour.set(red_hour)

def decrease_hour():
    global red_hour
    global var_hour
    red_hour = int(var_hour.get()) - 1
    if red_hour < 1:
        red_hour = 12
    var_hour.set(red_hour)

def increase_minute():
    global red_minute
    global var_minute
    red_minute = int(var_minute.get()) + 1
    if red_minute > 59:
        red_minute = 0
    var_minute.set(red_minute)

def decrease_minute():
    global red_minute
    global var_minute
    red_minute = int(var_minute.get()) - 1
    if red_minute < 0:
        red_minute = 59
    var_minute.set(red_minute)

def displayClock(display_font, screen, background, settings, blink):    
    time = datetime.datetime.now()
    newtime = datetime.datetime.now()
        
    if time.minute != newtime.minute:
        if newtime.hour > 12:
            hour = newtime.hour - 12
        else:
            hour = newtime.hour

        minute = newtime.minute
    else:
        if time.hour > 12:
            hour = time.hour - 12
        else:
            hour = time.hour
        minute = time.minute
        
    displayTime = str(hour).zfill(2) + ":" + str(minute).zfill(2)

    color = MATRIX_GREEN
    
    if hour < red_hour:
        color = RED
    elif hour == red_hour and minute < red_minute:
        color = RED
    
    text = display_font.render(str(displayTime), 1, color)
    colonText = display_font.render(":", 1, MATRIX_GREEN)

    screen.blit(background, (0,0))
    
    if blink:
        pygame.draw.rect(text, BLACK,
                        (text.get_width() / 2 - colonText.get_width() / 2,
                        text.get_height() /2 - colonText.get_height() / 2,
                        colonText.get_width(), colonText.get_height()))

    screen.blit(text, ((SCREEN_WIDTH / 2) - text.get_width() / 2,
                        (SCREEN_HEIGHT / 2) - text.get_height() / 2))
    
    imgRect = settings.get_rect()
    imgRect.x = 0
    imgRect.y = 0

    screen.blit(settings, imgRect)

    pygame.display.flip()

def display_settings(background, screen, display_font):
    color = MATRIX_GREEN

    up = pygame.image.load("up.png")
    down = pygame.image.load("down.png")

    hour_text = display_font.render(str(red_hour), 1, color)
    hour_loc = (100, 100)

    minute_text = display_font.render(str(red_minute), 1, color)
    minute_loc = (400, 100)

    screen.blit(background, (0,0))

    screen.blit(hour_text, hour_loc)
    screen.blit(minute_text, minute_loc)

    pygame.display.flip()


def main():
    pygame.init()

    # text
    TEXT_FONT = pygame.font.Font('freesansbold.ttf', 200)

    IMG = pygame.image.load("settings.png")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Clock')

    background = pygame.Surface(screen.get_size())
    background = background.convert()

    screen.blit(background, (0,0))
    pygame.display.update()
    
    #time = datetime.datetime.now()
    firstRun = True
    blink = False    
    show_settings = False

    last_ticks = pygame.time.get_ticks()
    
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                return
            elif event.type == KEYDOWN:
                keys = pygame.key.get_pressed()
                
                if keys[K_ESCAPE]:
                    pygame.quit()
                    sys.exit()
                if keys[K_LCTRL]:
                    root.mainloop()
                    print "after main loop"
                    print red_hour
                    print red_minute
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if IMG.get_rect().collidepoint(x,y):
                    print "button Clicked"
                    show_settings = True

        # if I click the button, the screen will stop updating
        if not show_settings:        
            displayClock(TEXT_FONT, screen, background, IMG, blink)
        else:
            display_settings(background, screen, TEXT_FONT)

        if firstRun:
            firstRun = False

        if pygame.time.get_ticks() - last_ticks > 700:
            blink = not blink
            last_ticks = pygame.time.get_ticks()

if __name__ == '__main__': main()
