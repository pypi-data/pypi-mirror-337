#!/usr/bin/env python3
from git_tools.gitrepo import GitRepo

domain = 'gitlab.mcorp.work'

if __name__ == "__main__":
    pro = GitRepo('gitlab.mcorp.work')
    # pro = GitRepo('codelab001.xyz')
    print(len(pro.projects))
    # for p in pro.projects:
    #     print(p.id, p.name, p.web_url)

    for k, v in pro.name_mapping.items():
        print(k)
        print(f"'{v.id}','{v.name}','{v.web_url}'")
    print(pro.name_mapping["muscle-service-inner"].name)
