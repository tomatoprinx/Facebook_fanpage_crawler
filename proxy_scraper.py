import json
import requests
import time
import pickle
from random import randint
from bs4 import BeautifulSoup
from requests.exceptions import ProxyError

response = requests.get('https://www.us-proxy.org/')
# print(response.text)

def parse(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    trs = soup.select("#proxylisttable tr")
    proxies = []
    for tr in trs:
        tds = tr.select("td")
        if len(tds)>6:
            ip = tds[0].text
            port = tds[1].text
            anonymity = tds[4].text
            ifScheme = tds[6].text
            if ifScheme == 'yes': 
                scheme = 'https'
            else: scheme = 'http'
            proxy = "%s://%s:%s"%(scheme, ip, port)
            meta = {
                'port': port,
                'proxy': proxy,
                '_proxy_scheme': scheme,
                '_proxy_ip': ip
            }
            proxies.append(meta)
    print(len(proxies), ' proxies found.')
    return proxies

def proxy_check_available(proxies):
    proxy_available = []
    for proxy in proxies:
        proxy_dict = {proxy['_proxy_scheme']: proxy['proxy']}
        try:
            resp = requests.get('https://httpbin.org/ip', proxies=proxy_dict)
            print(resp.text)
            resp_ip = json.loads(resp.text)['origin'].split(',')[0]
            if proxy['_proxy_ip'] == resp_ip:
                print(proxy['proxy'], ' is available.')
                proxy_available.append(proxy_dict)
            time.sleep(1)
        except ProxyError:
            print('OOPS!! Proxy error. Try another one.')
            continue
    print(len(proxy_available), ' proxies are available.')
    return proxy_available

"""
proxies = [{
    'port': '1234',
    'proxy': 'https://142.93.xxx.xxx:1234',
    '_proxy_scheme': 'https',
    '_proxy_ip': '142.93.xxx.xxx'}]
"""
proxies = parse(response)
print('Examine availability...')
# pxy_list = []
# for pxy in proxies:
#     pxy_list.append(pxy['proxy'])

proxy_list = proxy_check_available(proxies)
print(proxy_list)

# pickle save
with open('proxy_files/proxy_lists.pickle', 'wb')as file:
    pickle.dump(proxy_list, file)
file.close()