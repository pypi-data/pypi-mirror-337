import datetime
import argparse
import os
import sys

import requests
from tqdm import tqdm

from git_tools import cookie_util, git_env
from git_tools.config_utils import get_config
from git_tools.cookie_util import get_cookies_from_chrome
from git_tools.git_env import Env
from git_tools.job_info import job_info
from git_tools.sqlite_util import sqliteTool
headers = get_config()['default_http_header']

all_project = ["tkl-pom", "tkl-core", "tkl-component", "tkl-cms-api", "tkl-user-api", "tkl-tool-api", "tkl-base-api",
               "tkl-sport-core", "tkl-sport-adapter-api", "tkl-sport-data-api", "tkl-sport-risk-api", "tkl-offline-api",
               "tkl-wallet-api", "tkl-pay-api", "tkl-order-api", "tkl-rec-api", "tkl-sport-bet-api",
               "tkl-module-starter", "tkl-open-sdk", "tkl-search-api", "tkl-distributor-api", "tkl-event-api",
               "tkl-game-api", "tkl-lotto-api", "tkl-common-business", "tkl-cms-service", "tkl-tool-service",
               "tkl-user-service", "tkl-wallet-service", "tkl-order-service", "tkl-search-service",
               "tkl-statistics-api", "tkl-sport-bet-service", "tkl-lotto", "tkl-statistics", "tkl-event", "tkl-pay",
               "tkl-platform-engine", "tkl-archive", "tkl-game", "tkl-agent", "tkl-lottery-manager", "tkl-game-manager",
               "tkl-message", "tkl-h5-api", "tkl-open-api", "tkl-gateway", "shop-sales", "tkl-data-api", "tkl-sale-api",
               "tkl-riskctl-api", "tkl-dis-api", "tkl-lotto-daemon", "tkl-lotto-manager",
               "tkl-sport-risk-service", "tkl-sport-bet-engine", "tkl-sport-manager", "sport-bet-strategy",
               "sports-user-statistics", "sports-odds", "odds-model", "tkl-sport-data-adapter", "tkl-collector-bet365",
               "tkl-sport-data-service", "tkl-sport-data-engine", "tkl-tx", "tkl-riskctl-service", "tkl-data",
               "tkl-offline-service", "tkl-proxy-service", "tkl-distributor-service", "tkl-tx-center"]

# all_project = ['tkl-h5-api', 'tkl-platform-engine']
max_len = len(max(all_project, key=len))


def get_by_tag_startswith(ps, project_id, pick_date, pick_tag):
    results = []
    for page in range(1, 15):
        url = f'https://{ps.hostname}/api/v4/projects/{project_id}/pipelines?per_page=100&updated_after={pick_date}&page={page}&order_by=updated_at&sort=asc'
        resp = requests.get( url,headers=headers,
            cookies=cookie_util.get_cookies_from_chrome(ps.hostname))
        tags = resp.json()
        if len(tags) == 0:
            return results
        if pick_tag:
            result = [t for t in tags if t['ref'].startswith(pick_tag)]
        results = result + results
    return results


def query_jobs(projects, project_id, pipeline_id):
    job_url = f"{projects.gitlab_url}/api/v4/projects/{project_id}/pipelines/{pipeline_id}/jobs"
    pipeline_response = requests.get(job_url, cookies=get_cookies_from_chrome(projects.hostname))
    resp = pipeline_response.json()
    result = []
    for item in resp:
        job = job_info(str(item['id']), item['status'], item['stage'], item['name'], item['ref'],
                       item['pipeline']['web_url'])
        result.append(job)
    return result


def pick_command():
    parser = argparse.ArgumentParser()
    parser.add_argument('job', default=Env.get_task_name(sys.argv), help='the job name')
    parser.add_argument('--project', '-p',
                        help='project name (at repo in which your current location is), eg. tkl-h5-api')
    parser.add_argument('--date', '-d', default=datetime.datetime.now().strftime("%Y-%m-%d"),
                        help='pick date,format: yyyy-MM-dd')
    parser.add_argument('--tag', '-t', help='pick by tag')
    args = parser.parse_args()

    print("job_name", args.job)
    print("project", args.project)
    print("date", args.date)
    print("tag", args.tag)
    pick_tasks(args.job, args.project, args.date, args.tag)


def pick_tasks(job_name, pick_project, pick_date, pick_tag):
    ps = git_env.Env.get_git_repo()
    number = 0
    print(f"pick cicd [{ps.hostname}] to job name: {job_name}")
    existing_jobs = sqliteTool.query_by_job_name(job_name=job_name)
    existing_pipeline = [j.pipeline_id for j in existing_jobs]
    if not pick_project:
        pick_project = all_project
    print(f"pick project size:{len(pick_project)}")
    project_bar = tqdm([p for p in ps.projects if p.name in pick_project], position=0, leave=False)
    for p in project_bar:
        resps = get_by_tag_startswith(ps, p.id, pick_date, pick_tag)
        if resps:
            for resp in resps:
                web_url = resp['web_url']
                pipeline_id = os.path.basename(web_url)
                jobs = query_jobs(projects=ps, project_id=p.id, pipeline_id=pipeline_id)
                for j in jobs:
                    if pipeline_id in existing_pipeline:
                        continue
                    sqliteTool.insert_job(job_id=j.job_id, project_id=p.id, project_name=p.name,
                                          pipeline_id=pipeline_id,
                                          job_name=job_name, name=j.name, stage=j.stage, status=j.status,
                                          refer=resp['ref'],
                                          web_url=web_url, create_time=int(
                            datetime.datetime.strptime(resp['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()))
                    number += 1
        project_bar.set_description(f"[+{number}] {p.name}".ljust(max_len, ' '))

    print(f"picked all cicd: {number}")


if __name__ == '__main__':
    # pick_command()
    pick_tasks('test', 'tkl-h5-api', '2025-01-03', 'qauto-202501021634')
