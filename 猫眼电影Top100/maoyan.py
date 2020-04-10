import time
import json
import re
import requests
from requests.exceptions import RequestException
def get_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == requests.codes.ok:
            return response.text
        return None
    except RequestException:
        return None
def parse_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield{
            '电影排名': item[0],
            '电影图片': item[1],
            '电影名称': item[2].strip(),
            '演员': item[3].strip()[3:] if len(item[3]) > 3 else '',
            '上映时间': item[4].strip()[5:] if len(item[4]) > 5 else '',
            '评分': item[5].strip() + item[6].strip()
        }
def save_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
if __name__ == '__main__':
    for i in range(0, 100, 10):
        url = 'http://maoyan.com/board/4?offset=' + str(i)
        html = get_page(url)
        for item in parse_page(html):
            print(item)
            save_file(item)
        time.sleep(2)
