#!/bin/bash
# delete_empty_files.sh - finds and deletes all empty files in a directory
# Usage: ./delete_empty_files.sh <directory>

if [ $# -ne 1 ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

DIR=$1

if [ ! -d "$DIR" ]; then
    echo "Error: directory '$DIR' not found."
    exit 1
fi

COUNT=0
# -type f = files only, -empty = size 0, -maxdepth 1 = do not go into subfolders
while IFS= read -r FILE; do
    rm "$FILE"
    echo "Deleted: $FILE"
    COUNT=$((COUNT + 1))
done < <(find "$DIR" -maxdepth 1 -type f -empty)

echo "Total deleted: $COUNT empty file(s)."
