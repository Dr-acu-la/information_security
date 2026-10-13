#!/bin/bash
# current_time.sh - shows the current time and how long until the work day ends
# Usage: ./current_time.sh [end_hour]    (default end hour: 18, i.e. 18:00)

END_HOUR=${1:-18}

HOUR=$(date +%H)
MINUTE=$(date +%M)

# 10# forces base 10, so "08" and "09" are not read as octal numbers
NOW=$(( 10#$HOUR * 60 + 10#$MINUTE ))
END=$(( END_HOUR * 60 ))
LEFT=$(( END - NOW ))

echo "Current time: $HOUR:$MINUTE."

if [ "$LEFT" -le 0 ]; then
    echo "The work day is over. Go home!"
else
    echo "Work day ends after $(( LEFT / 60 )) hours and $(( LEFT % 60 )) minutes."
fi
