import json

import pkg_resources


def get_config():
    config_path = pkg_resources.resource_filename('git_tools', 'config/git-project-config.json')

    with open(config_path) as config:
        return json.loads(config.read())
