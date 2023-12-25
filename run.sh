#!/bin/bash

SCRIPT_PATH="main.py"
TYPE="anime"
NAME="Name-Goes-Here"
LANGUAGE="Deutsch" # most common: ["Deutsch","Ger-Sub","English"]
SEASON=0 # 0 means all seasons otherwise specify the season you want
NUM_RUNS=1
MOVIE=False

for ((i=1; i<=NUM_RUNS; i++))
do
    python3 "$SCRIPT_PATH" "$TYPE" "$NAME" "$LANGUAGE" "$MOVIE" "$SEASON"
done
