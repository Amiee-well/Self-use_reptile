import scrapy
from stackoverflowSpider.items import StackoverflowspiderItem


'''爬虫类'''
class StackoverflowSpider(scrapy.Spider):
    name = 'StackoverflowSpider'
    def start_requests(self):
        url_format = 'https://stackoverflow.com/questions/tagged/python?tab=newest&page={}&pagesize=15'
        for i in range(84561):
            yield scrapy.Request(url_format.format(i), callback=self.parse)
    def parse(self, response):
        questions = response.xpath('//*[@id="questions"]')
        for question in questions.xpath('./div'):
            item = StackoverflowspiderItem()
            item['title'] = question.xpath('div[2]/h3/a/text()').extract()[0]
            item['question_link'] = 'https://stackoverflow.com' + question.xpath('div[2]/h3/a/@href').extract()[0]
            item['num_votes'] = int(question.xpath('div[1]/div[1]/div[1]/div[1]/span/strong/text()').extract()[0])
            item['num_answers'] = int(question.xpath('div[1]/div[1]/div[2]/strong/text()').extract()[0])
            item['num_views'] = int(question.xpath('div[1]/div[2]/@title').extract()[0].split(' ')[0])
            tags = []
            for tag in question.xpath('div[2]/div[2]').xpath('./a'):
                tags.append(tag.xpath('text()').extract()[0])
            item['tags'] = tags
            yield item
