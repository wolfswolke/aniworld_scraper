#!/bin/bash

SCRIPT_PATH="start_app.py"
TYPE="serie"
NAME="game-of-thrones"
SEASON=8 # 0 means all seasons otherwise specify the season you want
NUM_RUNS=3

for ((i=1; i<=NUM_RUNS; i++))
do
    python3 "$SCRIPT_PATH" "$TYPE" "$NAME" "$SEASON"
done
