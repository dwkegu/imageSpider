import scrapy
import os
from urllib import request,response
import time
import re
from scrapy.linkextractors import LinkExtractor

class QuotesSpider(scrapy.Spider):
    name = "imageSpider"
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
            'http://www.ivsky.com/tupian/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse2)

    def parse2(self, response):
        # 选择图片标签
        #第一个部分/html/body/div[3]/div[2]/ul/li[1]
        self.count +=1
        imagesUrl = response.xpath('//ul[contains(@class,"ali")]/li/div/a/img/@src').extract()
        if imagesUrl is not None:
            for item in imagesUrl:
                imageName = str(item).split('/')[-1]
                self.saveImage(response.url, item, imageName)
                self.log('Saved file %s' % item)
        else:
            self.log("no img")
        # 第二部分 进入得到中图
        mImagesUrl = response.xpath('//ul[contains(@class,"ali")]/li/div/a/@href').extract()

        if mImagesUrl is not None:
            for item in mImagesUrl:
                if item.startswith("http"):
                    yield scrapy.Request(url=item, callback=self.parse3)
                else:
                    yield scrapy.Request(self._host+item, callback=self.parse3)
        xpStr = '//div[contains(@class, "pagelist")]/a[contains(@href, "/tupian/index_' \
                + str(self.count + 1) + '.html")]/@href'
        nextPageNum = response.xpath(xpStr).extract()
        if len(nextPageNum)>0:
            if self.count<2:
                print("next_page_next_page____________________________________________________________")
                yield scrapy.Request(self._host+nextPageNum[0], callback=self.parse2)


    def parse3(self, response):

        imagesUrl = response.xpath('//ul[contains(@class, "pli")]/li/div/a/img/@src').extract()
        if imagesUrl is not None:
            for item in imagesUrl:
                imageName = str(item).split('/')[-1]
                self.saveImage(response.url, item, imageName)
                self.log('Saved file %s' % item)
        else:
            self.log("no img")
        bImagesUrl = response.xpath('//ul[contains(@class,"pli")]/li/div/a/@href').extract()
        print(bImagesUrl)
        if bImagesUrl is not None:
            for item in bImagesUrl:
                if item.startswith("http"):
                    yield scrapy.Request(item, callback=self.parse4)
                else:
                    yield scrapy.Request(self._host+item, callback=self.parse4)
    def parse4(self, response):
        print("save_big_image________________________________________________________________")
        image = response.xpath('//img[@id="imgis"]/@src').extract()
        print(image)
        if image is not None:
            imageName = str(image[0]).split('/')[-1]
            self.saveImage(response.url, image[0], imageName)
            self.log('Saved file %s' % image[0])
        else:
            self.log("no img")

    def parse(self, response):
        self.count +=1
        url = response.url
        print(response.url, "  url counts:", self.count)
        #选择图片标签
        # response.css('img').xpath('@src').extract()
        imagesUrl = response.css("img::attr(src)").extract()
        if imagesUrl is not None:
            for item in imagesUrl:
                imageName = str(item).split('/')[-1]
                self.saveImage(self.host, item,imageName)
                self.log('Saved file %s' % item)
        else:
            self.log("no img")

        # 选择连接标签
        nextPages = []

        nextUrl = response.css("a::attr(href)").extract()
        for item in nextUrl:
            if not item.startswith("http"):
                item = url + item
            if str(item).__contains__("dongwushijie"):
                nextPages.append(item)
        """x
        mle = LinkExtractor()
        nextPages = mle.extract_links(response={response.url, 'utf8'})
        """
        for item in nextPages:
            yield scrapy.Request(item, callback=self.parse)

    def saveImage(self, host, item, name):
        if item.startswith("http"):
            url = item
        else:
            url = host+item
        mr = request.urlopen(url)
        with open(self.saveDir+str(time.time())+name , 'wb') as f:
            if f is not None:
                f.write(mr.read())