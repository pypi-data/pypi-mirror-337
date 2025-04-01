#!/usr/bin/env python3
from git_tools.gitrepo import GitRepo

domain = 'gitlab.mcorp.work'

if __name__ == "__main__":
    pro = GitRepo('gitlab.mcorp.work')
    print(len(pro.projects))
    # for p in pro.projects:
    #     print(p.id, p.name, p.web_url)

    for k, v in pro.name_mapping.items():
        print(k)
        print(f"'{v.id}','{v.name}','{v.web_url}'")
    print("=" * 11)
    print(f"'{pro.id_mapping[436].name}'")
    print(pro.name_mapping["tkl-h5-api"].name)
    print(pro.name_mapping["tkl-module-starter"].name)
