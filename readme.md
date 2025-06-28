# ARCHIVED PROJECT NOTICE

⚠️ This project is no longer maintained.
Why?

I haven't watched a anime in more then a year and couldn’t find a maintainable way to rebuild this project with a cleaner codebase.

If you find anything useful here, feel free to use it in your own projects.

# Anime/Series Scraper

This tool enables you to scrape and download all seasons and episodes of anime from Aniworld.to or series from SerienStream (S.to).

## How to Use

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Download or install [FFmpeg](https://ffmpeg.org):
   - If downloaded, place it in the root or `src` folder.
4. Platform-specific setup:
   - **Unix:** Edit the `_run.sh` file with desired values for easy execution.
   - **Windows:** Edit and run the `_run.bat` file, entering the desired values directly into the command line.

### Manual Usage with Python
You can:
- Edit the `src/constants.py` file.
- Pass arguments directly to the `main.py` script.

#### Supported Arguments
- `--type <TYPE>`: Specify "serie" or "anime" to select the website to scrape.
- `--name <NAME>`: The name of the anime or series to download.
- `--lang <LANGUAGE>`: Desired language (e.g., "Deutsch", "Ger-Sub", "English", or "Eng-Sub").
- `--dl-mode <DownloadMode>`: Content type to download (e.g., Movies, Series, All).
- `--season-override <SeasonOverride>`: Specify seasons to download:
  - `0`: Download all seasons.
  - `NUM`: Download only the specified season.
  - `NUM+`: Download this season and all subsequent seasons.
- `--provider <ProviderOverride>`: Specify the content provider (e.g., VOE, Streamtape, or Vidoza).

## Manual Download
If errors occur or only specific episodes are needed, use the `Manual_download.py` script:

1. Edit `src/constants.py` and set `episode_override` to the desired episode.
2. Run the script:
   ```bash
   python Manual_download.py --type <TYPE> --name <NAME> --lang <LANGUAGE> --season-override <SeasonOverride>
   ```

## Configuration Values

### Required
- `type_of_media`: "serie" or "anime" to select the correct URL.
- `name`: The name of the anime or series, formatted as `word-word-word`.
- `language`: Desired language of the files (e.g., "Deutsch", "Ger-Sub", "English").

### Optional
- `dlMode`: Content type to download (Movies, Series, All; default: Series).
- `season_override`: Specify the season(s) to download (default: 0 for all seasons).

### Constants
- `episode_override`: Specify the starting episode (default: 0 for all episodes).
- `ddos_protection_calc`: Number of episodes to download before pausing (default: 4).
- `ddos_wait_timer`: Wait time (in seconds) before resuming downloads (default: 60).
- `output_path`: Output directory (default: current working directory/Series-Name).

## Support
Please create an issue in the repository for assistance.

## Special Thanks
- [Michtdu](https://github.com/Michtdu) for the workaround and Captcha code.
- [speedyconzales](https://github.com/speedyconzales) for adding support for S.to.
