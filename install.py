#!/usr/bin/env python3

import os


def install_dotfiles(files):

    import pathlib

    home = pathlib.Path.home()

    for f in files:
        fn = os.path.basename(f)
        t = os.path.join(pathlib.Path.home(), f".{fn}")
        print(f"install {fn} {t}:")
        if os.path.islink(t):
            os.remove(t)
            print(f"    target is symlink, remove")
        elif os.path.isfile(t):
            print(f"    target is file, backup")
            exit(1)
        os.symlink(f, t)
        print(f"    link: {f} -> {t}")


def install_vim():
    print("setup vim")
    import pathlib
    home = pathlib.Path.home()
    b = os.path.join(home, ".vim/bundle")
    b_git = os.path.join(b, "Vundle.vim")
    if not os.path.isdir(b_git):
        print("    can't find Vundle, install it")
        pathlib.Path(b).mkdir(parents=True, exist_ok=True)

        import git
        g = git.Git(os.path.join(home, ".vim/bundle"))
        g.clone("https://github.com/VundleVim/Vundle.vim.git")
        print("        done")
    print("    install plugin for vim")

    import subprocess
    process = subprocess.call(['vim', '+PluginInstall', '+qall'])


if __name__ == "__main__":
    env_root = os.path.dirname(os.path.realpath(__file__))
    print(f"env_root = {env_root}")
    dot_file_path = os.path.join(env_root, "dotfiles")
    files = []
    for f in os.listdir(dot_file_path):
        if f.startswith('.'):
            continue
        f_path = os.path.join(dot_file_path, f)
        files.append(f_path)
    install_dotfiles(files)
    print("")
    install_vim()
