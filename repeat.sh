#!/bin/bash

command_to_start_program="python3 main.py"
counter=0
shutdown_flag="shutdown"
success_file="SUCCESS_OF_REPEAT.SH"

while true; do
    ${command_to_start_program}
    counter=$((counter+1))
    if [ ! -s logs/failures.log ];
    then
        echo ""
        echo ""
        echo ""
        echo "There were no errors. Stopping the program."
        echo "Program ran $counter times"
        break
    fi
    echo ""
    echo ""
    echo "There were errors. Re-running the program."
    echo ""
done

if [ -f $shutdown_flag ];
then
    echo "Removing $shutdown_flag"
    rm $shutdown_flag
    echo "Shutting down"
    shutdown now
else
    touch $success_file
fi
