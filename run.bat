@echo off
chcp 850 >nul
cls

echo Select your Display Language:
echo Waehle deine Anzeige-Sprache:
echo.
echo 1. English
echo 2. Deutsch (German)
echo.
set /p LANG=Language:
if %LANG%==1 goto eng
if %LANG%==2 goto ger

:eng
set hello_header=Welcome to AniWorldScraper!
set choose_media=Please select the type of media you want to download:
set media_type_anime=1. Anime (Aniworld.to)
set media_type_series=2. Series (s.to)
set media_name=Enter the exact name of the media you wish to download:
set media_desc=Use the precise name as in the website URL (e.g., angels-of-death).
set media_lang=Choose the language of the media:
set media_choice1=1. German
set media_choice2=2. German Subtitles
set media_choice3=3. English
set download_mode=Select the download mode:
set download_mode_movies=1. Movies only
set download_mode_series=2. Series only
set download_mode_all=3. All content
set season_header=Enter the season you want to download:
set season_desc=Enter nothing to download all seasons.
set provider_header=Select the provider to download from:
set provider_desc=Default provider is VOE.
set start_scraper=Starting the scraper...
set finish_scraper=Download completed!
goto start

:ger
set hello_header=Willkommen bei AniWorldScraper!
set choose_media=Bitte waehle den Medientyp aus, den du herunterladen moechtest:
set media_type_anime=1. Anime (Aniworld.to)
set media_type_series=2. Serie (s.to)
set media_name=Gib den exakten Namen des Mediums ein, das du herunterladen moechtest:
set media_desc=Verwende den genauen Namen wie in der URL der Webseite (z. B. angels-of-death).
set media_lang=Waehle die Sprache des Mediums aus:
set media_choice1=1. Deutsch
set media_choice2=2. Mit deutschen Untertiteln
set media_choice3=3. Englisch
set download_mode=Bitte waehle den Download-Modus aus:
set download_mode_movies=1. Nur Filme
set download_mode_series=2. Nur Serien
set download_mode_all=3. Alle Inhalte
set season_header=Gib die Staffel ein, die du herunterladen moechtest:
set season_desc=Gib nichts ein, um alle Staffeln herunterzuladen.
set provider_header=Waehle den Anbieter aus, von dem du herunterladen moechtest:
set provider_desc=Standardanbieter ist VOE.
set start_scraper=Scraper wird gestartet...
set finish_scraper=Herunterladen abgeschlossen!
goto start

:start
echo %hello_header%
echo.
echo %choose_media%
echo.
echo %media_type_anime%
echo %media_type_series%
echo.
set /p TYPE=Type:
if %TYPE%==1 set TYPE=anime
if %TYPE%==2 set TYPE=serie
cls
echo.
echo %media_name%
echo %media_desc%
echo.
set /p NAME=Name:
cls
echo.
echo %media_lang%
echo.
echo %media_choice1%
echo %media_choice2%
echo %media_choice3%
echo.
set /p LANGUAGUE=Language:
if %LANGUAGUE%==1 set LANGUAGUE=Deutsch
if %LANGUAGUE%==2 set LANGUAGUE=Ger-Sub
if %LANGUAGUE%==3 set LANGUAGUE=English
cls
echo.
echo %download_mode%
echo.
echo %download_mode_movies%
echo %download_mode_series%
echo %download_mode_all%
echo.
set /p DLMODE=dlMode:
if %DLMODE%==1 set DLMODE=Movies
if %DLMODE%==2 set DLMODE=Series
if %DLMODE%==3 set DLMODE=All
cls
echo.
echo %season_header%
echo %season_desc%
echo.
set /p SEASON=Season:
cls
echo.
echo %provider_header%
echo %provider_desc%
echo.
echo 1. VOE
echo 2. Vidoza
echo 3. Streamtape
echo.
set /p PROVIDER=Provider:
if %PROVIDER%==1 set PROVIDER=VOE
if %PROVIDER%==2 set PROVIDER=Vidoza
if %PROVIDER%==3 set PROVIDER=Streamtape
cls
echo.
echo %start_scraper%

set SCRIPT_PATH=main.py
python %SCRIPT_PATH% --type %TYPE% --name %NAME% --lang %LANGUAGUE% --dl-mode %DLMODE% --season-override %SEASON% --provider %PROVIDER%
echo %finish_scraper%
PAUSE
