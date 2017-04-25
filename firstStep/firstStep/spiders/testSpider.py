import scrapy
import os
from urllib import request
import time

class QuotesSpider(scrapy.Spider):
    name = "imageSpiderTest"
    saveDir = "image/"

    def __init__(self):
        super().__init__()
        self._host = ''
        self.count = 0
        if not os.path.exists(self.saveDir):
            os.mkdir(self.saveDir)

    def start_requests(self):
        self._host ="http://www.ivsky.com"
        urls = [
            #'http://www.27270.com/word/dongwushijie/list_8_2.html',
            'http://www.ivsky.com/tupian/baishouwan_v40924/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse2)

    def parse2(self, response):
        #print(response.body)
        image = response.xpath('//ul[contains(@class,"pli")]/li/div/a/@href').extract()
        print(image)




    def saveImage(self, host, item, name):
        if item.startswith("http"):
            url = item
        else:
            url = host+item
        mr = request.urlopen(url)
        with open(self.saveDir+str(time.time())+name , 'wb') as f:
            if f is not None:
                f.write(mr.read())