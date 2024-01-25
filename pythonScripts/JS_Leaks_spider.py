import requests
from termcolor import colored as cl

target = open('JS.txt', 'r').read().split('\n')

def Extract(url):
    try:
        req = requests.get(url).text
        sen = ['username=', 'email=', 'api=', 'password=','secret=','key=','db_username']
        for s in sen:
            if s in req:
                print(cl(f"{s} in {url}", color='red'))
            else:
                pass
    except Exception as e:
        print(e)
    
for url in target:
    Extract(url)
