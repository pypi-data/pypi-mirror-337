from setuptools import setup, find_packages

setup(
    name="smart-gitlab",
    version="1.0.1",
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

    }
)
