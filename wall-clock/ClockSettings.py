class ClockSettings:
    "This class holds all the settings for the clock"
    
    def __init__(self):
        # this flag tells the main loop whether to display the clock or the settings
        self.show_settings = False
        
        # The "Target Time"  While the current time is less than this 
        #  time the clock will be red (not time to wake up) this is
        #  stored has hour and minute
        self.red_hour = 7
        self.red_minute = 0
        self.available_fonts = []
        self.primary_font_size = 200
        self.secondary_font_size = 50
        
        # The current font used by the system
        self.current_font = "freesans" 
