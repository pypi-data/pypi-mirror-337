import requests
from joblib import Memory

from git_tools import cookie_util

memory = Memory(location="~/.cache")


class GProject:
    def __init__(self, id, name, web_url):
        self.id = id
        self.name = name
        self.web_url = web_url


class GitRepo:
    def __init__(self, hostname):
        self.hostname = hostname
        self.gitlab_url = f"https://{hostname}"
        self.projects = load_projects(hostname)
        self.id_mapping = {p.id: p for p in self.projects}
        self.name_mapping = {p.name: p for p in self.projects}


@memory.cache
def load_projects(domain):
    cookie = cookie_util.get_cookies_from_chrome(domain)
    result = []
    for i in range(1, 100):
        url = f"https://{domain}/api/v4/projects?per_page=100&page={i}"
        resp = requests.get(url, cookies=cookie)
        if len(resp.json()) == 0:
            return result
        p = [GProject(p['id'], p['name'].strip(), p['web_url']) for p in resp.json()]
        result = result + p
    return result


if __name__ == '__main__':
    # grepo = GitRepo('codelab001.xyz')
    grepo = GitRepo('gitlab.mcorp.work')
    print(grepo.name_mapping.get("tkl-h5-api").id)

    # p = load_projects('codelab001.xyz')
    # print(p)

