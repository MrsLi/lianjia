# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    user_id = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()#经纪人描述房源信息

    imgList = scrapy.Field()#list  图片信息

    totalPrice = scrapy.Field()#价格
    priceUnit = scrapy.Field()#单位

    infoList = scrapy.Field()#dic 位置信息

    location = scrapy.Field()#位置信息
    room_type = scrapy.Field()#房屋户型
    chuzu_type = scrapy.Field()#出租方式
    room_pulsh_time = scrapy.Field()#发布时间

    # 经纪人(发布人)信息
    brokerheaderImg = scrapy.Field()
    brokerName = scrapy.Field()
    brokerPhone = scrapy.Field()

    roomBaseInfoElem = scrapy.Field()#dic

    roomInfoElem = scrapy.Field()#dic
    pass
