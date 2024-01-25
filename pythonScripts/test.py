import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


# Getting subdomains from anubis 
def anubis(domain):
    url = f"https://jldc.me/anubis/subdomains/{domain}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        subdomains = response.json()

        if isinstance(subdomains, list):
            return subdomains
        else:
            print(f"Anubis response for {domain} is not in the expected format.")
            return []

    except requests.RequestException as e:
        print(f"Error Getting subdomains from {url}: {e}")
        return []


subs = anubis("wurl.com")
print(subs)