#!/bin/bash
# count_word.sh - counts how many times a word appears in a file
# Usage: ./count_word.sh <file> <word>

if [ $# -ne 2 ]; then
    echo "Usage: $0 <file> <word>"
    exit 1
fi

FILE=$1
WORD=$2

if [ ! -f "$FILE" ]; then
    echo "Error: file '$FILE' not found."
    exit 1
fi

# -o prints every match on its own line, -w matches whole words only,
# then wc -l counts the lines (= number of matches)
COUNT=$(grep -o -w -- "$WORD" "$FILE" | wc -l | tr -d ' ')

echo "The word '$WORD' appears $COUNT time(s) in $FILE."
