from setuptools import setup, find_packages

setup(
    name="smart-gitlab",
    version="1.0",
    keywords=("git_tools", "deploy"),
    description="gitlab sdk",
    long_description="tools for gitlab with python",
    license="MIT Licence",

    url="https://xxx.com",
    author="xuwuqiang",
    author_email="wuqiang@test.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["requests"],

    scripts=[],
    # 如果出现 ModuleNotFoundError: No module named,用 py_modules
    py_modules=[],
    entry_points={
        'console_scripts': [
            'ci = git_tools.git_push_tag:tag_command',
            'pick = git_tools.git_pick_task:pick_command',
            'tsk = git_tools.git_list_task:task_command',
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
