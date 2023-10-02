#!/usr/bin/python3

"""
disk_usage report for motd
the default MOTD path in Debian/Ubuntu is /etc/update-motd.d
grant execution permission and move this script to /etc/update-motd.d. Then you can get disk usage info on login
"""

from disk_usage_base import get_disk_usage, get_mount_points

def show_disks_usage(
        mounts:list,
        warn_thre:float=0.7, err_thre:float=0.9,
    ):
    for mount in mounts:
        print(get_disk_usage(mount, warn_thre, err_thre))

if __name__=="__main__":
    show_disks_usage(get_mount_points())