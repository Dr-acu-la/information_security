#!/usr/bin/env python3
"""
sysreport.py - append a timestamped system health report to a log file.
Run by cron on a schedule; needs no credentials, so it is easy to test.
"""
import os
import shutil
import datetime

LOG = os.path.expanduser("~/sysreport.log")


def human(n):
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024:
            return f"{n:.1f}{unit}"
        n /= 1024
    return f"{n:.1f}PB"


def main():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total, used, free = shutil.disk_usage("/")

    try:
        load1, load5, load15 = os.getloadavg()
        load = f"{load1:.2f} {load5:.2f} {load15:.2f}"
    except OSError:
        load = "n/a"

    line = (f"[{now}] disk used {human(used)}/{human(total)} "
            f"(free {human(free)}) | load avg: {load}\n")

    with open(LOG, "a") as f:
        f.write(line)

    print(line, end="")   # also print, so you see output when run by hand


if __name__ == "__main__":
    main()
