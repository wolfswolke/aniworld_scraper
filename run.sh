#!/bin/bash

SCRIPT_PATH="main.py"
TYPE="anime"
NAME="Name-Goes-Here"
LANGUAGE="Deutsch" # most common: ["Deutsch","Ger-Sub","English"]
SEASON=0 # 0 means all seasons otherwise specify the season you want
NUM_RUNS=1
DLMODE="Series"
PROVIDER="VOE"

# Reset
Color_Off='\033[0m'       # Text Reset

# Regular Colors
Black='\033[0;30m'        # Black
Red='\033[0;31m'          # Red
Green='\033[0;32m'        # Green
Yellow='\033[0;33m'       # Yellow
Blue='\033[0;34m'         # Blue
Purple='\033[0;35m'       # Purple
Cyan='\033[0;36m'         # Cyan
White='\033[0;37m'        # White

# Background
On_Black='\033[0;40m'       # Black
On_Red='\033[0;41m'         # Red
On_Green='\033[0;42m'       # Green
On_Yellow='\033[0;43m'      # Yellow
On_Blue='\033[0;44m'        # Blue
On_Purple='\033[0;45m'      # Purple
On_Cyan='\033[0;46m'        # Cyan
On_White='\033[0;47m'       # White

function choose_from_menu() {
    local prompt="$1" outvar="$2"
    shift
    shift
    local options=("$@") cur=0 count=${#options[@]} index=0
    local esc=$(echo -en "\033") # cache ESC as test doesn't allow esc codes
    printf "$prompt\n"

    COLOR_OFF='\033[0m'
    BICYAN='\033[1;96m'
    WHITE='\033[0;37m'
    BLACK='\033[0;30m'

    while true
    do
        # list all options (option list is zero-based)
        index=0
        for o in "${options[@]}"
        do
            if [ "$index" == "$cur" ]
            then echo -e " ${BICYAN}> $o${COLOR_OFF}" # mark & highlight the current option
            else echo -e "   $o"
            fi
            index=$(( $index + 1 ))
        done

        read -s -n3 key # wait for user to key in arrows or ENTER

        case $key in
            $esc[A)
                cur=$(( $cur - 1 ))
                if [ "$cur" -lt 0 ]; then
                    cur=0
                fi ;;
            $esc[B)
                cur=$(( $cur + 1 ))
                if [ "$cur" -ge "$count" ]; then
                    cur=$(( $count - 1 ))
                fi ;;
            '') break ;;
            *) ;;
        esac
        echo -en "\033[${count}A" # go up to the beginning to re-render
    done
    # export the selection to the requested output variable
    printf "${COLOR_OFF}"
    printf -v $outvar "${options[$cur]}"
}

selectionsType=(
    "Anime"
    "TV-show"
    "Quit"
)
choose_from_menu "Please select a download type:" selectedType "${selectionsType[@]}"
case $selectedType in
    "Anime")
        TYPE="anime"
        ;;
    "TV-show")
        TYPE="serie"
        ;;
    "Quit")
        exit
        ;;
    *) echo "invalid option $REPLY";;
esac
echo ""

selectionsDlMode=(
    "Seasons"
    "Movies"
    "Quit"
)
choose_from_menu "Please select the download mode:" selectedDlMode "${selectionsDlMode[@]}"
case $selectedDlMode in
    "Seasons")
        DLMODE="series"
        ;;
    "Movies")
        DLMODE="movies"
        ;;
    "Quit")
        exit
        ;;
    *) echo "invalid option $REPLY";;
esac
echo ""

selectionsLanguage=(
    "German"
    "English"
    "GerSub"
    "Quit"
)
choose_from_menu "Please select a language:" selectedLanguage "${selectionsLanguage[@]}"
case $selectedLanguage in
    "German")
        LANGUAGE="Deutsch"
        ;;
    "English")
        LANGUAGE="English"
        ;;
    "GerSub")
        LANGUAGE="Ger-Sub"
        ;;
    "Quit")
        exit
        ;;
    *) echo "invalid option $REPLY";;
esac
echo""

echo -e "Type in the name"
echo -e "example URL: https://aniworld.to/anime/stream/made-in-abyss/staffel-1"
echo -e "[${Green}made-in-abyss${Color_Off}]"
read -p " > " NAME

echo""

selectionsSeason=(
    "All"
    "Custom"
    "Quit"
)
choose_from_menu "Please select a season:" selectedSeason "${selectionsSeason[@]}"
case $selectedSeason in
    "All")
        SEASON=0
        ;;
    "Custom")
        read -p "Enter the season number: " SEASON
        ;;
    "Quit")
        exit
        ;;
    *) echo "invalid option $REPLY";;
esac
echo ""

selectionsProvider=(
    "VOE"
    "Streamtape"
    "Vidoza"
    "Quit"
)
choose_from_menu "Please select a provider:" selectedProvider "${selectionsProvider[@]}"
case $selectedProvider in
    "VOE")
        PROVIDER="VOE"
        ;;
    "Streamtape")
        PROVIDER="Streamtape"
        ;;
    "Vidoza")
        PROVIDER="Vidoza"
        ;;
    "Quit")
        exit
        ;;
    *) echo "invalid option $REPLY";;
esac
echo ""

for ((i=1; i<=NUM_RUNS; i++))
do
    python3 "$SCRIPT_PATH" --type "$TYPE" --name "$NAME" --lang "$LANGUAGE" --dl-mode "$DLMODE" --season-override "$SEASON" --provider "$PROVIDER"
done
