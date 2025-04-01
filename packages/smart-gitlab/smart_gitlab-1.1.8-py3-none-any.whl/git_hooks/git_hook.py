#!/usr/bin/env python3
import argparse
import multiprocessing
import os
import time
from tqdm import tqdm

import pkg_resources


def add_hook_command():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', '-p', default=os.getcwd(), help='project full path')
    args = parser.parse_args()
    do_add_hook(args.path)


pre_commit_file = '.git/hooks/pre-commit'
pre_push_file = '.git/hooks/pre-push'


def delay_revert_file(seconds):
    progress = tqdm(range(seconds))
    for i in progress:
        time.sleep(1)
        progress.set_description("Reverting...")
    os.rename(pre_commit_file + ".tmp", pre_commit_file)
    os.rename(pre_push_file + ".tmp", pre_push_file)


def force_commit_command():
    def rn_file(relative_file, tmp_relative_file):
        source_file = os.path.join(os.getcwd(), relative_file)
        target_file = os.path.join(os.getcwd(), tmp_relative_file)
        os.system(f"mv {source_file} {target_file}")

    rn_file(pre_commit_file, pre_commit_file + ".tmp")
    rn_file(pre_push_file, pre_push_file + ".tmp")

    background_process = multiprocessing.Process(name='background_process', target=delay_revert_file,args=(10,))
    background_process.daemon = True
    background_process.start()
    background_process.join()


def do_add_hook(path: str):
    target_pre_commit_file = f"{path}/.git/hooks/pre-commit"
    target_pre_push_file = f"{path}/.git/hooks/pre-push"

    source_pre_commit_file = pkg_resources.resource_filename('git_hooks', 'files/pre-commit.py')
    source_pre_push_file = pkg_resources.resource_filename('git_hooks', 'files/pre-push.py')

    def copy(file1, file2):
        print(f"copy {file1} to {file2}")
        f1 = open(file1, "r")
        f2 = open(file2, "w")

        s = f1.read()
        print(s)
        w = f2.write(s)

        f1.close()
        f2.close()
        os.system(f"chmod +x {file2}")

    copy(source_pre_commit_file, target_pre_commit_file)
    copy(source_pre_push_file, target_pre_push_file)


if __name__ == "__main__":
    add_hook_command()
