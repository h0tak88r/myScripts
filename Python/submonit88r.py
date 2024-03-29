#!/usr/bin/env python3
import sys
import argparse
import requests
from bs4 import BeautifulSoup
import json
import time
import sqlite3
from discord_webhook import DiscordWebhook
import urllib3

# Disable urllib3 warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
DB_FILE = "subdomains_database.db"


def parser_error(errmsg):
    print("Usage: python3 " + sys.argv[0] + " [Options] use -h for help")
    print("Error: " + errmsg)
    sys.exit()


def parse_args():
    parser = argparse.ArgumentParser(epilog='\tExample: \r\npython3 ' + sys.argv[0] + " -l domains.txt")
    parser.error = parser_error
    parser._optionals.title = "OPTIONS"
    parser.add_argument('-l', '--domain_list', help='Specify a file containing a list of domains', required=True)
    parser.add_argument('-m', '--monitor', help='Monitor subdomains and send updates to Discord', action='store_true',
                        required=False)
    parser.add_argument('-w', '--webhook', help='Specify the Discord webhook URL', required=False)
    return parser.parse_args()


def init_database():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS subdomains (subdomain TEXT)''')
        conn.commit()
        conn.close()
        print("[+] Database initialized successfully.")
    except Exception as e:
        print(f"[!] Error initializing the database: {e}")


def add_subdomains_to_db(subdomains):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        for subdomain in subdomains:
            cursor.execute("INSERT INTO subdomains (subdomain) VALUES (?)", (subdomain,))
        conn.commit()
        conn.close()
        print(f"[+] Added {len(subdomains)} subdomains to the database.")
    except Exception as e:
        print(f"[!] Error adding subdomains to the database: {e}")


def get_subdomains_from_db():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT subdomain FROM subdomains")
        subdomains = set(row[0] for row in cursor.fetchall())
        conn.close()
        print("[+] Retrieved subdomains from the database.")
        return subdomains
    except Exception as e:
        print(f"[!] Error retrieving subdomains from the database: {e}")
        return set()


def fetch_subdomains_from_crtsh(domain):
    subdomains = set()
    wildcard_subdomains = set()
    url = f"https://crt.sh/?q={domain}&output=json"
    print(f"[#] Fetching Subdomains from crt.sh for {domain}")

    try:
        response = requests.get(url, timeout=25)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        content = response.content.decode('UTF-8')

        if content:
            soup = BeautifulSoup(content, 'lxml')
            try:
                json_data = json.loads(soup.text)
                for entry in json_data:
                    name_value = entry.get('name_value', '')
                    if '\n' in name_value:
                        subname_value = name_value.split('\n')
                        for subname in subname_value:
                            subname = subname.strip()  # Remove leading/trailing spaces
                            if subname and '*' in subname:
                                wildcard_subdomains.add(subname)
                            elif subname:
                                subdomains.add(subname)
            except json.JSONDecodeError as e:
                print(f"[!] Error decoding JSON for domain {domain} from {url} ")

    except requests.exceptions.RequestException as e:
        print(f"[!] Error fetching subdomains for domain {domain} from {url}")

    return subdomains, wildcard_subdomains


def send_to_discord(webhook_url, message):
    print(f"[+] Sending New subdomains (if exists) to your Discord Server")

    if webhook_url:
        max_length = 2000
        chunks = [message[i:i + max_length] for i in range(0, len(message), max_length)]

        for chunk in chunks:
            webhook = DiscordWebhook(url=webhook_url, content=chunk)
            webhook.execute()


def fetch_subdomains_from_alienvault(domain):
    url = f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/passive_dns"
    print(f"[#] Fetching Subdomains from otx.alienvault.com for {domain}")

    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors

        data = response.json()

        if "passive_dns" in data:
            subdomains = [entry["hostname"] for entry in data["passive_dns"] if "hostname" in entry]
            return subdomains
        else:
            print("[X] No passive DNS data found.")
            return []

    except requests.exceptions.RequestException as e:
        print(f"[!] Error fetching data from {url}: {e}")
        return []


def fetch_subdomains_from_urlscan(domain):
    url = f"https://urlscan.io/api/v1/search/?q={domain}"
    print(f"[#] Fetching Subdomains from urlscan.io for {domain}")

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if "results" in data:
            subdomains = [entry["domain"] for entry in data["results"] if "domain" in entry]
            return subdomains
        else:
            print("[X] No subdomains Found")
    except requests.exceptions.RequestException as e:
        print(f"[!] Error fetching data from {url}: {e}")
        return []


def fetch_subdomains_from_anubis(domain):
    url = f"https://jldc.me/anubis/subdomains/{domain}"
    print(f"[#] Fetching Subdomains from anubis for {domain}")

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
        print(f"[!] Error Getting subdomains from {url}: {e}")
        return []


def fetch_subdomains_from_hackertarget(domain):
    url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
    print(f"[#] Fetching Subdomains from hackertarget.com for {domain}")

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.text

        if data:
            subdomains = [line.split(",")[0] for line in data.splitlines()]
            return subdomains
        else:
            print("[X] No subdomains Found")
            return []

    except requests.exceptions.RequestException as e:
        print(f"[!] Error fetching data from {url}: {e}")
        return []


# Function for getting subdomains from rapiddns.io
def rapiddns(domain):
    url = f"https://rapiddns.io/subdomain/{domain}?full=1#result"
    print(f"[#] Fetching Subdomains from rapiddns.io for {domain}")

    try:
        page = requests.get(url, verify=False)
        soup = BeautifulSoup(page.text, 'lxml')

        subdomains = []
        website_table = soup.find("table", {"class": "table table-striped table-bordered"})

        if website_table:
            website_table_items = website_table.find_all('tbody')
            for tbody in website_table_items:
                tr = tbody.find_all('tr')
                for td in tr:
                    subdomain = td.find_all('td')[0].text.strip()
                    subdomains.append(subdomain)
        else:
            print("[X] No table element found on the page.")

        return subdomains

    except requests.RequestException as e:
        print(f"[!] Error Getting subdomains from {url}: {e}")
        return []

def main():
    print('''
                __                   _ __  ___  ___     
      ___ __ __/ /  __ _  ___  ___  (_) /_( _ )( _ )____
     (_-</ // / _ \/  ' \/ _ \/ _ \/ / __/ _  / _  / __/
    /___/\_,_/_.__/_/_/_/\___/_//_/_/\__/\___/\___/_/   

                                  By SALLAM (h0tak88r)
    ''')

    args = parse_args()
    init_database()

    if args.monitor:
        while True:
            try:
                with open(args.domain_list, 'r') as domains_file:
                    domains = domains_file.read().splitlines()

                all_subdomains = set()
                all_wildcard_subdomains = set()

                for domain in domains:
                    subdomains, wildcard_subdomains = fetch_subdomains_from_crtsh(domain)
                    all_subdomains.update(subdomains)
                    all_wildcard_subdomains.update(wildcard_subdomains)

                    # Get subdomains from AlienVault OTX
                    otx_subdomains = fetch_subdomains_from_alienvault(domain)
                    all_subdomains.update(otx_subdomains)

                    # Get subdomains from urlscan.io
                    urlscan_subdomains = fetch_subdomains_from_urlscan(domain)
                    all_subdomains.update(urlscan_subdomains)

                    # Get subdomains from anubis
                    anubis_subdomains = fetch_subdomains_from_anubis(domain)
                    all_subdomains.update(anubis_subdomains)

                    # Get subdomains from hackertarget
                    hackertarget_subdomains = fetch_subdomains_from_hackertarget(domain)
                    all_subdomains.update(hackertarget_subdomains)

                    # Get subdomains from rapiddns.io
                    rapiddns_subdomains = fetch_subdomains_from_rapiddns(domain)
                    all_subdomains.update(rapiddns_subdomains)

                # Load old subdomains from the database
                old_subdomains = get_subdomains_from_db()

                # Find new subdomains
                new_subdomains = all_subdomains - old_subdomains

                # Send new subdomains to Discord
                if new_subdomains:
                    message = f"[+] New Subdomains found: {', '.join(new_subdomains)}"
                    send_to_discord(args.webhook, message)

                    # Add the new subdomains to the database
                    add_subdomains_to_db(new_subdomains)

                    # Wait for 5 hours before the next iteration
                    time.sleep(5 * 60 * 60)

            except Exception as e:
                print(f"[!] An error occurred: {e}")

    else:
        with open(args.domain_list, 'r') as domains_file:
            domains = domains_file.read().splitlines()

        all_subdomains = set()
        all_wildcard_subdomains = set()

        for domain in domains:
            subdomains, wildcard_subdomains = fetch_subdomains_from_crtsh(domain)
            all_subdomains.update(subdomains)
            all_wildcard_subdomains.update(wildcard_subdomains)

            # Get subdomains from AlienVault OTX
            otx_subdomains = fetch_subdomains_from_alienvault(domain)
            all_subdomains.update(otx_subdomains)

            # Get subdomains from urlscan.io
            urlscan_subdomains = fetch_subdomains_from_urlscan(domain)
            all_subdomains.update(urlscan_subdomains)

            # Get subdomains from anubis
            anubis_subdomains = fetch_subdomains_from_anubis(domain)
            all_subdomains.update(anubis_subdomains)

            # Get subdomains from hackertarget
            hackertarget_subdomains = fetch_subdomains_from_hackertarget(domain)
            all_subdomains.update(hackertarget_subdomains)

            # Get subdomains from rapiddns.io
            rapiddns_subdomains = fetch_subdomains_from_rapiddns(domain)
            all_subdomains.update(rapiddns_subdomains)

        # Load old subdomains from the database
        old_subdomains = get_subdomains_from_db()

        # Find new subdomains
        new_subdomains = all_subdomains - old_subdomains

        # Add the new subdomains to the database
        add_subdomains_to_db(new_subdomains)

    with open('Results.txt', 'w') as file:
        file.write('\n'.join(all_subdomains))

    print("[+] Subdomains Enumeration completed, Results are saved in Results.txt.")


if __name__ == "__main__":
    main()