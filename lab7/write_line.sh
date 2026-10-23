#!/bin/bash
# write_line.sh - append the current date/time to a log file
echo "New line at $(date)" >> "$HOME/file.txt"
