hexTap
======

hexTap game source for https://play.google.com/store/apps/details?id=com.oddbitstudio.hextap
The game was made as a learning exercise in game development in general and Kivy in particular over the course of three weeks with around 90 - 100 hours invested

I you plan to run this on desktop, you will need to install Kivy, and if you encounter any issues with the options settings (though I have hacked away in main.py to make sure that the loader is ready for whatever format the platform tries to save the settings) set self.musicOption, self.soundsOption and self.hardcoreOption manually to whatever you like and delete their respective get statements in the build method together with the if statements from build and on_config_change.
