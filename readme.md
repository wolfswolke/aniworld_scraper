
# Anime/Serien Scraper

Scraper for the Anime Hoster Aniworld and the Serien Hoster SerienStream

This tool will download either all Seasons and Episodes of an anime from Aniworld.to
or it will download all Seasons and Episodes of a serie from S.to

How to use:
* Clone the Repo
* pip install requirements.txt
* For easy use take the *run.sh* file and edit the desired values
* Either use arguments or edit the start_app.py file
* ARGUMENTS: .\start_app.py *TYPE* *NAME* [SeasonOverride]
* Change name in start_app.py to your desired name (Format -> see URL of the anime or serie)
* INFO: zk_tools is a self writen library. I used it here as a Logging handler. If you don't trust me remove all logger.X
and replace them with print. 
* If you now start the start_app.py a small Chrome window will open everytime it finds an Episode. This is for the Google Captcha!
* If the Captcha appears please solve it. If you close the window you have to restart the application.

## Values/Overrides
* name: Enter the anime or serie name you want to download. It has to be in the naming scheme *word-word-word*.
* type: Either "serie" or "anime" so the tool uses the correspondig url
* season_override: Specify which season to Download. 0 is the Default and will download all Seasons.
* ddos_protection_calc: How many episodes to download before waiting 60 seconds. Default 4.
* ddos_wait_timer: How long to wait until next download batch starts. Default 60.
* ddos_start_value: No need to change this. This is just the Start Value for the DDOS wait loop.
* episode_interval_timer: Sets a timer and waits a short time in between downloading the files

## Support
Please create a Issue.

## Special Thanks:
Thank you to @Michtdu for the workaround and code for the Captcha!
