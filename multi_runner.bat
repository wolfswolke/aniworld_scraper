@echo off
rem Script that takes a list of names and a base ARG set for those on main.py
rem v0.0.1
rem last change: 2024.08.21_6:15
rem change list:
rem 0.0.1 INITIAL COMMIT

set SCRIPT_PATH=main.py

echo.
echo Choose a type:
echo 1. Anime 2. Serie
set /p TYPE=Type:
if %TYPE%==1 set TYPE=anime
if %TYPE%==2 set TYPE=serie
cls

echo.
echo Choose a language:
echo 1. Deutsch 2. Ger-Sub 3. English
set /p LANGUAGE=Language:
if %LANGUAGE%==1 set LANGUAGE=Deutsch
if %LANGUAGE%==2 set LANGUAGE=Ger-Sub
if %LANGUAGE%==3 set LANGUAGE=English
cls

echo.
echo Choose a download mode:
echo 1. Movies 2. Series 3. All
set /p DLMODE=dlMode:
if %DLMODE%==1 set DLMODE=Movies
if %DLMODE%==2 set DLMODE=Series
if %DLMODE%==3 set DLMODE=All
cls

echo.
echo Choose a provider:
echo 1. VOE 2. Vidoza 3. Streamtape
set /p PROVIDER=Provider:
if %PROVIDER%==1 set PROVIDER=VOE
if %PROVIDER%==2 set PROVIDER=Vidoza
if %PROVIDER%==3 set PROVIDER=Streamtape
cls

echo.
echo Enter a list of names separated by spaces. Example: "name1 name2 name3"
set /p NAMES=Names:
for %%N in (%NAMES%) do (
    rem run the script with the current name
    python %SCRIPT_PATH% --type %TYPE% --name %%N --lang %LANGUAGE% --dl-mode %DLMODE% --provider %PROVIDER%
)
echo Done!
pause