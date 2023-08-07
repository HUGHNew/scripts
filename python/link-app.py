"""
move downloaded appimage file to `~/AppImages/`, make it executable and link it to `~/.local/bin/`

pip install typer[all]

"""
import os, shutil

import typer

DOWNLOADS = os.path.expanduser("~/Downloads/")
APPIMAGES = os.path.expanduser("~/AppImages/")
LOCAL_BIN = os.path.expanduser("~/.local/bin/")

def get_link_name(filename: str) -> str:
    """
    get default link name with the first part divided by -_.
    """
    if '-' in filename:
        linkname = filename.split('-', 2)[0]
    elif '_' in filename:
        linkname = filename.split('_', 2)[0]
    elif '.' in filename:
        linkname = filename.split('.', 2)[0]
    else:
        linkname = filename
    return linkname.lower()

def move_and_link_appimage(file: str, link: str=""):
    filename = os.path.basename(file)
    down_file = os.path.join(DOWNLOADS, file)
    if os.path.exists(file):
        print(f"{file} exists. prepare to move it to {APPIMAGES}")
        shutil.move(file, APPIMAGES)
    elif os.path.exists(down_file):
        print(f"{file} lies in {DOWNLOADS}. prepare to move it to {APPIMAGES}")
        shutil.move(down_file, APPIMAGES)
    else:
        print(f"{file} does not exist or in {DOWNLOADS}")
        return

    current_file = os.path.join(APPIMAGES, filename)
    print(f"allow user to exec the {current_file}")
    os.chmod(current_file, 0o744)


    linkname = link if link else get_link_name(filename)
    print(f"prepare to link {current_file} to {linkname}")
    os.symlink(current_file, os.path.join(LOCAL_BIN, linkname))

if __name__ == "__main__":
    typer.run(move_and_link_appimage)
