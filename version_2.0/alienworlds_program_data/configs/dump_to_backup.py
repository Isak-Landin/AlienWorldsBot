import requests
import json

response = requests.get('https://api.proxyscrape.com/v2/account/datacenter_shared/proxy-list?auth=ya1slvtaoybog0ylj6uw&type=getproxies&country[]=all&protocol=http&format=json&status=all').json()

with open('backup_proxy.json', 'w+') as file:
    json.dump(response, file, indent=4)
