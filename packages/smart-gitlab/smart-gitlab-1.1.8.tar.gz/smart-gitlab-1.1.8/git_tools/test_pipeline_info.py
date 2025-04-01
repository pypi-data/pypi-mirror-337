# curl --header "Private-Token: your_access_token" "https://gitlab.com/api/v4/groups/123/projects?per_page=100"
import json
import re

import requests
import git
from git_tools import cookie_util
from urllib.parse import urlparse

from git_tools.gitrepo import GitRepo

ps = GitRepo('gitlab.mcorp.work')
all_project = ["tkl-pom", "tkl-core", "tkl-component", "tkl-cms-api", "tkl-user-api", "tkl-tool-api", "tkl-base-api",
               "tkl-sport-core", "tkl-sport-adapter-api", "tkl-sport-data-api", "tkl-sport-risk-api", "tkl-offline-api",
               "tkl-wallet-api", "tkl-pay-api", "tkl-order-api", "tkl-rec-api", "tkl-sport-bet-api",
               "tkl-module-starter", "tkl-open-sdk", "tkl-search-api", "tkl-distributor-api", "tkl-event-api",
               "tkl-game-api", "tkl-lotto-api", "tkl-common-business", "tkl-cms-service", "tkl-tool-service",
               "tkl-user-service", "tkl-wallet-service", "tkl-order-service", "tkl-search-service",
               "tkl-statistics-api", "tkl-sport-bet-service", "tkl-lotto", "tkl-statistics", "tkl-event", "tkl-pay",
               "tkl-platform-engine", "tkl-archive", "tkl-game", "tkl-agent", "tkl-lottery-manager", "tkl-game-manager",
               "tkl-message", "tkl-h5-api", "tkl-open-api", "tkl-gateway", "shop-sales", "tkl-data-api", "tkl-sale-api",
               "tkl-riskctl-api", "tkl-distributor-api", "tkl-lotto-daemon", "tkl-lotto-manager",
               "tkl-sport-risk-service", "tkl-sport-bet-engine", "tkl-sport-manager", "sport-bet-strategy",
               "sports-user-statistics", "sports-odds", "odds-model", "tkl-sport-data-adapter", "tkl-collector-bet365",
               "tkl-sport-data-service", "tkl-sport-data-engine", "tkl-tx", "tkl-riskctl-service", "tkl-data",
               "tkl-offline-service", "tkl-proxy-service", "tkl-distributor-service", "tkl-tx-center"]


def get_by_tag(tag_id, project_id):
    for page in range(1, 15):
        resp = requests.get(
            f'https://{ps.hostname}/api/v4/projects/{project_id}/pipelines?per_page=100&page={page}',
            cookies=cookie_util.get_cookies_from_chrome(ps.hostname))
        tags = resp.json()
        if len(tags) == 0:
            return
        results = [t for t in tags if t['ref'].startswith(tag_id)]
        if len(results) > 0:
            return results[0]


def pipelines(tag_id):
    for p in ps.projects:
        if p.name not in all_project:
            continue
        resp = get_by_tag(tag_id, p.id)
        if resp:
            repo =git.Repo(f'/Users/xuwuqiang/Documents/workspace/game/{p.name}',search_parent_directories=True)
            v = repo.rev_parse("HEAD")
            remote_v = resp['sha']
            print(p.name, resp['web_url'], resp['status'],f'ok:{v.hexsha}' if v.hexsha == remote_v else f'error:{v.hexsha,remote_v}')
        else:
            print(p.name, p.id, 'not found')


if __name__ == '__main__':
    # pipelines(tag_id='7prd-')
    pipelines(tag_id='gwwq1-')
