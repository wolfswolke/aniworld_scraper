
# Anime/Serien Scraper

Scraper for the Anime Hoster Aniworld and the Serien Hoster SerienStream

This tool will download either all Seasons and Episodes of an anime from Aniworld.to
or it will download all Seasons and Episodes of a serie from S.to

How to use:
* Clone the Repo
* `pip install requirements.txt`
* install [ffmpeg](https://ffmpeg.org)
* On Unix for easy use take the *run.sh* file and edit the desired values
* Either use arguments or edit the `src/constants.py` file
* ARGUMENTS: `main.py <TYPE> <NAME> <LANGUAGE> [SeasonOverride]`
* Change name in `src/constants.py` to your desired name (Format -> see URL of the anime or serie)
* If you now start the `main.py` a small Chrome window will open everytime it finds an Episode. This is for the Google Captcha!
* If the Captcha appears please solve it. If you close the window you have to restart the application.

## Values/Overrides
### Required:
* type_of_media: Either "serie" or "anime" so the tool uses the correspondig url
* name: Enter the anime or serie name you want to download. It has to be in the naming scheme *word-word-word*.
* language: Determine the desired language of the files. Common options are: "Deutsch", "Ger-Sub" and "English"

### Optional:
* movie: If you want to download a movie set this to True. Default is False.
* season_override: Specify which season to Download. 0 is the Default and will download all Seasons.

## Constants
* episode_override: Specify which episode to start downloading. 0 is the Default and will download all Episodes.
* ddos_protection_calc: How many episodes to download before waiting 60 seconds. Default 4.
* ddos_wait_timer: How long to wait until next download batch starts. Default 60.
* output_path: Specify the output path. Default is the current working directory/Name-Of-Series.

## Support
Please create a Issue.

## Special Thanks:
Thank you to [Michtdu](https://github.com/Michtdu) for the workaround and code for the Captcha!

Thank you [speedyconzales](https://github.com/speedyconzales)  for adding S.to support
