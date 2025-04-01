import re

import requests

from git_tools.config_utils import get_config
from git_tools.cookie_util import get_cookies_from_chrome
from git_tools.job_info import job_info

headers = get_config()['default_http_header']


def query_pipeline(grepo, project_id, pipeline_id):
    pipeline_url = f"{grepo.gitlab_url}/api/v4/projects/{project_id}/pipelines/{pipeline_id}"
    pipeline_response = requests.get(pipeline_url, headers=headers, cookies=get_cookies_from_chrome(grepo.hostname))
    resp = pipeline_response.json()
    web_url = re.sub('http://13.229.25.115', 'https://codelab001.xyz', resp["web_url"])

    return resp["status"], resp["ref"], web_url


def query_jobs(domain, project_id, pipeline_id):
    job_url = f"https://{domain}/api/v4/projects/{project_id}/pipelines/{pipeline_id}/jobs"
    pipeline_response = requests.get(job_url, headers=headers, cookies=get_cookies_from_chrome(domain))
    resp = pipeline_response.json()
    result = []
    for item in resp:
        job = job_info(str(item['id']), item['status'], item['stage'], item['name'], item['ref'],
                       item['pipeline']['web_url'], item['commit']['id'])
        result.append(job)
    return result


def search_jobs(grepo, project_id, pipeline_id):
    job_url = f"{grepo.gitlab_url}/api/v4/projects/{project_id}/pipelines/{pipeline_id}/jobs"
    pipeline_response = requests.get(job_url, headers=headers, cookies=get_cookies_from_chrome(grepo.hostname))
    resp = pipeline_response.json()
    result = []
    for item in resp:
        job = job_info(str(item['id']), item['status'], item['stage'], item['name'], item['ref'],
                       item['pipeline']['web_url'], item['commit']['id'])
        result.append(job)
    return result
