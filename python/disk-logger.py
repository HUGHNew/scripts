import os.path as osp
from datetime import datetime
from typing import Callable
from dataclasses import dataclass
import json

from disk_usage_base import get_mount_points, get_disk_usage

import typer


@dataclass
class LogMsgDict:
    point: str
    usage: int
    free: int
    total: int
    rate: float


FormatFn = Callable[[str, str, LogMsgDict], str]
"""
date:= 2000-01-01
time:= 18:09:01
csv: date,time,mount_point,usage,free,total,use_rate
"""
Formatters: dict[str, FormatFn] = {}


def register(name: str):
    def decorator(cls):
        Formatters[name] = cls
        return cls

    return decorator


@register("csv")
def Csv(date: str, time: str, msg: LogMsgDict) -> str:
    parts = [
        date,
        time,
        msg.point,
        str(msg.usage),
        str(msg.free),
        str(msg.total),
        f"{100*msg.rate:.2f}",
    ]
    return ",".join(parts)


@register("json")
def Json(date: str, time: str, msg: LogMsgDict) -> str:
    return json.dumps(
        {
            "date": date,
            "time": time,
            "point": msg.point,
            "usage": {
                "total": msg.total,
                "free": msg.free,
                "use": msg.usage,
                "rate": msg.rate,
                "unit": "GiB",
            },
        }
    )


def get_formatter(format: str) -> FormatFn:
    if format not in Formatters:
        raise ValueError(f"formatter type:{format} does not exist")
    return Formatters.get(format) # type: ignore


def __compose_log_line(msg: LogMsgDict, format: str):
    date, time = datetime.now().strftime("%Y-%m-%d,%H:%M:%S").split(",")
    formatter = get_formatter(format)
    return formatter(date, time, msg)


def track_disk_usage(log_file: str, format: str = "csv", mount_only: bool = True):
    mps = get_mount_points()
    usages = [
        __compose_log_line(LogMsgDict(**get_disk_usage(mp, 0.7, 0.9, True)), format) # type: ignore
        + "\n"
        for mp in mps
        if mount_only and osp.ismount(mp)
    ]

    with open(log_file, "a") as logger:
        logger.writelines(usages)


if __name__ == "__main__":
    typer.run(track_disk_usage)
