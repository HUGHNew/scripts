#!/usr/bin/env python
# coding=utf-8
from datetime import datetime
import sys, socket

LOG_FILE = f".loc/{sys.argv[1]}"
HOST = socket.gethostname()

def offline_record(info:list[str]):
    line_1st_parts = info[0].split() # len: 10
    offset = 1 if '[' in info[1] else 0
    if info[1][4] == ' ':
        info[1] = info[1][:4]+info[1][5:]
    line_2nd_parts = info[1].split(' ', 11+offset)
    try:
        year = datetime.now().year
        month = line_1st_parts[0]
        day = line_1st_parts[1]
        time = line_1st_parts[2]
        pci = line_1st_parts[-2]
        gpu = line_1st_parts[-1]
        xid = line_2nd_parts[8+offset]
        reason = line_2nd_parts[-1]

        log = f"[{year}-{month}-{day}/{time}] {pci}, {gpu}, Xid:{xid} {reason}"
    except IndexError:
        # log =
        start = info[1].index("Xid")
        log = info[0][:-1] + "  " + info[1][start:]

    with open("gpu.log", "a") as logger:
        logger.write(log)

if __name__ == "__main__":
    with open(LOG_FILE) as fd:
        content = fd.readlines()

    tp = []
    for line in content:
        if line == "--\n":
            offline_record(tp)
            tp = []
        elif HOST in line:
            break
        else:
            tp.append(line)
    # parts.append(tp) # It looks no need
