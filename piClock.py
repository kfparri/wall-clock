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
from Tkinter import *

# global variables
red_hour = 6
red_minute = 0

# I'm having some issues re-opening the root window after it has been
#   closed.  This is because TK does not want you to run the mainloop
#   more than once.  I have found an interesting web page here:
#   http://grapevine.com.au/~wisteria/tkfront/pygame_tkinter.html
#   that shows a different way to show the window.  I need to check
#   this out.
root = Tk()
root.geometry('200x200')
    
var_hour = StringVar()
var_minute = StringVar()

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

def define_window():
    var_hour.set(red_hour)
    var_minute.set(red_minute)

    hour_up = Button(root, text="up", command=increase_hour)
    hour_down = Button(root, text="down", command=decrease_hour)
    minute_up = Button(root, text="up", command=increase_minute)
    minute_down = Button(root, text="down", command=decrease_minute)

    hour_lbl = Label(root, textvariable=var_hour)
    minute_lbl = Label(root, textvariable=var_minute)
    lblhour = Label(root, text="Hour")
    lblmin = Label(root, text="Minute")

    hour_up.grid(row=0, column=1)
    minute_up.grid(row=0, column=3)

    lblhour.grid(row=1, column=0)
    hour_lbl.grid(row=1, column=1)
    lblmin.grid(row=1, column=2)
    minute_lbl.grid(row=1, column=3)


    hour_down.grid(row=2, column=1)
    minute_down.grid(row=2, column=3)

def main():
    pygame.init()

    # text
    TEXT_FONT = pygame.font.Font('freesansbold.ttf', 200)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Clock')

    background = pygame.Surface(screen.get_size())
    background = background.convert()

    screen.blit(background, (0,0))
    pygame.display.update()
    
    time = datetime.datetime.now()
    updateTime = True
    firstRun = True
    blink = False

    # setup the tk stuff for the update window
    define_window()    

    #var_hour = StringVar()
    #var_minute = StringVar()    
    
    #redHour = 3
    #redMinute = 45
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
                    #root = Tk()
                    #define_window()
                
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
        
        text = TEXT_FONT.render(str(displayTime), 1, color)
        colonText = TEXT_FONT.render(":", 1, MATRIX_GREEN)

        screen.blit(background, (0,0))
        
        if blink:
            pygame.draw.rect(text, BLACK,
                         (text.get_width() / 2 - colonText.get_width() / 2,
                          text.get_height() /2 - colonText.get_height() / 2,
                          colonText.get_width(), colonText.get_height()))

        screen.blit(text, ((SCREEN_WIDTH / 2) - text.get_width() / 2,
                           (SCREEN_HEIGHT / 2) - text.get_height() / 2))
        pygame.display.flip()
        
        if firstRun:
            firstRun = False

        if pygame.time.get_ticks() - last_ticks > 700:
            blink = not blink
            last_ticks = pygame.time.get_ticks()

if __name__ == '__main__': main()
