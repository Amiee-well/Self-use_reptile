import requests
from lxml import etree
import random
headers = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
def response(url):
    html = requests.get(url,headers=headers)
    if html.status_code == 200:
        text = html.text
        return text
    else:
        print("请求失败")
def get_ip_list(url):
    text = response(url)
    dom = etree.HTML(text)
    mlist = []
    ip_ids = dom.xpath('//*[@id="ip_list"]/tr[/]/td[2]//text()')
    port_ids = dom.xpath('//*[@id="ip_list"]/tr[/]/td[3]//text()')
    type_ids = dom.xpath('//*[@id="ip_list"]/tr[/]/td[6]//text()')
    for a,b,c in zip(ip_ids,port_ids,type_ids):
        mlist.append(c+"  http://"+a+":"+b)
    return mlist
def get_random_ip(url):
    ip_list = get_ip_list(url)
    proxies = {}
    while True:
        chor = random.choice(ip_list)
        ip = chor.split("  ")
        if ip[0] == "HTTPS":
            proxies[ip[0]] = ip[1]
            break
    while True:
            chor = random.choice(ip_list)
            ip = chor.split("  ")
            if ip[0] == "HTTP":
                proxies[ip[0]] = ip[1]
                break
    return proxies
if __name__ == "__main__":
    url = "https://www.xicidaili.com/nn/"
    proxies = get_random_ip(url)
    print("proxies = ",proxies)
