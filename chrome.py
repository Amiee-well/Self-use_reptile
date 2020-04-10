import os
import requests
from lxml import etree
page = 1
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"}
def login(url):
    html = requests.get(url,headers=headers)
    html.encoding = "utf-8"
    if html.status_code == 200:
        text = html.text
        return text
    else:
        return
def xpaths(url= "http://www.58xueba.com/theme/anime/index.html"):
    global page
    if os.path.exists("page.txt"):
        with open("page.txt","r") as f:
            page = f.readline()
            print("正在下载第{}页".format(page))
            text = login("http://www.58xueba.com/theme/anime/index_{}.html".format(page))
            page = int(page)
    else:
        print("正在下载第{}页".format(page))
        text = login(url)
    dom = etree.HTML(text)
    img = dom.xpath('//div[@class="item col-md-4 col-sm-6"]//img/@src')
    home = dom.xpath('//div[@class="item col-md-4 col-sm-6"]/a/@href')
    next_url = dom.xpath('//div[@class="pageNo"]/a/@href')[-1]
    for m,n in zip(img,home):
        text = login(n)
        dom = etree.HTML(text)
        try:
            url_home = dom.xpath('//p/a/@href')[0].split("/")[-2]
            write_png(m,url_home)
        except Exception as err:
            write_err(err)
    page += 1
    write_page(page)
    xpaths(next_url)
def write_png(pic,url):
    create_url(r"picture")
    contents = requests.get(pic,headers=headers).content
    with open(r"./picture/{}.png".format(url),"wb") as f:
        f.write(contents)
def write_err(err):
    with open("err.txt","a") as f:
        f.write(str(err))
def create_url(name):
    if not os.path.exists(name):
        os.mkdir(name)
        with open("{}/download.txt".format(name),"w") as f:
            f.write("图片名称为数字链接\n请进入如下浏览器进行下载\nhttps://www.themebeta.com/chrome/theme/()/download")
def write_page(page):
    with open("page.txt","w") as f:
        f.write(str(page))
if __name__ == "__main__":
    xpaths()
