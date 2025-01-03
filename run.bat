@echo off
cls
echo Select your Display Language:
echo Wähle deine Anzeige-Sprache:
echo.
echo 1. English
echo 2. Deutsch
echo.
set /p LANG=Language:
if %LANG%==1 goto eng
if %LANG%==2 goto ger

:eng
set hello_header=Welcome to AniWorldScraper!
set choose_media=Please choose the media type you want to download:
set media_type_anime=1. Anime (Aniworld.to)
set media_type_series=2. Series (s.to)
set media_name=Please enter the name of the media you want to download:
set media_desc=Use the exact name as in the website URL. (angels-of-death)
set media_lang=Please choose the language of the media you want to download:
set media_choice1=1. German
set media_choice2=2. German Subtitles
set media_choice3=3. English
set download_mode=Please choose the download mode:
set download_mode_movies=1. Only Movies
set download_mode_series=2. Only Series
set download_mode_all=3. All Content
set season_header=Please enter the season you want to download:
set season_desc=Enter 0 for all seasons.
set provider_header=Please choose the provider you want to download from:
set provider_desc=Default value is VOE
set start_scraper=Starting scraper now...
set finish_scraper=Done!
goto start

:ger
set hello_header=Willkommen bei AniWorldScraper!
set choose_media=Bitte wähle den Medientyp, den du herunterladen möchtest:
set media_type_anime=1. Anime (Aniworld.to)
set media_type_series=2. Serie (s.to)
set media_name=Bitte gib den Namen des Mediums ein, das du herunterladen möchtest:
set media_desc=Verwende den genauen Namen wie in der URL der Webseite. (angels-of-death)
set media_lang=Bitte wähle die Sprache des Mediums, das du herunterladen möchtest:
set media_choice1=1. Deutsch
set media_choice2=2. Mit deutschen Untertiteln
set media_choice3=3. Englisch
set download_mode=Bitte wähle den Download-Modus:
set download_mode_movies=1. Nur Filme
set download_mode_series=2. Nur Serien
set download_mode_all=3. Alle Inhalte
set season_header=Bitte gib die Staffel ein, die du herunterladen möchtest:
set season_desc=Gib 0 für alle Staffeln ein.
set provider_header=Bitte wähle den Anbieter, von dem du herunterladen möchtest:
set provider_desc=Standardwert ist VOE
set start_scraper=Scraper wird jetzt gestartet...
set finish_scraper=Fertig!
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
python %SCRIPT_PATH% --type %TYPE% --name %NAME% --lang %LANGUAGUE% --mode %DLMODE% --season_override %SEASON% --provider %PROVIDER%
echo %finish_scraper%
PAUSE
