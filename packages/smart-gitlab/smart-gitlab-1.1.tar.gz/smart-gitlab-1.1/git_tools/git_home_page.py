#!/usr/bin/env python3
import os
import re
import sys
import webbrowser

import git

from git_tools import git_env


def page_pipeline_command():
    project = os.path.basename(os.getcwd())
    git_repo = git_env.Env.get_git_repo()
    web_url = git_repo.name_mapping.get(project).web_url
    web_url = re.sub('http://13.229.25.115', 'https://codelab001.xyz',  web_url)
    os.system(f"open {web_url}/pipelines")


def page_merge_command():
    project = os.path.basename(os.getcwd())
    git_repo = git_env.Env.get_git_repo()
    p = git_repo.name_mapping.get(project)
    if len(sys.argv) == 1:
        os.system(f"open {p.web_url}/-/merge_requests/new")
        return

    source = ''
    target = ''
    if len(sys.argv) == 2:
        repo = git.Repo(path=os.getcwd(), search_parent_directories=True)
        source = repo.active_branch
        target = sys.argv[1]
    if len(sys.argv) >= 3:
        source = sys.argv[1]
        target = sys.argv[2]
    url = f'{p.web_url}/-/merge_requests/new/diffs?utf8=✓&merge_request[source_project_id]={p.id}&merge_request[source_branch]={source}&merge_request[target_project_id]={p.id}&merge_request[target_branch]={target}'
    url = re.sub('http://13.229.25.115', 'https://codelab001.xyz',  url)
    webbrowser.open_new_tab(url)


if __name__ == '__main__':
    page_merge_command()
