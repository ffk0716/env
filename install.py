#!/usr/bin/env python3

import os

env_root = os.path.dirname(os.path.realpath(__file__))
print(f"env_root = {env_root}")

dot_file_path = os.path.join(env_root, "dotfiles")

import pathlib

home = pathlib.Path.home()

for f in os.listdir(dot_file_path):
    if f.startswith('.'):
        continue
    f_path = os.path.join(dot_file_path, f)
    if not os.path.isfile(f_path):
        continue
    t_path = os.path.join(pathlib.Path.home(), f".{f}")
    print(f"install {f}:")
    if os.path.isfile(t_path):
        if os.path.islink(t_path):
            os.remove(t_path)
            print(f"    target is symlink, remove")
        else:
            print(f"    target is file, backup")
            exit(1)
    os.symlink(f_path, t_path)
    print(f"    link")

print("")
print("setup vim")
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
