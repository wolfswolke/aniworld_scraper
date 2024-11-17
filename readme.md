# Anime/Serien Scraper

Scraper for the Anime Hoster Aniworld and the Serien Hoster SerienStream

This tool will download either all Seasons and Episodes of an anime from Aniworld.to
or it will download all Seasons and Episodes of a serie from S.to

How to use:

- Clone the Repo
- `pip install -r requirements.txt`
- download or install [ffmpeg](https://ffmpeg.org) (If you download it put it in the root folder or src folder)

- On Unix for easy use take the _run.sh_ file and edit the desired values
- On Windows for easy use take the _run.bat_ file and past the desired values in the command line

Manual usage with python:
- You can either edit the `src/constants.py` file or pass the values as arguments to the `main.py` file

Supported Arguments:
- `--type <TYPE>`: Either "serie" or "anime" to switch between websites to scrape.
- `--name <NAME>`: The name of the anime or serie you want to download.
- `--lang <LANGUAGE>`: The language you want to download. Normaly "Deutsch", "Ger-Sub", "English" or "Eng-Sub".
- `--dl-mode <DownloadMode>`: The type of content you want to download. Valid arguments are: Movies, Series, All.
- `--season-override <SeasonOverride>`: Specify which season to Download. `0` download ALL seasons, 
`NUM` download only the specified season, `NUM+` download this season and beyond.
- `--provider <ProviderOverride>`: Specify the provider to use. Valid arguments are: VOE, Streamtape and Vidoza.

## Manual download
If you get a error or only need a specific episode you can download it manually with the `Manual_download.py` script.

Run it with the same arguments as you would main.py.
- Edit the `src/constants.py` and change the `episode_override` to the desired episode.
- Run `python Manual_download.py <TYPE> <NAME> <LANGUAGE> <DownloadMode> [SeasonOverride] [ProviderOverride]`

## Values/Overrides

### Required:

- type_of_media: Either "serie" or "anime" so the tool uses the correspondig url
- name: Enter the anime or serie name you want to download. It has to be in the naming scheme _word-word-word_.
- language: Determine the desired language of the files. Common options are: "Deutsch", "Ger-Sub" and "English"

### Optional:

- dlMode: Choose the type of Content you want to download. Valid arguments are: Movies, Series, All. Default is Series.
- season_override: Specify which season to Download. 0 is the Default and will download all Seasons.

## Constants

- episode_override: Specify which episode to start downloading. 0 is the Default and will download all Episodes.
- ddos_protection_calc: How many episodes to download before waiting 60 seconds. Default 4.
- ddos_wait_timer: How long to wait until next download batch starts. Default 60.
- output_path: Specify the output path. Default is the current working directory/Name-Of-Series.

## Support

Please create a Issue.

## Special Thanks:

Thank you to [Michtdu](https://github.com/Michtdu) for the workaround and code for the Captcha!

Thank you [speedyconzales](https://github.com/speedyconzales) for adding S.to support
