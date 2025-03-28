#!/usr/bin/env python3
import time

import requests

from git_tools import gitlab_apis
from git_tools.sqlite_util import sqliteTool
from .config_utils import get_config
from .git_env import *

headers = get_config()['default_http_header']

from .cookie_util import get_cookies_from_chrome
from .gitrepo import GitRepo


def get_pipeline_by_tag(git_repo, project_id, tag_id):
    # 获取流水线列表
    pipelines_url = f"{git_repo.gitlab_url}/api/v4/projects/{project_id}/pipelines"
    response = requests.get(pipelines_url, headers=headers, cookies=get_cookies_from_chrome(git_repo.hostname))
    pipelines_json = response.json()

    # 遍历每个流水线
    for pipeline in pipelines_json:
        status, refer, web_url = gitlab_apis.query_pipeline(git_repo, project_id, pipeline["id"])
        web_url = re.sub('http://13.229.25.115', 'https://codelab001.xyz', web_url)
        if tag_id in refer:
            return pipeline["id"], status, web_url
    return None, "not found", "http://not-found"


def get_project_id(git_repo, project_name):
    return git_repo.name_mapping.get(project_name).id


def poll_cicd_status(git_repo, project_id, tag_name):
    pipeline_id, status, web_url = get_pipeline_by_tag(git_repo=git_repo, project_id=project_id, tag_id=tag_name)

    def is_done(status):
        return status == 'canceled' or status == 'success'  # or status == 'failed'

    while not is_done(status):
        time.sleep(2)
        pipeline_id, status, web_url = get_pipeline_by_tag(git_repo=git_repo, project_id=project_id, tag_id=tag_name)
        print(web_url)
        print(f"running:{web_url},status:{status}")


def push_tag(git_repo, tag_name):
    # 获取当前分支名称
    git_repo.create_tag(tag_name, message="add tag")
    remote = git_repo.remote("origin")
    remote.push(refspec=f"+refs/tags/{tag_name}")


def pull_branch(git_repo):
    # 先pull 下最新代码
    git_repo.git.pull('--progress', '--no-rebase', 'origin', git_repo.active_branch.name)


def tag_command():
    argv = sys.argv
    print(f"Usage python3 {argv[0]} {Env.all_envs()}")

    env, job_name = Env.from_argv(argv)

    formatted_date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    tag = env.get_tag_prefix() + formatted_date
    print(f"current tag: {tag}, job: {job_name}")

    repo = git.Repo(path=os.getcwd(), search_parent_directories=True)

    gRepo = Env.get_git_repo()
    print('remote', gRepo.gitlab_url)

    env.check_branches(repo.active_branch.name)  # git rev-parse --abbrev-ref HEAD

    print("begin pull code")
    pull_branch(repo)

    print("begin push tag")
    push_tag(repo, tag)

    project_name = os.path.basename(os.getcwd())
    poll_insert_jobs(job_name, tag, gRepo, project_name, repo.active_branch)


def poll_insert_jobs(job_name, tag, grepo, project_name, active_branch):
    project_id = get_project_id(git_repo=grepo, project_name=project_name)
    if not project_id:
        print(f"project does not exists, please check it")
        sys.exit(0)

    pipeline_id = None
    while not pipeline_id:
        # 等cicd 开始构建任务
        time.sleep(1)
        try:
            pipeline_id, status, web_url = get_pipeline_by_tag(git_repo=grepo, project_id=project_id, tag_id=tag)
        except Exception as e:
            pass

    jobs = gitlab_apis.search_jobs(grepo=grepo, project_id=project_id, pipeline_id=pipeline_id)
    for j in jobs:
        sqliteTool.insert_job(job_id=j.job_id, branch=active_branch, project_id=project_id,
                              project_name=project_name, pipeline_id=pipeline_id,
                              job_name=job_name, name=j.name, stage=j.stage, status=j.status, refer=j.refer,
                              web_url=web_url, hexsha=j.hexsha)

    poll_cicd_status(git_repo=grepo, project_id=project_id, tag_name=tag)
