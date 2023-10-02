import os, shutil

def _filter_non_disk_item(line:str) -> bool:
    """
    leave the mounted disk partitions only
    """
    return line.startswith('/') and \
        not (line.startswith("/dev/fuse") or "/boot" in line)

def get_mount_points(disk_only:bool=True) -> list[str]:
    with open("/proc/mounts") as mts:
        mps = [
            line.split(maxsplit=3)[1]
            for line in mts.readlines()
            if disk_only and _filter_non_disk_item(line)
        ]
    return mps

class Colors:
    RED    = '\033[91m'
    GREEN  = '\033[92m'
    YELLOW = '\033[93m'
    BLUE   = '\033[94m'
    PURPLE = '\033[95m'
    CYAN   = '\033[96m'
    ENDC   = '\033[0m'
    BOLD   = '\033[1m'
    UNDERLINE = '\033[4m'
    @classmethod
    def __concate(cls, color:str, msg:str)->str:
        return f"{color}{msg}{cls.ENDC}"
    @classmethod
    def none(cls, msg:str)->str:
        return msg
    @classmethod
    def health(cls, msg:str)->str:
        return cls.__concate(cls.GREEN, msg)
    @classmethod
    def warning(cls, msg:str)->str:
        return cls.__concate(cls.YELLOW, msg)
    @classmethod
    def error(cls, msg:str)->str:
        return cls.__concate(cls.RED, msg)

GiB = 2 ** 30
def get_disk_usage(mount:str, warn:float, err:float, return_dict:bool=False) -> str|dict[str, int|float|str]:
    if not os.path.ismount(mount):
        raise RuntimeError(f"{mount} is not a mount point")
    total, used, free = shutil.disk_usage(mount)
    usage_rate = used / total
    total_int_GiB, used_int_GiB, free_int_GiB = round(total/GiB), round(used/GiB), round(free/GiB)
    usage_msg = f"{used_int_GiB}GiB/{total_int_GiB}GiB({100*(used/total):.2f}%)"
    free_msg = f"{free_int_GiB}GiB"
    thres_msg = ""
    if usage_rate >= err:
        color = Colors.error
        thres_msg = "Get Over Dangerous Threshold"
    elif usage_rate >= warn:
        color = Colors.warning
        thres_msg = "Get Over Warning Threshold"
    else:
        color = Colors.none
    
    if return_dict:
        return {
            "point": mount,
            "total": total_int_GiB,
            "free": free_int_GiB,
            "usage": used_int_GiB,
            "rate": usage_rate
        }
    if thres_msg:
        full_usage_msg = f"<{color(mount)}>\t{color(thres_msg)}\n\tusage: {color(usage_msg)}\tfree: {color(free_msg)}"
    else:
        full_usage_msg = f"<{color(mount)}> usage: {color(usage_msg)}\tfree: {color(free_msg)}"
    return full_usage_msg