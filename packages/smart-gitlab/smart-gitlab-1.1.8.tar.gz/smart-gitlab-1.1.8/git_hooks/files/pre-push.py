#!/usr/bin/env python3
import os
import re
import subprocess
import sys
import time

import git

exception_projects = ['tkl-ops', 'tkl-doc']


def pre_push(project):
    # 获取当前分支名称
    repo = git.Repo(search_parent_directories=True)
    current_branch = repo.active_branch.name
    if project in exception_projects:
        return
    # 判断是否在 production 分支
    if current_branch in ('production', 'release', 'nlrelease','prod'):
        print(f"push已取消。当前branch: {current_branch}")
        print(f"执行 fCommit,暂时取消限制")
        sys.exit(1)


if __name__ == "__main__":
    path = os.path.basename(os.getcwd())
    pre_push(path)
