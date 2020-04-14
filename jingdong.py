import os
import time
import pickle
import random
from DecryptLogin import login
from pyecharts import options
from pyecharts.globals import ThemeType
from pyecharts.charts import Bar, Pie, Funnel

class JDGoodsCrawler():
    def __init__(self, **kwargs):
        if os.path.isfile('session.pkl'):
            print('[INFO]: 检测到已有会话文件session.pkl, 将直接导入该文件...')
            self.session = pickle.load(open('session.pkl', 'rb'))
            self.session.headers.update({'Referer': ''})
        else:
            self.session = JDGoodsCrawler.login()
            f = open('session.pkl', 'wb')
            pickle.dump(self.session, f)
            f.close()
    def run(self):
        search_url = 'https://search-x.jd.com/Search?'
        while True:
            goods_name = input('请输入想要抓取的商品信息名称: ')
            goods_infos_dict = {}
            page_interval = random.randint(1, 5)
            page_count = 1
            page_pointer = 1
            while True:
                params = {
                            'area': '15',
                            'enc': 'utf-8',
                            'keyword': goods_name,
                            'adType': '7',
                            'page': str(page_count),
                            'ad_ids': '291:19',
                            'xtest': 'new_search',
                            '_': str(int(time.time()*1000))
                        }
                response = self.session.get(search_url, params=params)
                if (response.status_code != 200):
                    break
                response_json = response.json()
                all_items = response_json.get('291', [])
                if len(all_items) == 0:
                    break
                for item in all_items:
                    goods_infos_dict.update({len(goods_infos_dict)+1: 
                                                {
                                                    'image_url': item.get('image_url', ''),
                                                    'price': item.get('pc_price', ''),
                                                    'shop_name': item.get('shop_link', {}).get('shop_name', ''),
                                                    'num_comments': item.get('comment_num', ''),
                                                    'link_url': item.get('link_url', ''),
                                                    'color': item.get('color', ''),
                                                    'title': item.get('ad_title', ''),
                                                    'self_run': item.get('self_run', ''),
                                                    'good_rate': item.get('good_rate', '')
                                                }
                                            })
                self.__save(goods_infos_dict, goods_name+'.pkl')
                page_count += 1
                page_pointer += 1
                if page_pointer == page_interval:
                    time.sleep(random.randint(50, 60)+random.random()*10)
                    page_interval = random.randint(2, 5)
                    page_pointer = 0
                else:
                    time.sleep(random.random()+1)
            print('[INFO]: 关于%s的商品数据抓取完毕, 共抓取到%s条数据...' % (goods_name, len(goods_infos_dict)))
            return goods_name
    def __save(self, data, savepath):
        fp = open(savepath, 'wb')
        pickle.dump(data, fp)
        fp.close()
    @staticmethod
    def login():
        lg = login.Login()
        infos_return, session = lg.jingdong()
        return session
    
def checkDir(dirpath):
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
        return False
    return True

def drawPie(title, data, savedir='./results'):
    checkDir(savedir)
    pie = (Pie(init_opts=options.InitOpts(theme=ThemeType.VINTAGE))
          .add('', [list(item) for item in data.items()], radius=['30%', '75%'], center=['50%', '50%'], rosetype='radius')
          .set_global_opts(title_opts=options.TitleOpts(title=title, pos_left='center'), legend_opts=options.LegendOpts(orient='vertical', pos_top='5%', pos_left='2%')))
    pie.render(os.path.join(savedir, title+'.html'))
    
def drawBar(title, data, savedir='./results'):
    checkDir(savedir)
    bar = (Bar(init_opts=options.InitOpts(theme=ThemeType.VINTAGE))
          .add_xaxis(list(data.keys()))
          .add_yaxis('', list(data.values()))
          .set_global_opts(xaxis_opts=options.AxisOpts(axislabel_opts=options.LabelOpts(rotate=-15)),
                           title_opts=options.TitleOpts(title=title, pos_left='center'), legend_opts=options.LegendOpts(orient='vertical', pos_top='15%', pos_left='2%')))
    bar.render(os.path.join(savedir, title+'.html'))

def drawFunnel(title, data, savedir='./results'):
    checkDir(savedir)
    funnel = (Funnel(init_opts=options.InitOpts(theme=ThemeType.MACARONS))
             .add('', [list(item) for item in data.items()], label_opts=options.LabelOpts(position="inside"))
             .set_global_opts(title_opts=options.TitleOpts(title=title, pos_left='center'), legend_opts=options.LegendOpts(orient='vertical', pos_top='15%', pos_left='2%')))
    funnel.render(os.path.join(savedir, title+'.html'))

def draw(name):
    goods_infos_dict = pickle.load(open('{}.pkl'.format(name), 'rb'))
    data = {'自营店': 0, '非自营店': 0}
    for key, value in goods_infos_dict.items():
        if value['self_run']:
            data['自营店'] += 1
        else:
            data['非自营店'] += 1
    drawPie('自营店与非自营店比例', data)
    data = {}
    for key, value in goods_infos_dict.items():
        if not value['shop_name'] or not value['good_rate']:
            continue
        data[value['shop_name']] = [int(value['num_comments']), int(value['good_rate'])]
    data_gr = dict(sorted(data.items(), key=lambda item: item[1][1])[:10])
    data_ct = dict(sorted(data.items(), key=lambda item: -item[1][0])[:10])
    data_gr_filter = {}
    for key, value in data_gr.items():
        data_gr_filter[key] = value[0]
    data_ct_filter = {}
    for key, value in data_ct.items():
        data_ct_filter[key] = value[0]
    drawBar('商品排名前10的店的商品评论数量', data_gr_filter)
    drawBar('评论排名前10的店铺', data_ct_filter)
    data = {'100元以内': 0, '100-300元': 0, '300-500元': 0, '500-1000元': 0, '1000-2000元': 0, '2000元以上': 0}
    for key, value in goods_infos_dict.items():
        price = float(value['price'])
        if price < 100:
            data['100元以内'] += 1
        elif price >= 100 and price < 300:
            data['100-300元'] += 1
        elif price >= 300 and price < 500:
            data['300-500元'] += 1
        elif price >= 500 and price < 1000:
            data['500-1000元'] += 1
        elif price >= 1000 and price < 2000:
            data['1000-2000元'] += 1
        elif price >= 2000:
            data['2000元以上'] += 1
    drawFunnel('{}相关商品的价格分布'.format(name), data)

if __name__ == '__main__':
    crawler = JDGoodsCrawler()
    name = crawler.run()
    draw(name)
