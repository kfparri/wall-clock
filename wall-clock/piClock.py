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
import datetime, pygame, sys, datetime, time, requests, os, logging
from pygame.locals import *
from ClockSettings import ClockSettings
from Button import Button

logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.ERROR,
        datefmt='%m-%d-%Y %H:%M:%S')

def get_time():
    # make the api request
    url = "http://worldtimeapi.org/api/timezone/America/Chicago"
    
    logging.debug('Calling WorldTimeAPI to get the time: ' + url)
    
    response = requests.get(url)
    
    logging.debug('Call to API complete!')
    
    # useful page for this part was found here: https://docs.python.org/3/tutorial/datastructures.html#dictionaries
    #https://stackoverflow.com/questions/3682748/converting-unix-timestamp-string-to-readable-date
    data = response.json()
    dt = datetime.datetime.fromtimestamp(data['unixtime'])
    return dt
        
# global variables

app_settings = ClockSettings()

# set the current time, this is used to make the drawing more efficient
current_time = get_time()

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

current_color = colors['matrix_green']

# define some functions for changing the time the clock will be red
    
def get_all_fonts():
    logging.debug('Getting all the fonts from the system')
    fonts = []
    
    for root, dirs, files in os.walk("/usr/share/fonts/truetype"):
        for file in files:
            if file.endswith(".ttf"):
                fonts.append(file.lower())
    
    return fonts

# increase the target hour by one, if it is greater than 12 set it to 1
def increase_hour():
    global app_settings
    app_settings.red_hour = app_settings.red_hour + 1
    if app_settings.red_hour > 23:
        app_settings.red_hour = 0

# decrease the target hour by one, if the hours is less than 1 set it to 12
def decrease_hour():
    global app_settings
    app_settings.red_hour = app_settings.red_hour - 1
    if app_settings.red_hour < 0:
        app_settings.red_hour = 23

# increase the target minute by one, if it is more than 59 reset it to 0
def increase_minute():
    global app_settings
    app_settings.red_minute = app_settings.red_minute + 1
    if app_settings.red_minute > 59:
        app_settings.red_minute = 0

# decrease the target minute by one, if it is less than 0 set it to 59
def decrease_minute():
    global app_settings
    app_settings.red_minute = app_settings.red_minute - 1
    if app_settings.red_minute < 0:
        app_settings.red_minute = 59

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
    global app_settings
    
    app_settings.red_hour = (app_settings.red_hour + 12) % 24

# this function handles the logic of displaying the clock to the screen
def displayClock(display_font, screen, background, settings_button, blink, new_time):   
    # get the global time variable 
    global current_time
    global current_color

    # create a new time variable so we can compare the current time vs the last updated time
    pm = False

    # if the time has changed, update the display values
    if current_time.minute != new_time.minute:
        hour = new_time.hour
        minute = new_time.minute
    else:
        hour = current_time.hour
        minute = current_time.minute
        
    logging.debug('hour: {} minute: {}'.format(hour, minute))
    logging.debug('red_hour: {} red_minute: {}'.format(app_settings.red_hour, app_settings.red_minute))
    
    display_hour = get_display_hour(hour)
    display_minutes = get_display_minutes(minute)
        
    # create the text that will be drawn to the screen
    displayTime = display_hour + ":" + display_minutes

    # set the default color for the clock, in this case, green
    color = current_color # colors['matrix_green']
    
    logging.debug('current color to use (color from current_color): {}'.format(color))
    
    # if the current time is less than the target time, set the color to red
    if hour < app_settings.red_hour or (app_settings.red_hour < 12 and hour >= 12):
        color = colors['red']
    elif hour == app_settings.red_hour and minute < app_settings.red_minute:
        color = colors['red']
    
    logging.debug('color after checking the target time: {}'.format(color))
    
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
    
    settings_button.update(screen)
    
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
    global app_settings
    global app_settings
    
    app_settings.available_fonts = pygame.font.get_fonts()
    
    for i in range(len(app_settings.available_fonts)):
        if app_settings.available_fonts[i] == app_settings.current_font:
            if(i == len(app_settings.available_fonts) - 1):
                app_settings.current_font = app_settings.available_fonts[0]
            else:
                app_settings.current_font = app_settings.available_fonts[i + 1]
            return

# This function will handle all the code to display the settings screen.
# background -
# screen - 
# primary_display_font - The font/size to draw the major items on the screen
# secondary_display_font - The font/size to draw other items on the screen
# up - the image used for the up button
# down - the image used for the down button
# close - the image use for the close button
def display_settings(background, screen, primary_display_font, secondary_display_font, up_hour_button, up_minute_button, down_hour_button, down_minute_button, close_button, am_pm_button, text_color_button, text_font_button):    
    global current_color
    global app_settings
    
    color_button_rect_size = 80

    # first, build our text objects, these will be the focal point of all the other objects on the screen
    color = current_color
    am_pm_value = "AM"

    if app_settings.red_hour >= 12:
        am_pm_value = "PM"
 
    display_hour = get_display_hour(app_settings.red_hour)
    display_minutes = get_display_minutes(app_settings.red_minute)
    
    hour_text = primary_display_font.render(display_hour, 1, color)
    minute_text = primary_display_font.render(display_minutes, 1, color)
    am_pm_text = secondary_display_font.render(am_pm_value, 1, colors['white'])
    font_text = secondary_display_font.render(app_settings.current_font, 1, colors['white'])

    # Define some constants for positions on the screen
    HOUR_POS_X = 100
    HOUR_POS_Y = 150

    MINUTE_POS_X = 400
    MINUTE_POS_Y = HOUR_POS_Y

    UP_HOUR_BUTTON_POS_X = HOUR_POS_X + (hour_text.get_width() / 2) - (up_hour_button.image.get_width() / 2)
    UP_HOUR_BUTTON_POS_Y = HOUR_POS_Y - up_hour_button.image.get_height() 

    UP_MINUTE_BUTTON_POS_X = MINUTE_POS_X + (minute_text.get_width() / 2) - (up_hour_button.image.get_width() / 2)
    UP_MINUTE_BUTTON_POS_Y = UP_HOUR_BUTTON_POS_Y

    DOWN_HOUR_BUTTON_POS_X = UP_HOUR_BUTTON_POS_X 
    DOWN_HOUR_BUTTON_POS_Y = HOUR_POS_Y + hour_text.get_height() - 20

    DOWN_MINUTE_BUTTON_POS_X = UP_MINUTE_BUTTON_POS_X
    DOWN_MINUTE_BUTTON_POS_Y = DOWN_HOUR_BUTTON_POS_Y

    AM_PM_POS_X = 650
    AM_PM_POS_Y = HOUR_POS_Y
    
    AM_PM_BUTTON_POS_X = AM_PM_POS_X - 4
    AM_PM_BUTTON_POS_Y = AM_PM_POS_Y - 4

    COLOR_CHANGE_BUTTON_X = 0
    COLOR_CHANGE_BUTTON_Y = SCREEN_HEIGHT - color_button_rect_size

    hour_loc = (HOUR_POS_X, HOUR_POS_Y) 
    
    minute_loc = (MINUTE_POS_X, MINUTE_POS_Y)

    am_pm_loc = (AM_PM_POS_X, AM_PM_POS_Y)
    
    font_text_loc = (0, 0)

    up_hour_button.x = UP_HOUR_BUTTON_POS_X 
    up_hour_button.y = UP_HOUR_BUTTON_POS_Y 

    up_minute_button.x = UP_MINUTE_BUTTON_POS_X 
    up_minute_button.y = UP_MINUTE_BUTTON_POS_Y 

    down_hour_button.x = DOWN_HOUR_BUTTON_POS_X
    down_hour_button.y = DOWN_HOUR_BUTTON_POS_Y

    down_minute_button.x = DOWN_MINUTE_BUTTON_POS_X 
    down_minute_button.y = DOWN_MINUTE_BUTTON_POS_Y
    
    am_pm_button.x = AM_PM_BUTTON_POS_X
    am_pm_button.y = AM_PM_BUTTON_POS_Y
    am_pm_button.rect.height = am_pm_text.get_height() + 4
    am_pm_button.rect.width = am_pm_text.get_width() + 4
    
    #Color change rect
    text_color_button.x = COLOR_CHANGE_BUTTON_X
    text_color_button.y = COLOR_CHANGE_BUTTON_Y
    text_color_button.rect.width = color_button_rect_size
    text_color_button.rect.height = color_button_rect_size
    
    # Font text rect
    text_font_button.x = 0
    text_font_button.y = 0
    text_font_button.rect.width = font_text.get_width() + 4
    text_font_button.rect.height = font_text.get_height() + 4

    # first blank the screen to make sure we don't have any stray artifacts
    screen.blit(background, (0,0))
    
    am_pm_button.update(screen, colors['button_blue'])
    text_color_button.update(screen, current_color)
    text_font_button.update(screen, colors['button_blue'])
   
    up_hour_button.update(screen)
    up_minute_button.update(screen)
    down_hour_button.update(screen)
    down_minute_button.update(screen)
    close_button.update(screen)
    screen.blit(hour_text, hour_loc)
    screen.blit(minute_text, minute_loc)
    screen.blit(am_pm_text, am_pm_loc)
    screen.blit(font_text, font_text_loc)

    # flip the buffers to display the screen
    pygame.display.flip()

def main():
    pygame.init()

    app_settings.available_fonts = get_all_fonts()
    
    web_api_max_wait = 50000

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
    app_settings.show_settings = False

    # get the current clock ticks
    last_ticks = pygame.time.get_ticks()
    last_ticks_web_call = pygame.time.get_ticks()

    settings_button = Button(SETTINGS, 0, 0)
    up_hour_button = Button(UP, 0, 0)
    up_minute_button = Button(UP, 0, 0)
    down_hour_button = Button(DOWN, 0, 0)
    down_minute_button = Button(DOWN, 0, 0)
    close_button = Button(CLOSE, SCREEN_WIDTH - CLOSE.get_width(), SCREEN_HEIGHT - CLOSE.get_height())
    am_pm_button = Button(None, 0, 0, am_pm_rect, current_color)
    text_color_button = Button(None, 0, 0, text_color_rect, current_color)
    text_font_button = Button(None, 0, 0, text_font_rect, current_color)

    # main loop
    while 1:
        # load the text font
        TEXT_FONT = pygame.font.SysFont(app_settings.current_font, app_settings.primary_font_size)
        SECONDARY_TEXT_FONT = pygame.font.SysFont(app_settings.current_font, app_settings.secondary_font_size)

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
                if app_settings.show_settings:
                    if up_hour_button.collides_with(x,y):
                        increase_hour()
                    if down_hour_button.collides_with(x,y):
                        decrease_hour()
                    if up_minute_button.collides_with(x,y):
                        increase_minute()
                    if down_minute_button.collides_with(x,y):
                        decrease_minute()
                    if close_button.collides_with(x,y):
                        app_settings.show_settings = False     
                    if am_pm_button.collides_with(x,y):
                        change_am_pm()
                    if text_color_button.collides_with(x,y):
                        rotate_current_color()
                    if text_font_button.collides_with(x,y):
                        rotate_current_font()
                        
                # if the user clicked the settings button, set show settings to true, this will update the screen to 
                #  show the settings window
                if settings_button.collides_with(x,y): #SETTINGS.get_rect().collidepoint(x,y):
                    app_settings.show_settings = True
                
                

        # if I click the button, the screen will stop updating
        if not app_settings.show_settings:      
            #dt = datetime.datetime(2011, 11, 4, 23, 35)  
            if(pygame.time.get_ticks() - last_ticks_web_call > web_api_max_wait):
                last_ticks_web_call = pygame.time.get_ticks()
                print('Getting the time')
                dt = get_time()
                print('Done getting the time')
            
            displayClock(TEXT_FONT, screen, background, settings_button, blink, dt)
        else:
            display_settings(background, screen, TEXT_FONT, SECONDARY_TEXT_FONT, up_hour_button, up_minute_button, down_hour_button, down_minute_button, close_button, am_pm_button, text_color_button, text_font_button) # UP, DOWN, CLOSE)

        # using the clock ticks to determine how fast to blink the colon
        if pygame.time.get_ticks() - last_ticks > 700:
            blink = not blink
            last_ticks = pygame.time.get_ticks()

        time.sleep(0.05)

# main function
if __name__ == '__main__': main()
