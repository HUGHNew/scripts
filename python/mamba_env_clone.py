#!/usr/bin/python3
"""
Script for micromamba env clone
I use the idea
"""
import os
import os.path as osp
import shutil

import fire


def rename_shebang(folder: str, env: str, file_only: bool = True):
    assert osp.isdir(folder), f"{folder} is not a folder"
    assert env.count(" ") == 0, f"space in env name:{env} is disallowd"
    for file in os.listdir(folder):
        bfs = osp.join(folder, file)
        if file_only and not osp.isfile(bfs):
            continue

        with (
            open(bfs) as reader,
        ):
            try:
                content = reader.readlines()
                if not content[0].startswith("#!/"):
                    continue
                parts = content[0][2:].split("/")
                index = parts.index("envs")
                parts[index + 1] = env
                content[0] = f"#!{'/'.join(parts)}"

                writer = open(bfs+".temp", "w")
                writer.writelines(content)
                writer.close()
                print(f"mv {bfs+'.temp'} {bfs}")
                shutil.move(bfs+".temp", bfs)
                os.chmod(bfs, 0o755)
            except UnicodeDecodeError:
                print(f"{bfs} may be a binary file")
            except ValueError:
                # #!/bin/sh or something else who is irrelative with Python
                continue
            except:
                breakpoint()

def replace_shebang(folder: str, path:str, file_only: bool = True):
    assert osp.isdir(folder), f"{folder} is not a folder"
    assert folder.endswith("bin"), f"{folder} should be a bin folder"
    assert path.count(" ") == 0, f"space in path name:{path} is disallowd"
    for file in os.listdir(folder):
        bfs = osp.join(folder, file)
        if file_only and not osp.isfile(bfs):
            continue

        with (
            open(bfs) as reader,
        ):
            try:
                content = reader.readlines()
                if not content[0].startswith("#!/"):
                    continue
                parts = content[0][2:].split("/")
                index = parts.index("envs")
                content[0] = f"#!{path}\n"

                writer = open(bfs+".temp", "w")
                writer.writelines(content)
                writer.close()
                print(f"mv {bfs+'.temp'} {bfs}")
                shutil.move(bfs+".temp", bfs)
                os.chmod(bfs, 0o755)
            except UnicodeDecodeError:
                print(f"{bfs} may be a binary file")
            except ValueError:
                # `#!/bin/sh`,`#! /bin/sh`
                # or something else who is irrelative with Python
                continue
            except:
                breakpoint()

def clone_env(root: str, old_env: str, new_env: str):
    if old_env == new_env:
        return
    assert osp.isdir(root), f"{root} seems not a conda env root"
    old_env_path = osp.join(root, old_env)
    assert osp.isdir(old_env_path), f"{old_env} doesn't exist in {old_env_path}"
    new_env_path = osp.join(root, new_env)
    assert not osp.exists(new_env_path), f"{new_env_path} should not exist"

    shutil.copytree(old_env_path, new_env_path, True)
    rename_shebang(osp.join(new_env_path, "bin"), new_env)


if __name__ == "__main__":
    fire.Fire({"clone": clone_env, "rename": rename_shebang})
