#!/usr/bin/env python3
import os
import time
from datetime import datetime


def list_items_older_than(date_input):
    try:
        # Parse the input date
        target_date = datetime.strptime(date_input, "%Y-%m-%d").timestamp()

        # Get the current directory items (files and folders)
        items = os.listdir('.')

        for item in items:
            # Get the creation time.
            # os.lstat() reads the item itself, so a broken symlink does not crash it.
            # A file we cannot read is skipped instead of crashing the whole shell.
            try:
                item_ctime = os.lstat(item).st_ctime
            except OSError as error:
                print(f"{item} (skipped: {error.strerror})")
                continue

            if item_ctime < target_date:
                # Determine if the item is a file or folder
                item_type = "Folder" if os.path.isdir(item) else "File"
                creation_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item_ctime))
                print(f"{item} ({item_type}, Created: {creation_time})")

    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")


def toy_shell():
    print("Toy Shell: List files and folders older than a given date (based on creation time)")
    print("Enter a date in the format YYYY-MM-DD or type 'exit' to quit.")

    while True:
        try:
            command = input("toy-shell> ").strip()

            if command.lower() == "exit":
                print("Exiting toy shell.")
                break

            list_items_older_than(command)

        except KeyboardInterrupt:
            print("\nUse 'exit' to quit the shell.")
        except EOFError:
            # Ctrl+D closes the input, so quit cleanly
            print("\nExiting toy shell.")
            break


if __name__ == "__main__":
    toy_shell()
