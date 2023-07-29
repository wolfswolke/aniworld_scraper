#!/bin/bash

SCRIPT_PATH="start_app.py"
TYPE="anime"
NAME="tokyo-godfathers"
LANGUAGE="Deutsch" # most common: ["Deutsch","Ger-Sub","English"]
SEASON=0 # 0 means all seasons otherwise specify the season you want
NUM_RUNS=1

for ((i=1; i<=NUM_RUNS; i++))
do
    python3 "$SCRIPT_PATH" "$TYPE" "$NAME" "$LANGUAGE" "$SEASON"
done
