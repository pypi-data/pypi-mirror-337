import datetime
import os
import re
import sys
from urllib.parse import urlparse

import git

from git_tools import config_utils
from git_tools.gitrepo import GitRepo


class Env:
    def __init__(self):
        self.tag_prefix = "7fq1-"

    def get_tag_prefix(self):
        return self.tag_prefix

    def check_branches(self, current_branch):
        pass

    @staticmethod
    def from_tag(tag_name: str):
        subclasses = Env.__subclasses__()
        for subclass in subclasses:
            sub = subclass()
            if tag_name.startswith(sub.get_tag_prefix()):
                return sub
        default_env = Env()
        default_env.tag_prefix = tag_name
        return default_env

    @staticmethod
    def all_envs():
        result = []
        for subclass in Env.__subclasses__():
            result.append(subclass().tag_prefix)
        return result

    @staticmethod
    def is_prod_branch(current_branch):
        return re.findall("betfofo/production", current_branch) or re.findall("production-20240306",
                                                                              current_branch) or current_branch == 'betfofo/feature_fission' or current_branch == 'gww/production'

    @staticmethod
    def from_argv(argv):
        env = Qa7F()
        if len(argv) >= 2:
            env = Env.from_tag(argv[1])

        jobs = "Everyday-" + datetime.datetime.now().strftime("%Y%m%d")
        if not env:  # 如果环境不符合要求，则认为是任务name
            jobs = argv[1]
        if len(argv) >= 3:
            jobs = argv[2]
        return env, jobs

    @staticmethod
    def get_task_name(argv):
        if len(argv) == 1:
            return "Everyday-" + datetime.datetime.now().strftime("%Y%m%d")
        return argv[1]

    @staticmethod
    def get_git_repo() -> GitRepo:
        def get_remote_hostname():
            repo = git.Repo(path=os.getcwd(), search_parent_directories=True)
            remotes = repo.remotes
            git_pattern = r"git@([^:]+):"
            for r in remotes:
                git_match = re.search(git_pattern, r.url)
                if git_match:
                    return git_match.group(1)
                uri = urlparse(r.url)
                if uri.hostname:
                    return uri.hostname

        try:
            hostname = get_remote_hostname()
            if hostname:
                return GitRepo(hostname)
        except Exception:
            return GitRepo(config_utils.get_config()['default_git_domain'])
        return None


class Qa7F(Env):
    def __init__(self):
        self.tag_prefix = "7fq1-"


class Qa7QA(Env):
    def __init__(self):
        self.tag_prefix = "7qa-"


class QaGWW(Env):
    def __init__(self):
        self.tag_prefix = "gwwq1-"


class DevTW(Env):
    def __init__(self):
        self.tag_prefix = "dev-"


class QaTW(Env):
    def __init__(self):
        self.tag_prefix = "twq1-"


class Prd7f(Env):
    def __init__(self):
        self.tag_prefix = "7prd-"

    def check_branches(self, current_branch):
        if not Env.is_prod_branch(current_branch):
            print(f"Not allowed! 当前branch:{current_branch},tag_prefix:{self.tag_prefix}")
            sys.exit(1)
