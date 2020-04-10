import os
import json
from pyecharts import options
from wordcloud import WordCloud
from pyecharts.globals import ThemeType
from pyecharts.charts import Pie, Bar, Funnel


'''检查文件在是否存在'''
def checkDir(dirpath):
	if not os.path.exists(dirpath):
		os.mkdir(dirpath)
		return False
	return True


'''画饼图'''
def drawPie(title, data, savepath='./results'):
	checkDir(savepath)
	pie = (Pie(init_opts=options.InitOpts(theme=ThemeType.VINTAGE))
		  .add('', [list(item) for item in data.items()], radius=['30%', '75%'], center=['25%', '50%'], rosetype='radius')
		  .set_global_opts(title_opts=options.TitleOpts(title=title, pos_left='center'), legend_opts=options.LegendOpts(orient='vertical', pos_top='5%', pos_left='50%')))
	pie.render(os.path.join(savepath, title+'.html'))


'''画柱状图'''
def drawBar(title, data, savepath='./results'):
	checkDir(savepath)
	bar = (Bar(init_opts=options.InitOpts(theme=ThemeType.VINTAGE))
		  .add_xaxis(list(data.keys()))
		  .add_yaxis('', list(data.values()))
		  .set_global_opts(xaxis_opts=options.AxisOpts(axislabel_opts=options.LabelOpts(rotate=-30)),
		  				   title_opts=options.TitleOpts(title=title, pos_left='center'), legend_opts=options.LegendOpts(orient='vertical', pos_top='15%', pos_left='2%')))
	bar.render(os.path.join(savepath, title+'.html'))


'''漏斗图'''
def drawFunnel(title, data, savepath='./results'):
	checkDir(savepath)
	funnel = (Funnel(init_opts=options.InitOpts(theme=ThemeType.MACARONS))
			 .add('', [list(item) for item in data.items()], label_opts=options.LabelOpts(position="inside"))
			 .set_global_opts(title_opts=options.TitleOpts(title=title, pos_left='center'), legend_opts=options.LegendOpts(orient='vertical', pos_top='15%', pos_left='2%')))
	funnel.render(os.path.join(savepath, title+'.html'))


'''统计词频'''
def statisticsWF(texts, stopwords):
	words_dict = {}
	for text in texts:
		words = text.split(' ')
		for word in words:
			word = word.lower().replace('[', '').replace(']', '').replace('.', '').replace(',', '')
			if word in stopwords:
				continue
			if word in words_dict.keys():
				words_dict[word] += 1
			else:
				words_dict[word] = 1
	return words_dict


'''词云'''
def drawWordCloud(words, title, savepath='./results'):
	checkDir(savepath)
	wc = WordCloud(font_path='simkai.ttf', background_color='white', max_words=2000, width=1920, height=1080, margin=5)
	wc.generate_from_frequencies(words)
	wc.to_file(os.path.join(savepath, title+'.png'))


'''run'''
if __name__ == '__main__':
	with open('stackoverflow.json', 'r', encoding='utf-8') as f:
		all_data = json.load(f)
	'''问题标题词云图'''
	stopwords = open('enstopwords.data', 'r', encoding='utf-8').read().split('\n')
	texts = [each.get('title') for each in all_data]
	words_dict = statisticsWF(texts, stopwords)
	drawWordCloud(words_dict, '问题标题词云图', savepath='./results')
	'''Tag统计'''
	tags = []
	for each in all_data:
		tags += each.get('tags')
	tags_dict = dict()
	for tag in set(tags):
		tags_dict[tag] = tags.count(tag)
	tags_dict = dict(sorted(tags_dict.items(), key=lambda item: item[1], reverse=True)[:10])
	drawBar('Python话题下tag前10', tags_dict)
	'''回答数量分布'''
	keys = ['无回答', '1-2', '2-4', '4-6', '6-8', '8-10', '10以上']
	num_answers_dict = dict(zip(keys, [0 for _ in range(len(keys))]))
	for each in all_data:
		num_answers = each.get('num_answers')
		if num_answers == 0:
			num_answers_dict['无回答'] += 1
		elif num_answers <= 2:
			num_answers_dict['1-2'] += 1
		elif num_answers <= 4:
			num_answers_dict['2-4'] += 1
		elif num_answers <= 6:
			num_answers_dict['4-6'] += 1
		elif num_answers <= 8:
			num_answers_dict['6-8'] += 1
		elif num_answers <= 10:
			num_answers_dict['8-10'] += 1
		else:
			num_answers_dict['10以上'] += 1
	drawPie('Python话题下回答数量分布', num_answers_dict)
	'''问题浏览量分布'''
	keys = ['小于100', '100-200', '200-400', '400-600', '600-800', '800-1000', '1000以上']
	num_views_dict = dict(zip(keys, [0 for _ in range(len(keys))]))
	for each in all_data:
		num_views = each.get('num_views')
		if num_views < 100:
			num_views_dict['小于100'] += 1
		elif num_views <= 200:
			num_views_dict['100-200'] += 1
		elif num_views <= 400:
			num_views_dict['200-400'] += 1
		elif num_views <= 600:
			num_views_dict['400-600'] += 1
		elif num_views <= 800:
			num_views_dict['600-800'] += 1
		elif num_views <= 1000:
			num_views_dict['800-1000'] += 1
		else:
			num_views_dict['1000以上'] += 1
	drawFunnel('Python话题下问题浏览量分布', num_views_dict)
