#------------------------------------------------------------------------------------------------------
# File Name:    piClock.py
# Author:       Kyle Parrish
# Date:         12/29/2017
# Description:  An application to display a clock with different colors for my daughters room.
#
# Change log:
#       2/3/2018	Initial Release
#------------------------------------------------------------------------------------------------------


# imports
import datetime, pygame, sys, datetime
import time as SysTime
from pygame.locals import *

# global variables

# The "Target Time"  While the current time is less than this time (relative, since we are using a simple 12 hour time)
#  the clock will be red (not time to wake up)

# target hour
red_hour = 6

# target minute
red_minute = 0

# this flag tells the main loop whether to display the clock or the settings
show_settings = False

# set the current time, this is used to make the drawing more efficient
time = datetime.datetime.now()

# Making these rectangles global so config "screens" can be updated in a function
up_hour_rect = pygame.Rect(0,0,0,0)
up_minute_rect = pygame.Rect(0,0,0,0)
down_hour_rect = pygame.Rect(0,0,0,0)
down_minute_rect = pygame.Rect(0,0,0,0)
close_rect = pygame.Rect(0,0,0,0)

# constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480

# colors that are used in this program
RED = (255, 0, 0)
MATRIX_GREEN = (0, 255, 21)
BLACK = (0, 0, 0)

# define some functions for changing the time the clock will be red

# increase the target hour by one, if it is greater than 12 set it to 1
def increase_hour():
    global red_hour
    red_hour = red_hour + 1
    if red_hour > 23:
        red_hour = 1

# decrease the target hour by one, if the hours is less than 1 set it to 12
def decrease_hour():
    global red_hour
    red_hour = red_hour - 1
    if red_hour < 1:
        red_hour = 23

# increase the target minute by one, if it is more than 59 reset it to 0
def increase_minute():
    global red_minute
    red_minute = red_minute + 1
    if red_minute > 59:
        red_minute = 0

# decrease the target minute by one, if it is less than 0 set it to 59
def decrease_minute():
    global red_minute
    red_minute = red_minute - 1
    if red_minute < 0:
        red_minute = 59

# this function handles the logic of displaying the clock to the screen
def displayClock(display_font, screen, background, settings, blink):   
    # get the global time variable 
    global time

    # create a new time variable so we can compare the current time vs the last updated time
    newtime = datetime.datetime.now()
    pm = False

    # if the time has changed, update the display values
    if time.minute != newtime.minute:
        hour = newtime.hour
        minute = newtime.minute
    else:
        hour = time.hour
        minute = time.minute
    
    display_hour = 0

    if hour > 12:
        display_hour = hour - 12
    else:
        display_hour = hour
        
    # create the text that will be drawn to the screen
    displayTime = str(display_hour).zfill(2) + ":" + str(minute).zfill(2)

    # set the default color for the clock, in this case, green
    color = MATRIX_GREEN
    
    # if the current time is less than the target time, set the color to red
    if hour < red_hour or (red_hour < 12 and hour >= 12):
        color = RED
    elif hour == red_hour and minute < red_minute:
        color = RED
    
    # create the text surface that we will blit to the screen
    text = display_font.render(str(displayTime), 1, color)

    # create a surface for the colon so we can use it to blank it out on the blink
    colonText = display_font.render(":", 1, MATRIX_GREEN)

    # blit the background to clear the screen
    screen.blit(background, (0,0))
    
    # if we are blinking the colon, draw a rectangle over top of the colon in the text surface 
    if blink:
        pygame.draw.rect(text, BLACK,
                        (text.get_width() / 2 - colonText.get_width() / 2,
                        text.get_height() /2 - colonText.get_height() / 2,
                        colonText.get_width(), colonText.get_height()))

    # blit the text surface to the screen
    resultRect = screen.blit(text, ((SCREEN_WIDTH / 2) - text.get_width() / 2,
                        (SCREEN_HEIGHT / 2) - text.get_height() / 2))
    
    # get the rectangle for the settings button
    imgRect = settings.get_rect()
    imgRect.x = 0
    imgRect.y = 0

    # blit the settings button to the screen
    screen.blit(settings, imgRect)

    # if the current time is in the PM display the 'pm dot'
    if hour > 12:
        pygame.draw.circle(screen, color, (resultRect.right + 10, resultRect.bottom - 50), 10)

    # flip will flip the buffer to display all the images that we've blited
    pygame.display.flip()

# This function will handle all the code to display the settings screen.
def display_settings(background, screen, display_font, up, down, close):
    # get the global rectangles.  These are global because the main loop has to have access to them
    #  to see if someone has clicked the buttons
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
    MINUTE_POS_X = 400 #HOUR_POS_X + 300
    UP_HOUR_POS_X = HOUR_POS_X + (hour_text.get_width() / 2) - (up.get_width() / 2)
    UP_BUTTON_POS_Y = TIME_POS_Y - up.get_height() 
    BUTTON_MINUTE_POS_X = MINUTE_POS_X + (minute_text.get_width() / 2) - (up.get_width() / 2)
    
    DOWN_HOUR_POS_X = UP_HOUR_POS_X 
    DOWN_BUTTON_POS_Y = TIME_POS_Y + hour_text.get_height() - 20

    CLOSE_BUTTON_X = SCREEN_WIDTH - close.get_width()
    CLOSE_BUTTON_Y = SCREEN_HEIGHT - close.get_height()

    hour_loc = (HOUR_POS_X, TIME_POS_Y) 
    
    minute_loc = (MINUTE_POS_X, TIME_POS_Y)

    # Now setup the images
    # up and down arrows
    up_hour_rect = up.get_rect()
    up_hour_rect.x = UP_HOUR_POS_X 
    up_hour_rect.y = UP_BUTTON_POS_Y 

    up_minute_rect = up.get_rect()
    up_minute_rect.x = BUTTON_MINUTE_POS_X 
    up_minute_rect.y = UP_BUTTON_POS_Y 

    down_hour_rect = down.get_rect()
    down_hour_rect.x = DOWN_HOUR_POS_X
    down_hour_rect.y = DOWN_BUTTON_POS_Y

    down_minute_rect = down.get_rect()
    down_minute_rect.x = BUTTON_MINUTE_POS_X
    down_minute_rect.y = DOWN_BUTTON_POS_Y

    # close button image
    close_rect = close.get_rect()
    close_rect.x = CLOSE_BUTTON_X
    close_rect.y = CLOSE_BUTTON_Y

    # first blank the screen to make sure we don't have any stray artifacts
    screen.blit(background, (0,0))

    # blit all the buttons and the text
    screen.blit(up, up_hour_rect)
    screen.blit(up, up_minute_rect)
    screen.blit(down, down_hour_rect)
    screen.blit(down, down_minute_rect)
    screen.blit(close, close_rect)
    screen.blit(hour_text, hour_loc)
    screen.blit(minute_text, minute_loc)

    # flip the buffers to display the screen
    pygame.display.flip()

def main():
    pygame.init()

    # load the text font
    TEXT_FONT = pygame.font.Font('freesansbold.ttf', 200)

    # load the images into constants for use in the functions
    IMG = pygame.image.load("settings.png")
    UP = pygame.image.load("up.png")
    DOWN = pygame.image.load("down.png")
    CLOSE = pygame.image.load("close.png")

    # create the display with the defined size and make it full screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    # this is for developing locally on my laptop.
    #screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # create the surface for the background and create it
    background = pygame.Surface(screen.get_size())
    background = background.convert()

    # blit the background to clear it out
    screen.blit(background, (0,0))

    # update the display
    pygame.display.update()
    
    # set the start state for the blink flag
    blink = False    

    # we don't want to start the clock in the settings window
    show_settings = False

    # get the current clock ticks
    last_ticks = pygame.time.get_ticks()
    
    # main loop
    while 1:
        # event loop
        for event in pygame.event.get():
            # check for quit events (close windows)
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                return
            # if the user presses the escape key, we will also exit
            elif event.type == KEYDOWN:
                keys = pygame.key.get_pressed()
                
                if keys[K_ESCAPE]:
                    pygame.quit()
                    sys.exit()
            # the other event we are looking for is mouse clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # get the mouse position x and y values
                x, y = event.pos                

                # if the user clicked the settings button, set show settings to true, this will update the screen to 
                #  show the settings window
                if IMG.get_rect().collidepoint(x,y):
                    show_settings = True
                
                # only check these events if we are on the settings screen (these buttons don't exist on the main window)
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

        # using the clock ticks to determine how fast to blink the colon
        if pygame.time.get_ticks() - last_ticks > 700:
            blink = not blink
            last_ticks = pygame.time.get_ticks()
    
        SysTime.sleep(0.05)

# main function
if __name__ == '__main__': main()
