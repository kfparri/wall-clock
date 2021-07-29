#------------------------------------------------------------------------------------------------------
# File Name:    piClock.py
# Author:       Kyle Parrish
# Date:         12/29/2017
# Description:  An application to display a clock with different colors for my daughters room.
#
# Change log:
#       2/3/2018	Initial Release
#       7.21.2021   Updated default red hour to 7 instead of 6 (kids still wake up too early)
#                   Started updating settings screen to show 12 hour clock (w/ AM/PM)
#       7.23.2021   Finished updating the settings page and added the api functionality so the 
#                   clock is now syncing to worldtimeapi.org to get its time
#------------------------------------------------------------------------------------------------------

## NOTES I found this link that has a couple of functions to export the json to an object
## https:stackoverflow.com/questions/6578986/how-to-convert-json-data-into-a-python-object

# imports
import datetime, pygame, sys, datetime, time, requests, os
from pygame.locals import *

def get_time():
    # make the api request
    response = requests.get("http://worldtimeapi.org/api/timezone/America/Chicago")
    # useful page for this part was found here: https://docs.python.org/3/tutorial/datastructures.html#dictionaries
    #https://stackoverflow.com/questions/3682748/converting-unix-timestamp-string-to-readable-date
    data = response.json()
    dt = datetime.datetime.fromtimestamp(data['unixtime'])
    return dt
    
# global variables

# The "Target Time"  While the current time is less than this time (relative, since we are using a simple 12 hour time)
#  the clock will be red (not time to wake up)

# target hour
red_hour = 7

# target minute
red_minute = 0

# this flag tells the main loop whether to display the clock or the settings
show_settings = False

# set the current time, this is used to make the drawing more efficient
current_time = get_time()

### NEW 
# The current font used by the system
current_font = "freesans" #"freesansbold.ttf"

available_fonts = []

# The primary text font size
primary_font_size = 200

# the secondary text font size
secondary_font_size = 50
###

# Making these rectangles global so config "screens" can be updated in a function
#  while allowing the mail loop to check for collisions (aka 'click events') directly
up_hour_rect = pygame.Rect(0,0,0,0)
up_minute_rect = pygame.Rect(0,0,0,0)
down_hour_rect = pygame.Rect(0,0,0,0)
down_minute_rect = pygame.Rect(0,0,0,0)
close_rect = pygame.Rect(0,0,0,0)
am_pm_rect = pygame.Rect(0,0,0,0)
text_color_rect = pygame.Rect(0,0,0,0)
text_font_rect = pygame.Rect(0,0,0,0)

# constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480

# colors that are used in this program
colors = {}
colors['red'] = (255, 0, 0)
colors['matrix_green'] = (0, 255, 21)
colors['black'] = (0, 0, 0)
colors['button_blue'] = (51, 122, 183)
colors['white'] = (255, 255, 255)

current_color = colors['button_blue']

# define some functions for changing the time the clock will be red

def get_all_fonts():
    fonts = []
    
    for root, dirs, files in os.walk("/usr/share/fonts/truetype"):
        for file in files:
            if file.endswith(".ttf"):
                fonts.append(file.lower())
    
    return fonts

# increase the target hour by one, if it is greater than 12 set it to 1
def increase_hour():
    global red_hour
    red_hour = red_hour + 1
    if red_hour > 23:
        red_hour = 0

# decrease the target hour by one, if the hours is less than 1 set it to 12
def decrease_hour():
    global red_hour
    red_hour = red_hour - 1
    if red_hour < 0:
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

# Convert the military time hour to 12 hour time with 0 padding
def get_display_hour(hour):
    display_hour = 0

    if hour > 12:
        display_hour = hour - 12
    else:
        display_hour = hour
    
    if hour == 0:
        display_hour = 12
        
    return str(display_hour).zfill(2)
    
# Convert the minutes to nice 0 filled string
def get_display_minutes(minutes):
    return str(minutes).zfill(2)
   
# Change the time from am to pm
def change_am_pm():
    global red_hour
    
    red_hour = (red_hour + 12) % 24

# this function handles the logic of displaying the clock to the screen
def displayClock(display_font, screen, background, settings, blink, new_time):   
    # get the global time variable 
    global current_time
    global current_color
    
    # create a new time variable so we can compare the current time vs the last updated time
    #new_time = datetime.datetime.now()
    pm = False

    # if the time has changed, update the display values
    if current_time.minute != new_time.minute:
        hour = new_time.hour
        minute = new_time.minute
    else:
        hour = current_time.hour
        minute = current_time.minute
    
    display_hour = get_display_hour(hour)
    display_minutes = get_display_minutes(minute)
        
    # create the text that will be drawn to the screen
    displayTime = display_hour + ":" + display_minutes

    # set the default color for the clock, in this case, green
    color = current_color # colors['matrix_green']
    
    # if the current time is less than the target time, set the color to red
    if hour < red_hour or (red_hour < 12 and hour >= 12):
        color = colors['red']
    elif hour == red_hour and minute < red_minute:
        color = colors['red']
    
    # create the text surface that we will blit to the screen
    text = display_font.render(str(displayTime), 1, color)

    # create a surface for the colon so we can use it to blank it out on the blink
    colonText = display_font.render(":", 1, colors['matrix_green'])

    # blit the background to clear the screen
    screen.blit(background, (0,0))
    
    # if we are blinking the colon, draw a rectangle over top of the colon in the text surface 
    if blink:
        pygame.draw.rect(text, colors['black'],
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

def rotate_current_color():
    global colors
    global current_color
    
    assign_color = False
    
    for color in colors:
        if assign_color and not color == 'black':
            current_color = colors[color]
            assign_color = False
            return
        
        if current_color == colors[color]:
            # the next color is going to be the new current color
            assign_color = True
    
    ### You need to fix this to be better!
    if assign_color:
        current_color = colors['button_blue']
        
def rotate_current_font():
    global current_font
    global available_fonts
    
    available_fonts = pygame.font.get_fonts()
    
    for i in range(len(available_fonts)):
        if available_fonts[i] == current_font:
            if(i == len(available_fonts) - 1):
                current_font = available_fonts[0]
            else:
                current_font = available_fonts[i + 1]
            return

# This function will handle all the code to display the settings screen.
# background -
# screen - 
# primary_display_font - The font/size to draw the major items on the screen
# secondary_display_font - The font/size to draw other items on the screen
# up - the image used for the up button
# down - the image used for the down button
# close - the image use for the close button
def display_settings(background, screen, primary_display_font, secondary_display_font, up, down, close):
    # get the global rectangles.  These are global because the main loop has to have access to them
    #  to see if someone has clicked the buttons
    global up_hour_rect
    global up_minute_rect
    global down_hour_rect
    global down_minute_rect
    global am_pm_rect
    global text_color_rect
    global close_rect
    global text_font_rect
    
    global current_color
    global current_font
    
    color_button_rect_size = 80

    # first, build our text objects, these will be the focal point of all the other objects on the screen
    color = current_color
    am_pm_value = "AM"

    if red_hour >= 12:
        am_pm_value = "PM"
 
    display_hour = get_display_hour(red_hour)
    display_minutes = get_display_minutes(red_minute)
    
    hour_text = primary_display_font.render(display_hour, 1, color)
    minute_text = primary_display_font.render(display_minutes, 1, color)
    am_pm_text = secondary_display_font.render(am_pm_value, 1, colors['white'])
    font_text = secondary_display_font.render(current_font, 1, colors['white'])

    # Define some constants for positions on the screen
    HOUR_POS_X = 100
    HOUR_POS_Y = 150

    MINUTE_POS_X = 400 #HOUR_POS_X + 300
    MINUTE_POS_Y = HOUR_POS_Y

    UP_HOUR_BUTTON_POS_X = HOUR_POS_X + (hour_text.get_width() / 2) - (up.get_width() / 2)
    UP_HOUR_BUTTON_POS_Y = HOUR_POS_Y - up.get_height() 

    UP_MINUTE_BUTTON_POS_X = MINUTE_POS_X + (minute_text.get_width() / 2) - (up.get_width() / 2)
    UP_MINUTE_BUTTON_POS_Y = UP_HOUR_BUTTON_POS_Y

    DOWN_HOUR_BUTTON_POS_X = UP_HOUR_BUTTON_POS_X 
    DOWN_HOUR_BUTTON_POS_Y = HOUR_POS_Y + hour_text.get_height() - 20

    DOWN_MINUTE_BUTTON_POS_X = UP_MINUTE_BUTTON_POS_X
    DOWN_MINUTE_BUTTON_POS_Y = DOWN_HOUR_BUTTON_POS_Y

    AM_PM_POS_X = 650
    AM_PM_POS_Y = HOUR_POS_Y
    
    AM_PM_BUTTON_POS_X = AM_PM_POS_X - 4
    AM_PM_BUTTON_POS_Y = AM_PM_POS_Y - 4

    CLOSE_BUTTON_X = SCREEN_WIDTH - close.get_width()
    CLOSE_BUTTON_Y = SCREEN_HEIGHT - close.get_height()
    
    COLOR_CHANGE_BUTTON_X = 0
    COLOR_CHANGE_BUTTON_Y = SCREEN_HEIGHT - color_button_rect_size

    hour_loc = (HOUR_POS_X, HOUR_POS_Y) 
    
    minute_loc = (MINUTE_POS_X, MINUTE_POS_Y)

    am_pm_loc = (AM_PM_POS_X, AM_PM_POS_Y)
    
    font_text_loc = (0, 0)

    # Now setup the images
    # up and down arrows
    up_hour_rect = up.get_rect()
    up_hour_rect.x = UP_HOUR_BUTTON_POS_X 
    up_hour_rect.y = UP_HOUR_BUTTON_POS_Y 

    up_minute_rect = up.get_rect()
    up_minute_rect.x = UP_MINUTE_BUTTON_POS_X 
    up_minute_rect.y = UP_MINUTE_BUTTON_POS_Y 

    down_hour_rect = down.get_rect()
    down_hour_rect.x = DOWN_HOUR_BUTTON_POS_X
    down_hour_rect.y = DOWN_HOUR_BUTTON_POS_Y

    down_minute_rect = down.get_rect()
    down_minute_rect.x = DOWN_MINUTE_BUTTON_POS_X 
    down_minute_rect.y = DOWN_MINUTE_BUTTON_POS_Y
    
    am_pm_rect.x = AM_PM_BUTTON_POS_X
    am_pm_rect.y = AM_PM_BUTTON_POS_Y
    am_pm_rect.height = am_pm_text.get_height() + 4
    am_pm_rect.width = am_pm_text.get_width() + 4
    
    #Color change rect
    text_color_rect.x = COLOR_CHANGE_BUTTON_X
    text_color_rect.y = COLOR_CHANGE_BUTTON_Y
    text_color_rect.width = color_button_rect_size
    text_color_rect.height = color_button_rect_size
    
    # Font text rect
    text_font_rect.x = 0
    text_font_rect.y = 0
    text_font_rect.width = font_text.get_width() + 4
    text_font_rect.height = font_text.get_height() + 4

    # close button image
    close_rect = close.get_rect()
    close_rect.x = CLOSE_BUTTON_X
    close_rect.y = CLOSE_BUTTON_Y

    # first blank the screen to make sure we don't have any stray artifacts
    screen.blit(background, (0,0))
    
    pygame.draw.rect(screen, colors['button_blue'], am_pm_rect)
    pygame.draw.rect(screen, current_color, text_color_rect)
    pygame.draw.rect(screen, colors['button_blue'], text_font_rect)

    # blit all the buttons and the text
    screen.blit(up, up_hour_rect)
    screen.blit(up, up_minute_rect)
    screen.blit(down, down_hour_rect)
    screen.blit(down, down_minute_rect)
    screen.blit(close, close_rect)
    screen.blit(hour_text, hour_loc)
    screen.blit(minute_text, minute_loc)
    screen.blit(am_pm_text, am_pm_loc)
    screen.blit(font_text, font_text_loc)

    # flip the buffers to display the screen
    pygame.display.flip()

def main():
    pygame.init()

    available_fonts = get_all_fonts()
    
    web_api_max_wait = 10000

    dt = current_time

    # load the images into constants for use in the functions
    SETTINGS = pygame.image.load("settings.png")
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
    last_ticks_web_call = pygame.time.get_ticks()
    
    # main loop
    while 1:
        # load the text font
        TEXT_FONT = pygame.font.SysFont(current_font, primary_font_size)
        SECONDARY_TEXT_FONT = pygame.font.SysFont(current_font, secondary_font_size)
        
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
                    if am_pm_rect.collidepoint(x,y):
                        change_am_pm()
                    if text_color_rect.collidepoint(x,y):
                        rotate_current_color()
                    if text_font_rect.collidepoint(x,y):
                        rotate_current_font()
                        
                # if the user clicked the settings button, set show settings to true, this will update the screen to 
                #  show the settings window
                if SETTINGS.get_rect().collidepoint(x,y):
                    show_settings = True
                
                

        # if I click the button, the screen will stop updating
        if not show_settings:      
            #dt = datetime.datetime(2011, 11, 4, 23, 35)  
            if(pygame.time.get_ticks() - last_ticks_web_call > web_api_max_wait):
                last_ticks_web_call = pygame.time.get_ticks()
                dt = get_time()
            
            displayClock(TEXT_FONT, screen, background, SETTINGS, blink, dt)
        else:
            display_settings(background, screen, TEXT_FONT, SECONDARY_TEXT_FONT, UP, DOWN, CLOSE)

        # using the clock ticks to determine how fast to blink the colon
        if pygame.time.get_ticks() - last_ticks > 700:
            blink = not blink
            last_ticks = pygame.time.get_ticks()
    
        time.sleep(0.05)

# main function
if __name__ == '__main__': main()
