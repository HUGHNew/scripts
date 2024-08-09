import os
import os.path as osp
import shutil

import fire

def replace_shebang(folder: str, path:str, file_only: bool = True, force: bool = False):
    assert osp.isdir(folder), f"{folder} is not a folder"
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
                if not force:
                    assert "envs" in parts, f"{bfs} does not contain 'envs' in shebang"
                    # index = parts.index("envs")
                else:
                    if "python" not in parts[-1]:
                        continue # skip non-python file
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
                # #!/bin/sh or something else who is irrelative with Python
                continue
            except:
                breakpoint()

def replace_with_conda_root(root:str, new_home:str):
    """
    1. root/bin -> new_home/`dirname root`/bin
    2. root/envs/*/bin

    root: the root path of conda like $HOME/miniconda3
    new_home: the new home path to replace the old one
    """
    # replace root/bin
    if root.endswith("/"):
        root = root[:-1]
    root_parts = root.split("/")
    # #!/home/alice/miniconda3/bin/python
    root_home = osp.join(new_home, root_parts[-1])
    replace_shebang(osp.join(root, "bin"), osp.join(root_home, "bin", "python"), force=True)

    # replace root/envs/*/bin
    # #!/home/alice/miniconda3/envs/myenv/bin/python
    for env in os.listdir(osp.join(root, "envs")):
        replace_shebang(osp.join(root, "envs", env, "bin"), osp.join(root_home, "envs", env, "bin", "python"))


if __name__ == "__main__":
    fire.Fire({
        "env_move": replace_shebang,
        "conda_move": replace_with_conda_root
    })