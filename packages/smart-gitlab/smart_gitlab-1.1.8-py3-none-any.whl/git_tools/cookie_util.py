from pycookiecheat import BrowserType, get_cookies
import requests

"""
目前能破解的Chrome最高版本： 130.0.6723.91
请禁用Chrome升级，否则高版本不能保证获取cookie信息
如遇到不兼容问题，考虑升级从最新代码中升级pycookiecheat版本：
python -m pip install git+https://github.com/n8henrie/pycookiecheat@master
"""

def get_cookies_from_chrome(domain):
    url = f"https://{domain}"
    cookies = get_cookies(url)
    r = requests.get(url, cookies=cookies)
    return get_cookies(url, browser=BrowserType.CHROME)

if __name__ == '__main__':
    c = get_cookies_from_chrome('gitlab.mcorp.work')
    # c = get_cookie_from_browser('chrome','gitlab.mcorp.work')

    for k, v in c.items():
        print(k, v)