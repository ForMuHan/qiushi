# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from qiushi.items import QiushiItem


class ImagespiderSpider(CrawlSpider):
    # 生成命令：scrapy genspider -t crawl tencent tencent.com
    name = 'imagespider'
    allowed_domains = ['qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/imgrank/page/1/']

    rules = (
        # 第一个参数用来匹配url，第二个参数用来指定解析方法，第三个参数用来确定是否在深层页面继续查找是否有匹配的url
        Rule(LinkExtractor(allow=r'/imgrank/page/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        for each in response.xpath('//div[contains(@id,"qiushi_tag")]'):
            item = QiushiItem()
            # 有一些没起名字的用户，html数据结构不一样，暂时就不处理了
            item['name']=each.xpath("./div/a/h2/text()").extract()
            item['image']=each.xpath("./div[@class='thumb']/a/img/@src").extract()
            # 直接把结果返回给pipelines文件
            yield item
            # 使用CrawlSpider之后，不需要再yield请求了，rules规则中符合条件的url都会直接发送给调度器加入队列

