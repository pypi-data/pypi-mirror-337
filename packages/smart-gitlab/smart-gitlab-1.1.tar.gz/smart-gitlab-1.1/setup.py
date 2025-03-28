from setuptools import setup, find_packages

setup(
    name="smart-gitlab",
    version="1.1",
    keywords=("gitlab", "deploy", "cicd"),
    description="gitlab sdk",
    long_description="tools for gitlab with python",
    license="MIT Licence",

    url="https://xxx.com",
    author="xuwuqiang",
    author_email="xwqiang2008@outlook.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["browser_cookie3==0.20.1",
                      "GitPython==3.1.44",
                      "joblib==1.4.2",
                      "onetimepass==1.0.1",
                      "prettytable==3.16.0",
                      "pycookiecheat==0.8.0",
                      "Requests==2.32.3",
                      "setuptools==65.6.3",
                      "tqdm==4.66.2"],

    scripts=[],
    # 如果出现 ModuleNotFoundError: No module named,用 py_modules
    py_modules=[],
    entry_points={
        'console_scripts': [
            'ci = git_tools.git_push_tag:tag_command',
            'pick = git_tools.git_pick_task:pick_command',
            'task = git_tools.git_list_task:task_command',
            'h = git_tools.git_home_page:page_pipeline_command',
            'merge = git_tools.git_home_page:page_merge_command',
            'addHook = git_hooks.git_hook:add_hook_command',
            'fcommit = git_hooks.git_hook:force_commit_command',
            'branches = branches.branch_ops:git_branches_command',
            'currbranch = branches.branch_ops:git_current_branch_command',
            'gcheckout = branches.branch_ops:git_checkout_branch_command',
            'repolist = branches.branch_ops:git_repolist_command',
            'prepull = branches.branch_ops:git_prepull_command',
            'gstatus = branches.branch_ops:git_status_command',
            'git-logs = branches.branch_ops:git_log_command',
            'git-extract = branches.branch_ops:git_extract_pull_command',
            'vpn=vpn.otputils:vpn_command'
        ]
    }
)
