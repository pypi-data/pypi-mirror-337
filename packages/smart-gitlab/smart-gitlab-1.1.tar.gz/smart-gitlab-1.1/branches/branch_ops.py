import argparse
import datetime
import glob
import os
import re

import git


def __get_git_base_path__():
    current = os.getcwd()
    paths = glob.glob(os.path.join(current) + "/**/.git", recursive=True)
    if not paths:
        print("no git files found")
        return None
    return [os.path.dirname(p) for p in paths]


def git_branches_search(branch_name, cmd, cmd_x):
    for git_repo_path in __get_git_base_path__():
        repo = git.Repo(path=git_repo_path, search_parent_directories=True)
        for branch in repo.branches:
            if branch_name == branch.name:
                print(git_repo_path)
                if cmd:
                    each_cmd = re.sub('{}', git_repo_path, cmd, flags=re.I)
                    os.system(each_cmd)
            else:
                if cmd_x:
                    each_cmd = re.sub('{}', git_repo_path, cmd_x, flags=re.I)
                    os.system(each_cmd)


def git_branches_command():
    parser = argparse.ArgumentParser()
    parser.add_argument('branch_name', help='branch name for search')
    parser.add_argument('--do', '-d', help='Execute a command for each item, {} is for each item')
    parser.add_argument('--dx', '-dx', help='Execute a command for each item which is not matches, {} is for each item')

    args = parser.parse_args()
    git_branches_search(args.branch_name, args.do, args.dx)


def git_repolist_command():
    parser = argparse.ArgumentParser()
    parser.add_argument('--do', '-d', help='Execute a command for each item, {} is for each item')
    args = parser.parse_args()
    cmd = args.do
    for git_repo_path in __get_git_base_path__():
        print(git_repo_path)
        if cmd:
            each_cmd = re.sub('{}', git_repo_path, cmd, flags=re.I)
            os.system(each_cmd)


def git_current_branch_command():
    parser = argparse.ArgumentParser()
    parser.add_argument('base_path', default=os.getcwd(), help='Your git project path')
    args = parser.parse_args()

    print(args.base_path)
    git_current_branch(args.base_path)


def git_current_branch(base_path):
    if not os.path.exists(os.path.join(base_path, ".git")):
        print("not a git path")

    repo = git.Repo(path=base_path, search_parent_directories=True)
    print(repo.active_branch)


def git_checkout_branch_command():
    '''
    目录下所有代码checkout到指定分支
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('branch_name', default=os.getcwd(), help='Your branch name to checkout')
    args = parser.parse_args()

    git_checkout_branch(args.branch_name)


def git_checkout_branch(branch_name):
    current = os.getcwd()
    for git_repo_path in __get_git_base_path__():
        print(f"Checkout {os.path.basename(git_repo_path)} to {branch_name}")
        os.system(f"cd {git_repo_path};git checkout {branch_name}")
    os.system(f"cd {current}")


def git_prepull_command():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fetch', '-f', default="False", help='fetch before compare. yes/y/true indicate True')
    args = parser.parse_args()
    fetch = args.fetch

    def custom_bool(fetch):
        if not fetch:
            return False
        if fetch.lower() == "true" or fetch.lower == 'yes' or fetch.lower == 'y':
            return True
        return False;

    git_compare_commit(custom_bool(fetch))


def git_compare_commit(fetch):
    for git_repo_path in __get_git_base_path__():
        try:
            repo = git.Repo(path=git_repo_path, search_parent_directories=True)
            v = repo.rev_parse("HEAD")
            local_hexsha = v.hexsha
            if fetch:
                # fetch code
                remote = repo.remote('origin')
                remote.fetch()

            commits = list(repo.iter_commits(f'origin/{repo.active_branch.name}'))
            remote_sha = commits[0].hexsha
            if remote_sha != local_hexsha:
                print(git_repo_path)
        except Exception as e:
            print(f"error occurred: {git_repo_path},{e}")


def git_status_command():
    parser = argparse.ArgumentParser()
    parser.add_argument('--do', '-d', help='Execute a command for each item, {} is for each item')
    parser.add_argument('--verbose', '-v', help='Print details')
    args = parser.parse_args()
    cmd = args.do

    for git_repo_path in __get_git_base_path__():
        try:
            repo = git.Repo(path=git_repo_path, search_parent_directories=True)
            if repo.is_dirty():
                print(git_repo_path)
                if args.verbose:
                    os.system("git diff --stat|head -n 2222")
                if cmd and not args.verbose:
                    each_cmd = re.sub('{}', git_repo_path, cmd, flags=re.I)
                    os.system(each_cmd)
        except Exception as e:
            print(f"error occurred: {git_repo_path},{e}")


def git_log_command():
    parser = argparse.ArgumentParser()
    parser.add_argument('--message', '-m', help='message')
    parser.add_argument('--author', '-a', help='author')
    parser.add_argument('--committed_date', '-d', default=datetime.datetime.now().strftime("%Y-%m-%d"),
                        help='committed_date,fmt: yyyy-MM-dd')
    args = parser.parse_args()

    def query_logs(commit, message, author, committed_date=datetime.datetime.now().strftime("%Y-%m-%d")):
        if message:
            if not message in commit.message:
                return False
        if author:
            if not author in commit.author:
                return False
        if committed_date:
            if not committed_date in str(datetime.datetime.fromtimestamp(commit.committed_date)):
                return False
        return True

    for git_repo_path in __get_git_base_path__():
        try:
            repo = git.Repo(path=git_repo_path, search_parent_directories=True)
            commits = list(repo.iter_commits(f'origin/{repo.active_branch.name}'))
            cms = [c for c in commits if query_logs(c, args.message, args.author, args.committed_date)]
            if not cms:
                continue
            print(git_repo_path)
            print(f"commits num: {len(cms)}")
            for i in cms[0:10]:
                print(f"{i.author}@{datetime.datetime.fromtimestamp(i.committed_date)}: {i.hexsha}, {i.message}")
        except Exception as e:
            print(f"error occurred: {git_repo_path},{e}")


def git_extract_pull_command():
    parser = argparse.ArgumentParser()
    parser.add_argument('--remote', '-r', default="origin", required=False, help='remote name,default: origin')
    args = parser.parse_args()

    urls = []
    for git_repo_path in __get_git_base_path__():
        repo = git.Repo(path=git_repo_path, search_parent_directories=True)
        urls.append(repo.remote(args.remote).url)
    with open('clone.sh', 'w', encoding='utf-8', ) as f:
        txt = ''
        for url in urls:
            txt += f"git clone {url}\n"
        f.writelines(txt)


if __name__ == '__main__':
    git_extract_pull_command()
