
# Aniworld Scraper

Scraper for the Anime Hoster Aniworld. 

This tool will download all Seasons and Episodes of an anime from Aniworld.to

How to use:
* Clone the Repo
* pip install requirements.txt
* Change anime_name in start_app to your anime name (Format -> see URL of the anime)
* INFO: GUtils is a self writen library. I used it here as a Logging handler. If you don't trust me remove all logger.X
and replace them with print. 
* If you now start the start_app.py a small Chrome window will open everytime it finds an Episode. This is for the Google Captcha!
* If the Captcha appears please solve it. If you close the window you have to restart the application.

## Overrides
* season_override: Specify which season to Download. 0 is the Default and will download all Seasons.
* ddos_protection_calc: How many episodes to download before waiting 60 seconds. Default 5.

## Feedback
* Discord: ZKWolf#1926 
* Mail: zkwolf@zkwolf.com


## Support
Please create a Issue.

## Special Thanks:
Thank you to @Michtdu for the workaround and code for the Captcha!
