#!/bin/bash

SCRIPT_PATH="start_app.py"
ANIME_NAME="hunter-x-hunter"
SEASON=0 # 0 means all seasons otherwise specify the season you want
NUM_RUNS=3

for ((i=1; i<=NUM_RUNS; i++))
do
    python3 "$SCRIPT_PATH" "$ANIME_NAME" "$SEASON"
done
