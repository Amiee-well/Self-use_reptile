import sys,time,re,json,os
import requests
import pandas as pd
from threading import Thread
from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.globals import ThemeType
from pyecharts.charts import Bar
from pyecharts.faker import  Faker
from pyecharts.charts import Line
from pyecharts.commons.utils import JsCode
from pyecharts.charts import WordCloud
from QcureUi import cure
from PyQt5.QtGui import QIcon,QFont
from PyQt5.QtWidgets import QWidget,QVBoxLayout,QLabel,QPushButton,QTextEdit,\
    QMessageBox,QDesktopWidget,QApplication,QFileDialog
from PyQt5.QtCore import Qt,QRect

class Ui_main_widget(QWidget):
    def __init__(self):
        self.directory = False
        super(Ui_main_widget,self).__init__()
        self.setupUi()
        self.show()
        self.resize(300, 299)
    def setupUi(self):
        self.widget = QWidget()
        self.Layout = QVBoxLayout(self.widget)
        self.Layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.Layout)
        self.setWindowFlag(Qt.Tool)
        self.main_widget = QWidget()
        self.Layout.addWidget(self.main_widget)
        self.label = QLabel(self.main_widget)
        self.label.setGeometry(QRect(0, 0, 291, 41))
        self.label.setText("新型冠状病毒爬虫作业")
        font = QFont()
        font.setPointSize(17)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.select = QPushButton(self.main_widget)
        self.select.setGeometry(QRect(0, 40, 301, 80))
        self.select.setText("选择文件夹")
        self.select.clicked.connect(self.select_def)
        font.setPointSize(29)
        font.setBold(True)
        font.setWeight(75)
        self.select.setFont(font)
        self.start_up = QPushButton(self.main_widget)
        self.start_up.setGeometry(QRect(0, 130, 301, 80))
        self.start_up.setText("启动爬虫")
        self.start_up.clicked.connect(self.start)
        font.setPointSize(29)
        font.setBold(True)
        font.setWeight(75)
        self.start_up.setFont(font)
        self.open = QPushButton(self.main_widget)
        self.open.setGeometry(QRect(0, 220, 301, 80))
        self.open.setText("打开文件夹")
        self.open.clicked.connect(self.opener)
        font.setPointSize(29)
        font.setBold(True)
        font.setWeight(75)
        self.open.setFont(font)
    def select_def(self):
        self.directory = QFileDialog.getExistingDirectory(self, "请选择爬虫文件夹", "./")
        if self.directory:
            QMessageBox.about(self,"成功","文件夹选择成功\n{}".format(self.directory))
    def start(self):
        if self.directory:
            QMessageBox.about(self,"爬虫","爬虫已启动。\n请等待")
            download_start = Thread(target=parse,args=(self.directory,))
            download_start.start()
        else:
            reply = QMessageBox.question(self, '文件夹未选择', '您未选择文件夹\n是否启动当前文件夹爬虫',
                                           QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                QMessageBox.about(self,"爬虫","爬虫已启动。\n请等待")
                download_start = Thread(target=parse)
                download_start.start()
    def opener(self):
        if self.directory:
            self.directory = self.directory.replace("/",'\\')
            os.system(r'explorer {}'.format(self.directory))
        else:
            self.directory = os.getcwd().replace("/",'\\')
            os.system(r'explorer {}'.format(self.directory))
class parse(object):
    def __init__(self, Contents=os.getcwd(), url='https://gwpre.sina.cn/interface/fymap2020_data.json?_={}&callback=dataAPIData'.format(int(time.time()*1000))):
        self.url = url
        self.Contents = Contents
        self.headers = {
	        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36',
	        'Referer':'https://news.sina.cn/zt_d/yiqing0121'
        }
        self.get_html()
    def get_html(self):
        html = requests.get(self.url,headers = self.headers)
        take_json = re.compile('{"data_title":"fymap","data":(.*?)}}')
        new_json = take_json.findall(html.text)
        new_json = json.loads(new_json[0]+'}}')
        province_dict = {
		    '省份名字':[],
		    '省份英文名字':[],
		    '目前确诊人数':[],
		    '累计确诊人数':[],
		    '治愈人数':[],
		    '目前死亡人数':[],	
		    '现存无症状人数':[],
		    '目前怀疑感染人数':[],
		    '目前境外输入人数':[],
		    '较昨日增加人数':[],
		    '连续无感染天数':[],

	    }
        city_dict = {
		    '城市名字':[],
		    '目前确诊人数':[],
		    '累计确诊人数':[],
		    '目前治愈人数':[],
		    '目前死亡人数':[],
		    '现存无症状人数':[],
		    '目前怀疑感染人数':[],
		    '目前境外输入人数':[],
		    '较昨日增加人数':[],
		    '连续无感染天数':[],
	    }
        for i in new_json['list']:
            province_dict['省份名字'].append(i['name'])
            province_dict['省份英文名字'].append(i['ename'])
            province_dict['现存无症状人数'].append(i['asymptomNum'])
            province_dict['治愈人数'].append(i['cureNum'])
            province_dict['目前死亡人数'].append(i['deathNum'])
            province_dict['目前确诊人数'].append(i['econNum'])
            province_dict['累计确诊人数'].append(i['value'])
            province_dict['目前怀疑感染人数'].append(i['susNum'])
            province_dict['目前境外输入人数'].append(i['jwsrNum'])
            province_dict['较昨日增加人数'].append(i['conadd'])		
            province_dict['连续无感染天数'].append(i['zerodays'])	
            for t in i['city']:
                city_dict['城市名字'].append(t['mapName'])	
                city_dict['累计确诊人数'].append(t['conNum'])	
                city_dict['目前治愈人数'].append(t['cureNum'])
                city_dict['目前死亡人数'].append(t['deathNum'])
                city_dict['目前确诊人数'].append(t['econNum'])
                city_dict['较昨日增加人数'].append(t['conadd'])
                city_dict['连续无感染天数'].append(t['zerodays'])
                city_dict['目前境外输入人数'].append(t['jwsr'])
                city_dict['现存无症状人数'].append(t['asymptomNum'])
                city_dict['目前怀疑感染人数'].append(t['susNum'])
        province_data = pd.DataFrame(province_dict)
        city_data = pd.DataFrame(city_dict)
        for i in province_dict:
            province_data[i] = province_data[i].apply(lambda x: '0' if x=='' else x)
        for i in city_dict:
            city_data[i] = city_data[i].apply(lambda x: '0' if x=='' else x)
        city_data = city_data[~city_data['城市名字'].isin(['境外','外来','0'])]
        province_id = province_data['省份名字'].values.tolist()
        province_set = province_data['累计确诊人数'].values.tolist()
        self.filename = self.Contents+'/数据可视化/'
        if not os.path.exists(self.filename):
            os.makedirs(self.filename)
        self.di_tu(province_id,province_set)
        self.zhu_zhuang(province_id,province_set)
        city_id = city_data['城市名字'].values.tolist()
        city_set = city_data['累计确诊人数'].values.tolist()
        whole_id = province_id + city_id
        whole_data = province_set + city_set
        self.ci_yun(whole_id, whole_data)
        province_set = province_data['治愈人数'].values.tolist()
        self.zhe_xian(province_id, province_set)
        province_data.to_csv(self.Contents + "/疫情省份分析.csv",encoding='utf-8-sig')
        city_data.to_csv(self.Contents + "/疫情城市分析.csv",encoding='utf-8-sig')
    def di_tu(self, your_id, your_data):
        m = Map()
        m.add("确诊人数", [list(z) for z in zip(your_id, your_data)], "china")
        m.set_global_opts(title_opts=opts.TitleOpts(title="新型冠状病毒疫情图"),
				        visualmap_opts=opts.VisualMapOpts(max_=800))
        m.render(self.Contents + "/数据可视化/地图.html")
    def zhu_zhuang(self, your_id, your_data):
        bar = Bar(
        init_opts = opts.InitOpts(
	        theme = ThemeType.PURPLE_PASSION,
	        width = "1280px",
	        height = "720px"))
        bar.add_xaxis(your_id)
        bar.add_yaxis('确诊人数',your_data)
        bar.set_global_opts(
	        title_opts = opts.TitleOpts(
		        title = '新型冠状病毒柱状图'),
	        datazoom_opts = [opts.DataZoomOpts()],
	        xaxis_opts = opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=10)))
        bar.render(self.filename+ "柱状图.html")
    def ci_yun(self, your_id, your_data):
        new = list(zip(your_id, your_data))
        words = new
        wordcloud = WordCloud(init_opts=opts.InitOpts(width="1920px",height='960px'))
        wordcloud.add('',words,word_size_range=[20,100])
        wordcloud.set_global_opts(title_opts = opts.TitleOpts(title = '新型冠状病毒词云图'))
        wordcloud.render(self.filename+ "词云图.html")
        
    def zhe_xian(self, your_id, your_data):
        x_data = your_id
        y_data = your_data
        background_color_js = (
            "new echarts.graphic.LinearGradient(0, 0, 0, 1, "
            "[{offset: 0, color: '#c86589'}, {offset: 1, color: '#06a7ff'}], false)"
        )
        area_color_js = (
            "new echarts.graphic.LinearGradient(0, 0, 0, 1, "
            "[{offset: 0, color: '#eb64fb'}, {offset: 1, color: '#3fbbff0d'}], false)"
        )
        c = (
            Line(init_opts=opts.InitOpts(bg_color=JsCode(background_color_js)))
            .add_xaxis(xaxis_data=x_data)
            .add_yaxis(
                series_name="治愈人数总量",
                y_axis=y_data,
                is_smooth=True,
                is_symbol_show=True,
                symbol="circle",
                symbol_size=6,
                linestyle_opts=opts.LineStyleOpts(color="#fff"),
                label_opts=opts.LabelOpts(is_show=True, position="top", color="white"),
                itemstyle_opts=opts.ItemStyleOpts(
                    color="red", border_color="#fff", border_width=3
                ),
                tooltip_opts=opts.TooltipOpts(is_show=False),
                areastyle_opts=opts.AreaStyleOpts(color=JsCode(area_color_js), opacity=1),
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title="目前治愈人数",
                    pos_bottom="5%",
                    pos_left="center",
                    title_textstyle_opts=opts.TextStyleOpts(color="#fff", font_size=16),
                ),
                xaxis_opts=opts.AxisOpts(
                    type_="category",
                    boundary_gap=False,
                    axislabel_opts=opts.LabelOpts(margin=30, color="#ffffff63"),
                    axisline_opts=opts.AxisLineOpts(is_show=False),
                    axistick_opts=opts.AxisTickOpts(
                        is_show=True,
                        length=25,
                        linestyle_opts=opts.LineStyleOpts(color="#ffffff1f"),
                    ),
                    splitline_opts=opts.SplitLineOpts(
                        is_show=True, linestyle_opts=opts.LineStyleOpts(color="#ffffff1f")
                    ),
                ),
                yaxis_opts=opts.AxisOpts(
                    type_="value",
                    position="right",
                    axislabel_opts=opts.LabelOpts(margin=20, color="#ffffff63"),
                    axisline_opts=opts.AxisLineOpts(
                        linestyle_opts=opts.LineStyleOpts(width=2, color="#fff")
                    ),
                    axistick_opts=opts.AxisTickOpts(
                        is_show=True,
                        length=15,
                        linestyle_opts=opts.LineStyleOpts(color="#ffffff1f"),
                    ),
                    splitline_opts=opts.SplitLineOpts(
                        is_show=True, linestyle_opts=opts.LineStyleOpts(color="#ffffff1f")
                    ),
                ),
                legend_opts=opts.LegendOpts(is_show=False),
            )
        )
        c.render(self.filename+ "渐变折线图.html")
if __name__ == "__main__":
    print(os.getcwd())
    app = QApplication(sys.argv)
    win = cure.Windows(Ui_main_widget(), '新冠病毒托盘', True, '新冠病毒-李凯','New.ico')
    sys.exit(app.exec_())
