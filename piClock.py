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
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480

# colors
RED = (255, 0, 0)
MATRIX_GREEN = (0, 255, 21)
BLACK = (0, 0, 0)

up_hour_rect = pygame.Rect(0,0,0,0)
up_minute_rect = pygame.Rect(0,0,0,0)
down_hour_rect = pygame.Rect(0,0,0,0)
down_minute_rect = pygame.Rect(0,0,0,0)
close_rect = pygame.Rect(0,0,0,0)

# define some functions for the GUI frame to use
def increase_hour():
    global red_hour
    red_hour = red_hour + 1
    if red_hour > 12:
        red_hour = 1

def decrease_hour():
    global red_hour
    red_hour = red_hour - 1
    if red_hour < 1:
        red_hour = 12

def increase_minute():
    global red_minute
    red_minute = red_minute + 1
    if red_minute > 59:
        red_minute = 0

def decrease_minute():
    global red_minute
    red_minute = red_minute - 1
    if red_minute < 0:
        red_minute = 59

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

def display_settings(background, screen, display_font, up, down, close):
    global up_hour_rect
    global up_minute_rect
    global down_hour_rect
    global down_minute_rect
    global close_rect
    # first, build our text objects, these will be the focal point of all the other objects on the screen
    color = MATRIX_GREEN
    hour_text = display_font.render(str(red_hour), 1, color)
    minute_text = display_font.render(str(red_minute), 1, color)

    # Define some constants for positions on the screen
    HOUR_POS_X = 100
    TIME_POS_Y = 150
    MINUTE_POS_X = HOUR_POS_X + 300 # 350
    UP_HOUR_POS_X = HOUR_POS_X + (hour_text.get_width() / 2) - (up.get_width() / 2)
    UP_BUTTON_POS_Y = TIME_POS_Y - up.get_height() # - 10
    BUTTON_MINUTE_POS_X = MINUTE_POS_X + (minute_text.get_width() / 2) - (up.get_width() / 2)
    
    DOWN_HOUR_POS_X = UP_HOUR_POS_X 
    DOWN_BUTTON_POS_Y = TIME_POS_Y + hour_text.get_height() - 20

    CLOSE_BUTTON_X = SCREEN_WIDTH - close.get_width()
    CLOSE_BUTTON_Y = SCREEN_HEIGHT - close.get_height()

    #DOWN_MINUTE_POS_X = MINUTE_POS_X + (minute_text.get_width() / 2) - (up.get_width() / 2)

    hour_loc = (HOUR_POS_X, TIME_POS_Y) # (100, 100)
    
    minute_loc = (MINUTE_POS_X, TIME_POS_Y) # (400, 100)

    # Now setup the images
    up_hour_rect = up.get_rect()
    up_hour_rect.x = UP_HOUR_POS_X #100 + (hour_text.get_width() / 2) - (up.get_width() / 2)
    up_hour_rect.y = UP_BUTTON_POS_Y # 40

    up_minute_rect = up.get_rect()
    up_minute_rect.x = BUTTON_MINUTE_POS_X # 400 + (minute_text.get_width() / 2) - (up.get_width() / 2)
    up_minute_rect.y = UP_BUTTON_POS_Y # 40

    down_hour_rect = down.get_rect()
    down_hour_rect.x = DOWN_HOUR_POS_X
    down_hour_rect.y = DOWN_BUTTON_POS_Y

    down_minute_rect = down.get_rect()
    down_minute_rect.x = BUTTON_MINUTE_POS_X
    down_minute_rect.y = DOWN_BUTTON_POS_Y

    close_rect = close.get_rect()
    close_rect.x = CLOSE_BUTTON_X
    close_rect.y = CLOSE_BUTTON_Y

    #down = pygame.image.load("down.png")
    #close = pygame.image.load("close.png")

    screen.blit(background, (0,0))

    screen.blit(up, up_hour_rect)
    screen.blit(up, up_minute_rect)
    screen.blit(down, down_hour_rect)
    screen.blit(down, down_minute_rect)
    screen.blit(close, close_rect)
    screen.blit(hour_text, hour_loc)
    screen.blit(minute_text, minute_loc)

    pygame.display.flip()

def main():
    pygame.init()

    # text
    TEXT_FONT = pygame.font.Font('freesansbold.ttf', 200)

    IMG = pygame.image.load("settings.png")
    UP = pygame.image.load("up.png")
    DOWN = pygame.image.load("down.png")
    CLOSE = pygame.image.load("close.png")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    #pygame.mouse.set_visible(False)
    #pygame.display.set_caption('Clock')

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
                    print "settings button Clicked"
                    show_settings = True
                if show_settings:
                    if up_hour_rect.collidepoint(x,y):
                        increase_hour()
                    if down_hour_rect.collidepoint(x,y):
                        decrease_hour()
                    if up_minute_rect.collidepoint(x,y):
                        increase_minute()
                    if down_minute_rect.collidepoint(x,y):
                        decrease_minute()
                    if close_rect.collidepoint(x,y):
                        show_settings = False          

        # if I click the button, the screen will stop updating
        if not show_settings:        
            displayClock(TEXT_FONT, screen, background, IMG, blink)
        else:
            display_settings(background, screen, TEXT_FONT, UP, DOWN, CLOSE)

        if firstRun:
            firstRun = False

        if pygame.time.get_ticks() - last_ticks > 700:
            blink = not blink
            last_ticks = pygame.time.get_ticks()

if __name__ == '__main__': main()
