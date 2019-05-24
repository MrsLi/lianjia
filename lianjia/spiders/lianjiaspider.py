# coding=utf-8
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.loader import ItemLoader
from lianjia.items import LianjiaItem
from lianjia.proxies import Proxies
from datetime import datetime
import time
from scrapy.exceptions import CloseSpider
user_id=110
class MySpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['lianjia.com']
    host = 'https://sh.lianjia.com/'
    # host = 'https://bj.lianjia.com/' 北京
    start_urls = [host+'zufang/']


    def parse(self,response):
        # print(response.text)
        # sel =Selector(response)
        # selectprElem = sel.xpath('//*[@id="content"]/div[1]/div[2]/a[5]')
        # #pageNumElem = selectprElem.xpath('@page-data').extract()[0]
        # #pageNum = eval(pageNumElem)['totalPage']
        # pageNum = sel.xpath('//div[@data-el="page_navigation"]').extract()
        # print(len(pageNum))
        for i in range(10):
            url =self.start_urls[0]+'pg'+str(i)
            print('url:'+url)
            yield Request(url,self.parse_zufang)
            return


    #爬取列表
    def parse_zufang(self,response):
        sel = Selector(response)
        selectorElm = sel.xpath('//*[@id="content"]/div[1]/div[1]/div')
        print(len(selectorElm))
        for item in selectorElm:
            picPanelElm = item.xpath('div/p[1]')
            infoUrl = picPanelElm.xpath('a/@href').extract()[0]#详细信息链接
            print('列表URL:' +infoUrl)
            yield Request(infoUrl, self.parse_info)



    #爬取详情信息
    def parse_info(self,response):
        item_loader = ItemLoader(item=LianjiaItem(), response=response)
        lianjiaItem = LianjiaItem()

        global  user_id
        user_id+=1
        if user_id > 222:
            raise CloseSpider
        else:
            sel =Selector(response)
            title =sel.xpath('//div[3]/div[1]/div[3]/p/text()').extract()[0]#标题
            description =sel.xpath('//*[@id="desc"]/ul/li/p[1]/text()').extract()[0]#经纪人描述房源信息
            room_pulsh_time = sel.xpath('//div[3]/div[1]/div[3]/div[1]/text()').extract()[0]
            lianjiaItem['user_id'] = user_id
            lianjiaItem['title'] = title
            lianjiaItem['description'] = description
            lianjiaItem['room_pulsh_time'] = room_pulsh_time.replace('房源上架时间 ','')

            print(title)

            #图片信息
            imgList =sel.xpath('//*[@id="prefix"]/li')
            imgDict = list()
            for imgItem in imgList:
                imgSrcList = imgItem.xpath('img/@src').extract()#图片URl
                if len(imgSrcList)>0:
                    imgDict.append(imgSrcList[0])
            lianjiaItem['imgList'] = imgDict


            # 具体信息
            contentElem = sel.xpath('//*[@id="aside"]')
            totalProcexpath = contentElem.xpath('p[1]/span/text()').extract()

            if len(totalProcexpath) > 0:
                totalPrice = totalProcexpath[0]#价格
            else:
                totalPrice = '面议'

            priceUnitxpath = contentElem.xpath('p[1]/text()').extract()

            if len(priceUnitxpath) > 0:
                priceUnit = priceUnitxpath[0]  # 价格单位
            else:
                priceUnit = ''
            lianjiaItem['totalPrice']=totalPrice
            lianjiaItem['priceUnit']=priceUnit


            # infoList = contentElem.xpath('div[@class="zf-room"]/p')
            # infoDict = dict()
            # for infoItem in infoList:
            #     infoKey = infoItem.xpath('i/text()').extract()[0]#键
            #
            #     if infoKey == "位置：":
            #         infoValue = infoItem.xpath('a/text()').extract()[0]+'&'+infoItem.xpath('a/text()').extract()[1]
            #     elif infoKey== "小区：":
            #         infoValue = infoItem.xpath('a/text()').extract()[0]
            #     else:
            #         infoValue = infoItem.xpath('text()').extract()[0]
            #     infoDict.setdefault(infoKey,infoValue)
            # lianjiaItem['infoList'] = infoDict
            lianjiaItem['location'] = contentElem.xpath('//*[@id="mapDetail"]/div[3]/div[2]/ul[2]/li[1]/p[1]/text()').extract()[0]
            lianjiaItem['room_type'] = contentElem.xpath('//*[@id="aside"]/ul[1]/p/span[2]/text()').extract()[0]#房屋户型

            #经纪人(发布人)信息
            #brokerInfoElem = contentElem.xpath('div[@class="brokerInfo"]')
            #brokerheaderImg = brokerInfoElem.xpath('a/img/@src').extract()[0]#经济人头像
            #brokerName = brokerInfoElem.xpath('div[@class="brokerInfoText"]/div[@class="brokerName"]/a/text()').extract()[0]#经济人名字
            #brokerPhone = brokerInfoElem.xpath('div[@class="brokerInfoText"]/div[@class="phone"]/text()').extract()[0]  # 电话(有待验证)

            #lianjiaItem['brokerheaderImg'] = brokerheaderImg
            #lianjiaItem['brokerName'] = brokerName
            lianjiaItem['brokerPhone'] = contentElem.xpath('//*[@id="aside"]/ul[2]/li/p[2]/text()').extract()[0]

            # #基本属性
            lianjiaItem['chuzu_type'] = contentElem.xpath('//*[@id="aside"]/ul[1]/p/span[1]/text()').extract()[0]#出租方式
            # roomBaseInfoElem = sel.xpath('//*[@id="introduction"]/div/div[2]/div[1]/div[2]/ul/li')
            # roomBaseInfoElemDict = dict()
            # for  roomBaseInfo in roomBaseInfoElem:
            #     roomBaseInfoKey =roomBaseInfo.xpath('span/text()').extract()
            #     roomBaseInfoValue =roomBaseInfo.xpath('text()').extract()
            #     if len(roomBaseInfoKey) > 0 and len(roomBaseInfoValue) > 0:
            #         roomBaseInfoElemDict.setdefault(roomBaseInfoKey[0], roomBaseInfoValue[0])
            # lianjiaItem['roomBaseInfoElem'] = roomBaseInfoElemDict

            #房源特色(介绍)
            # roomInfoElem = sel.xpath('//*[@id="introduction"]/div/div[2]/div[2]/div[@class="featureContent"]/ul/li')
            # roomInfoElemDict = dict()
            # for roomInfo in roomInfoElem:
            #     roomInfoKey = roomInfo.xpath('span[@class="label"]/text()').extract()#key
            #     roomInfoValue = roomInfo.xpath('span[@class="text"]/text()').extract()#value
            #     if len(roomInfoKey) > 0 and len(roomInfoValue) > 0:
            #         roomInfoElemDict.setdefault(roomInfoKey[0], roomInfoValue[0])
            # lianjiaItem['roomInfoElem'] = roomInfoElemDict

            yield lianjiaItem


