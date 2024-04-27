@echo off

cls

echo Welcome to AniWorldScraper!
echo.
echo Please choose the media type you want to download:
echo.
echo 1. Anime (Aniworld.to)
echo 2. Series (s.to)
echo.
set /p TYPE=Type:

if %TYPE%==1 set TYPE=anime
if %TYPE%==2 set TYPE=serie
cls

echo.
echo Please enter the name of the media you want to download:
echo Use the exact name as on the website. (angels-of-death)
echo.
set /p NAME=Name:
cls

echo.
echo Please choose the language of the media you want to download:
echo.
echo 1. Deutsch
echo 2. Ger-Sub
echo 3. English
echo.
set /p LANGUAGUE=Language:

if %LANGUAGUE%==1 set LANGUAGUE=Deutsch
if %LANGUAGUE%==2 set LANGUAGUE=Ger-Sub
if %LANGUAGUE%==3 set LANGUAGUE=English
cls

echo.
echo Please choose the download mode:
echo.
echo 1. Only Movies
echo 2. Only Series
echo 3. All Content
echo.
set /p DLMODE=dlMode:

if %DLMODE%==1 set DLMODE=Movies
if %DLMODE%==2 set DLMODE=Series
if %DLMODE%==3 set DLMODE=All
cls

echo.
echo Please enter the season you want to download:
echo Enter 0 for all seasons.
echo.
set /p SEASON=Season:
cls

echo.
echo Please choose the provider you want to download from:
echo Default is VOE.
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
echo Starting scraper now...

REM Set the values from command line arguments
set SCRIPT_PATH=main.py
REM set TYPE=anime
REM set NAME=Name-Goes-Here
REM set LANGUAGUE=Deutsch
REM set DLMODE=Series
REM set SEASON=0
REM set PROVIDER=VOE

rem Script path = File to run
rem Type = anime or serie
rem Name = Name of the anime or series
rem Language = Language of the anime or series most common: ["Deutsch","Ger-Sub","English"]
rem dlMode = Choose your Content ["Movies", "Series", "All"]
rem Season = 0 means all seasons otherwise specify the season you want
rem Provider = Choose your Provider ["VOE", "Vidoza", "Streamtape"]

python %SCRIPT_PATH% %TYPE% %NAME% %LANGUAGUE% %DLMODE% %SEASON% %PROVIDER%
echo Done!
exit