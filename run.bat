@echo off

REM Set the values from command line arguments
set SCRIPT_PATH=main.py
set TYPE=anime
set NAME=Name-Goes-Here
set LANGUAGUE=Deutsch
set MOVIE=False
set SEASON=0

rem Script path = File to run
rem Type = anime or series
rem Name = Name of the anime or series
rem Language = Language of the anime or series most common: ["Deutsch","Ger-Sub","English"]
rem Movie = True or False this is for Specials
rem Season = 0 means all seasons otherwise specify the season you want

python %SCRIPT_PATH% %TYPE% %NAME% %LANGUAGUE% %MOVIE% %SEASON%
