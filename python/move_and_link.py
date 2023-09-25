import typer
import shutil
import os
import os.path as osp

def _sh_path(path:str) -> str:
    return osp.abspath(osp.expanduser(osp.expandvars(path)))

def move_and_link(src:str, target:str, prompt:bool=False, dryrun:bool=False):
    src = _sh_path(src)
    tgt = _sh_path(target)
    if not osp.exists(src):
        raise ValueError(src, "file/folder not found")
    if osp.isfile(src) and osp.isdir(tgt):
        tgt = osp.join(tgt, osp.basename(src))
    # TODO: process folders merge case
    if src == tgt or osp.realpath(src) == osp.realpath(tgt):
        print("Ignore: same place")
    if osp.exists(tgt):
        print(f"{tgt} does exist")
        if not prompt:
            exit(1)
        choice = input("enter [Y/y/yes] to overwrite current file")
        if choice.lower() not in ['y', 'yes']:
            exit(1)
    if dryrun:
        print(f"mv {src} {tgt}")
        print(f"ln -s {tgt} {src}")
    else:
        shutil.move(src, tgt)
        os.symlink(tgt, src, osp.isdir(tgt))

if __name__ == "__main__":
    typer.run(move_and_link)