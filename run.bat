@echo off

REM Set the values from command line arguments
set SCRIPT_PATH=main.py
set TYPE=anime
set NAME=Name-Goes-Here
set LANGUAGUE=Deutsch
set DLMODE=Series
set SEASON=0
set PROVIDER=VOE

rem Script path = File to run
rem Type = anime or series
rem Name = Name of the anime or series
rem Language = Language of the anime or series most common: ["Deutsch","Ger-Sub","English"]
rem dlMode = Choose your Content ["Movies", "Series", "All"]
rem Season = 0 means all seasons otherwise specify the season you want
rem Provider = Choose your Provider ["VOE", "Vidoza", "Streamtape"]

python %SCRIPT_PATH% %TYPE% %NAME% %LANGUAGUE% %DLMODE% %SEASON% %PROVIDER%
```
