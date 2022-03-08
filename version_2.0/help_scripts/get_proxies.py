import traceback

import requests
import json
import random


def get_all_proxies():
    response = requests.get(
        'https://api.proxyscrape.com/v2/account/datacenter_shared/proxy-list?auth=ya1slvtaoybog0ylj6uw&type=getproxies&country[]=all&protocol=http&format=json&status=all').json()

    return response


def randomize_proxy_choice(proxies):
    proxies_to_return = []
    max_number = len(proxies) - 1

    while len(proxies_to_return) < 10:
        try:
            index = random.randint(0, max_number)
            proxy = proxies.pop(index)
            proxies_to_return.append(proxy)
            max_number -= 1
        except:
            print(traceback.print_exc())
        finally:
            pass

    return proxies_to_return


def get_ten_and_check_online():
    all_proxies = get_all_proxies()['data']
    for proxy in all_proxies:
        if proxy[2] != 'Online':
            index = all_proxies.index(proxy)
            all_proxies.pop(index)

    proxy_list_to_use = randomize_proxy_choice(all_proxies)

    return proxy_list_to_use







