import csv
import requests
from lxml import etree
from threading import Thread
from tkinter import messagebox
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"}

def login(url="https://steamdb.info/upcoming/free/"):
    try:
        html = requests.get(url,headers = headers)
        if html.status_code == 200:
            text = html.text
            dom = etree.HTML(text)
            return dom
        else:
            pass
    except:
        messagebox.showinfo("warning","warn Internet")
def now(dom):
    name = dom.xpath('//table[1]//a/b/text()')
    price = dom.xpath('//table[1]//td[4]/text()')
    start_time = dom.xpath('//table[1]//td[5]/@title')
    end_time = dom.xpath('//table[1]//td[6]/@title')
    for a,b,c,d in zip(name,price,start_time,end_time):
        name,price,start,end = replace(a,b,c,d)
        write_csv(name,price,start,end,"now.csv")
def furture(dom):
    name = dom.xpath('//table[2]//a/b/text()')
    price = dom.xpath('//table[2]//td[3]/text()')
    start_time = dom.xpath('//table[2]//td[4]/@title')
    end_time = dom.xpath('//table[2]//td[5]/@title')
    for a,b,c,d in zip(name,price,start_time,end_time):
        name,price,start,end = replace(a,b,c,d)
        write_csv(name,price,start,end,"furture.csv")
def replace(name,price,start,end):
    start = start.split("+")[0]
    end = end.split("+")[0]
    if price != "Weekend":
        name = name.split("Limited")[0]
        price = "Free"
    else:
        name = name.split("Free")[0]
    return name,price,start,end
def write_csv(name,price,start,end,csv_name):
    with open(csv_name,"a",newline="") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([name,price,start,end])
    print(name,price,start,end)
if __name__ == "__main__":
    threads = []
    dom = login()
    threads.append(Thread(target=now,args=(dom,)))
    threads.append(Thread(target=furture,args=(dom,)))
    for thread in threads:
        thread.start()
        thread.join()
