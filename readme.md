# Anime/Serien Scraper

Scraper for the Anime Hoster Aniworld and the Serien Hoster SerienStream

This tool will download either all Seasons and Episodes of an anime from Aniworld.to
or it will download all Seasons and Episodes of a serie from S.to

### How to use:

- Clone the Repo
- `pip install -r requirements.txt`
- download or install [ffmpeg](https://ffmpeg.org) (If you download it put it in the root folder or src folder)

#### Unix:

- Use the command line to execute the script: `run.sh`
- Follow the instructions in the terminal
  - First option: **New request** or **Retry**
    - New request: Creates a download thread based on the specified given arguments
    - Retry: Retry all failed downloads from the `logs/failures.log` file

#### Windows:

- Use the command line to execute the script: `run.bat`
- Follow the instructions in the terminal

### Manual usage with python:

- Either use arguments or edit the `src/constants.py` file
- ARGUMENTS: `main.py <TYPE> <NAME> <LANGUAGE> <DownloadMode> [SeasonOverride] [ProviderOverride]`
- Change name in `src/constants.py` to your desired name (Format -> see URL of the anime or serie)
- If you now start the `main.py` it will start downloading the desired content.

## Manual download

If you get a error or only need a specific episode you can download it manually with the `Manual_download.py` script.

Run it with the same arguments as you would main.py.

- Edit the `src/constants.py` and change the `episode_override` to the desired episode.
- Run `python Manual_download.py <TYPE> <NAME> <LANGUAGE> <DownloadMode> [SeasonOverride] [ProviderOverride]`

## Values/Overrides

### Required:

- **type_of_media**: Either "**serie**" or "**anime**" so the tool uses the correspondig url
- **name**: Enter the anime or serie name you want to download. It has to be in the naming scheme `word-word-word`.
- **language**: Determine the desired language of the files. Common options are: "**Deutsch**", "**Ger-Sub**" and "**English**"

### Optional:

- **dlMode**: Choose the type of Content you want to download. Valid arguments are: Movies, Series, All. Default is `Series`.
- **season_override**: Specify which season to Download. `0` is the Default and will download all Seasons.

## Constants

- **episode_override**: Specify which episode to start downloading. `0` is the Default and will download all Episodes.
- **ddos_protection_calc**: How many episodes to download before waiting **60** seconds. Default `4`.
- **ddos_wait_timer**: How long to wait until next download batch starts. Default `60`.
- **output_path**: Specify the output path. Default is the current working directory/Name-Of-Series.
- **useYears** (bool): If True, the year is added to the output path. Default is `False`.
- **file_exists_check**: If True, the programm only checks whether a real file exists in the **output directory**. If False, the **output directory** and **success.log** are checked. Default is `False`

## Failures Log

If a download fails, this is logged in the `logs/failures.log` file. You can retry the failed downloads by running `run.sh` with the `retry` option.
You can manually modify the **logs/failures.log** file to remove the failed downloads. You can also change the language or download provider if the download failed due to an unsupported language or provider.

## Support

Please create a Issue.

## Special Thanks:

Thank you to [Michtdu](https://github.com/Michtdu) for the workaround and code for the Captcha!

Thank you [speedyconzales](https://github.com/speedyconzales) for adding S.to support
