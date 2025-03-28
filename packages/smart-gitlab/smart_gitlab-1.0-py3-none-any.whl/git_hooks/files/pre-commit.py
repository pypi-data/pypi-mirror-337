#!/usr/bin/env python3
import os
import re
import subprocess
import sys

import git

exception_projects = ['tkl-ops', 'tkl-doc']


def can_commit(current_branch):

    if re.findall("betfofo/\d{6,8}", current_branch):
        return True
    if re.findall("gww/\d{6,8}", current_branch):
        return True
    if re.findall("feature/\d{2,8}", current_branch):
        return True
    return False


def pre_commit(project):
    # 获取当前分支名称
    repo = git.Repo(search_parent_directories=True)
    current_branch = repo.active_branch.name
    if project in exception_projects:
        return
    # 判断是否在 master 分支
    if not can_commit(current_branch):
        print(f"[pre-commit]提交已取消。当前branch: {current_branch}")
        print(f"执行 fCommit,暂时取消限制")
        sys.exit(1)


if __name__ == "__main__":
    path = os.path.basename(os.getcwd())
    pre_commit(path)
    # 1
