# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SanxinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    phone_name=scrapy.Field()       #手机名称
    price=scrapy.Field()            #价格
    battery_life=scrapy.Field()     #电池容量
    running_memory=scrapy.Field()   #运行内存
    body_color=scrapy.Field()       #机身颜色
    front_pixel=scrapy.Field()       #前置摄像头
    post_pixel=scrapy.Field()       #后置摄像头